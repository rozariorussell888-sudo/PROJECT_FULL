from datetime import timedelta
import random
import secrets
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from django.db import transaction
from django.utils import timezone
from accounts.models import Student, SignupOTP, PasswordResetOTP
from resources.models import ResourceItem
from requests_app.models import ResourceRequest, ProductRequest, ResourceRequestResponse, WebsiteNotification

def otp_expired(created_at):
    return created_at < timezone.now() - timedelta(minutes=10)

def create_request(request):
    student = get_current_student(request)
    if not student:
        return redirect('login')
    form = ResourceRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        resource_request = form.save(commit=False)
        resource_request.student = student
        resource_request.save()
                                                                        
        WebsiteNotification.objects.bulk_create([
            WebsiteNotification(
                recipient_id=recipient_id, actor=student,
                kind="community_request",
                title=f"New resource request: {resource_request.title}"[:220],
            )
            for recipient_id in Student.objects.exclude(pk=student.pk).values_list("pk", flat=True)
        ], batch_size=500)
        messages.success(request, 'Your resource request was created.')
        return redirect('resource_request_list')
    return render(request, 'create_request.html', {'form': form, 'student': student})

def get_current_student(request):
    student_id = request.session.get("student_id")

    if not student_id:
        return None

    return Student.objects.filter(
        id=student_id
    ).first()

@require_POST
def send_product_request(request, id):

    student = get_current_student(request)

    if not student:
        messages.error(request, "Please login first.")
        return redirect("login")

    resource = get_object_or_404(
        ResourceItem,
        id=id
    )

    if not resource.student:
        messages.error(
            request,
            "This resource does not have an owner."
        )
        return redirect("resource_detail", id=id)

    if resource.category != "equipment":
        messages.info(request, "Direct product requests are available for equipment only.")
        return redirect("resource_detail", id=id)

    if resource.student_id == student.id:
        messages.error(
            request,
            "You cannot request your own product."
        )
        return redirect("resource_detail", id=id)

    message = request.POST.get("message", "").strip()

    with transaction.atomic():

        product_request, created = (
            ProductRequest.objects.select_for_update()
            .get_or_create(
                resource=resource,
                requester=student,
                defaults={
                    "message": message,
                    "status": "pending"
                }
            )
        )

        if not created:

            if product_request.status == "cancelled":
                product_request.status = "pending"
                product_request.message = message
                product_request.save()
                WebsiteNotification.objects.create(
                    recipient=resource.student, actor=student, kind="equipment_request",
                    title=f"Equipment requested again: {resource.title}"[:220],
                )

                messages.success(
                    request,
                    "Your request has been sent again."
                )

            else:
                messages.info(
                    request,
                    "You already requested this product."
                )

            return redirect("my_requests")

    WebsiteNotification.objects.create(
        recipient=resource.student, actor=student, kind="equipment_request",
        title=f"New equipment request: {resource.title}"[:220],
    )
    messages.success(
        request,
        "Product request sent successfully!"
    )

    return redirect("my_requests")

def received_requests(request):

    student = get_current_student(request)

    if not student:
        return redirect("login")

    requests_received = (
        ProductRequest.objects
        .filter(resource__student=student)
        .select_related("resource", "requester")
        .order_by("-created_at")
    )

    community_requests = list(
        ResourceRequest.objects.exclude(student=student)
        .select_related("student").order_by("-created_at")
    )
    my_responses = {r.request_id: r for r in
        ResourceRequestResponse.objects.filter(
            student=student, request_id__in=[r.id for r in community_requests]
        )}
    for community_request in community_requests:
        community_request.my_response = my_responses.get(community_request.id)

    return render(request, "received_requests.html", {
        "requests_received": requests_received,
        "community_requests": community_requests,
        "student": student,
    })

def my_requests(request):

    student = get_current_student(request)

    if not student:
        return redirect("login")

    sent_requests = (
        ProductRequest.objects
        .filter(requester=student)
        .select_related("resource", "resource__student")
        .order_by("-created_at")
    )

    community_requests = (
        ResourceRequest.objects.filter(student=student)
        .prefetch_related("responses__student").order_by("-created_at")
    )
    return render(request, "my_requests.html", {
        "sent_requests": sent_requests,
        "community_requests": community_requests,
        "student": student,
    })

@require_POST
def accept_product_request(request, id):

    student = get_current_student(request)

    if not student:
        return redirect("login")

    with transaction.atomic():

        product_request = get_object_or_404(
            ProductRequest.objects.select_for_update(),
            id=id,
            resource__student=student
        )

        if product_request.status != "pending":
            messages.error(
                request,
                "Only pending requests can be accepted."
            )
            return redirect("received_requests")

        product_request.status = "accepted"
        product_request.save()
        WebsiteNotification.objects.create(
            recipient=product_request.requester, actor=student, kind="equipment_response",
            title=f"Your equipment request was accepted: {product_request.resource.title}"[:220],
        )

    messages.success(
        request,
        "Request accepted successfully!"
    )

    return redirect("received_requests")

@require_POST
def reject_product_request(request, id):

    student = get_current_student(request)

    if not student:
        return redirect("login")

    with transaction.atomic():

        product_request = get_object_or_404(
            ProductRequest.objects.select_for_update(),
            id=id,
            resource__student=student
        )

        if product_request.status != "pending":
            messages.error(
                request,
                "Only pending requests can be rejected."
            )
            return redirect("received_requests")

        product_request.status = "rejected"
        product_request.save()
        WebsiteNotification.objects.create(
            recipient=product_request.requester, actor=student, kind="equipment_response",
            title=f"Your equipment request was rejected: {product_request.resource.title}"[:220],
        )

    messages.success(
        request,
        "Request rejected."
    )

    return redirect("received_requests")

@require_POST
def cancel_product_request(request, id):

    student = get_current_student(request)

    if not student:
        return redirect("login")

    with transaction.atomic():

        product_request = get_object_or_404(
            ProductRequest.objects.select_for_update(),
            id=id,
            requester=student
        )

        if product_request.status != "pending":
            messages.error(
                request,
                "Only pending requests can be cancelled."
            )
            return redirect("my_requests")

        product_request.status = "cancelled"
        product_request.save()

    messages.success(
        request,
        "Your request has been cancelled."
    )

    return redirect("my_requests")


                                                                       
from .forms import ResourceRequestForm


def resource_request_list(request):
    student = get_current_student(request)
    if not student:
        return redirect("login")
                                                                
    items = ResourceRequest.objects.filter(student=student).order_by("-created_at")
    return render(request, "resource_request_list.html", {
        "items": items, "student": student,
    })


def edit_resource_request(request, id):
    student = get_current_student(request)
    if not student:
        return redirect("login")
    item = get_object_or_404(ResourceRequest, id=id, student=student)
    form = ResourceRequestForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Resource request updated.")
        return redirect("resource_request_list")
    return render(request, "edit_resource_request.html", {"form": form, "item": item})


@require_POST
def delete_resource_request(request, id):
    student = get_current_student(request)
    if not student:
        return redirect("login")
    item = get_object_or_404(ResourceRequest, id=id, student=student)
    item.delete()
    messages.success(request, "Resource request deleted.")
    return redirect("resource_request_list")


@require_POST
def respond_to_resource_request(request, id):
    student = get_current_student(request)
    if not student:
        return redirect("login")
    requested_resource = get_object_or_404(ResourceRequest, id=id)
    if requested_resource.student_id == student.id:
        messages.error(request, "You cannot respond to your own resource request.")
        return redirect("received_requests")
    decision = request.POST.get("decision")
    if decision not in ("accepted", "rejected"):
        messages.error(request, "Invalid response.")
        return redirect("received_requests")
    with transaction.atomic():
        response, created = ResourceRequestResponse.objects.select_for_update().get_or_create(
            request=requested_resource, student=student, defaults={"status": decision}
        )
        if not created:
            messages.info(request, "You have already responded to this request.")
            return redirect("received_requests")
    WebsiteNotification.objects.create(
        recipient=requested_resource.student, actor=student, kind="community_response",
        title=f"{student.full_name} {decision} your request: {requested_resource.title}"[:220],
    )
    messages.success(request, "Response saved. The requester can view your decision.")
    return redirect("received_requests")


                                                  
                                          
                                                  

def notifications(request):
    student = get_current_student(request)
    if not student:
        return redirect("login")
    from django.core.paginator import Paginator
    qs = WebsiteNotification.objects.filter(recipient=student).select_related("actor")
    page_obj = Paginator(qs, 20).get_page(request.GET.get("page"))
    return render(request, "notifications.html", {"student": student, "page_obj": page_obj})


@require_POST
def open_notification(request, id):
    student = get_current_student(request)
    if not student:
        return redirect("login")
    item = get_object_or_404(WebsiteNotification, id=id, recipient=student)
    if not item.is_read:
        item.is_read = True
        item.save(update_fields=["is_read"])
    return redirect(item.destination())


@require_POST
def mark_all_notifications_read(request):
    student = get_current_student(request)
    if not student:
        return redirect("login")
    WebsiteNotification.objects.filter(recipient=student, is_read=False).update(is_read=True)
    return redirect("notifications")
