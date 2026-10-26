
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from accounts.models import Student
from resources.models import ResourceItem
from requests_app.models import ProductRequest


                                            
                                
                                            

def get_logged_student(request):
    student_id = request.session.get("student_id")

    if not student_id:
        return None

    return Student.objects.filter(id=student_id).first()


                                            
           
                                            

def home(request):
    student = get_logged_student(request)

    if not student:
        request.session.flush()
        return redirect("login")

    return render(request, "home.html", {
        "student": student
    })


                                            
                               
                                            

def resources(request):

                                     
    items = ResourceItem.objects.all().order_by(
        "-created_at", "-id"
    )

                                      
    category = request.GET.get("category", "").strip()
    search = request.GET.get("search", "").strip()

                     
    if category:
        items = items.filter(category=category)

                   
    if search:
        items = items.filter(title__icontains=search)

                                            
                                    
                                            

    paginator = Paginator(items, 15)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

                                                 
    query_params = request.GET.copy()
    query_params.pop("page", None)

    pagination_query = query_params.urlencode()

    context = {
        "items": page_obj,
        "page_obj": page_obj,
        "selected_category": category,
        "search": search,
        "total_items": paginator.count,
        "pagination_query": pagination_query,
    }

    return render(request, "resources2.html", context)


                                            
                  
                                            

def resource_detail(request, id):

    item = ResourceItem.objects.filter(id=id).first()

    if not item:
        return redirect("resources")

    student_id = request.session.get("student_id")

    can_contact_owner = bool(
        item.student_id == student_id or
        ProductRequest.objects.filter(
            resource=item,
            requester_id=student_id,
            status="accepted"
        ).exists()
    ) if student_id else False

    return render(request, "resource_detail.html", {
        "item": item,
        "can_contact_owner": can_contact_owner
    })


                                            
              
                                            

def add_item(request):

    student = get_logged_student(request)

    if not student:
        request.session.flush()
        return redirect("login")

    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        category = request.POST.get("category", "").strip()
        description = request.POST.get("description", "").strip()
        author = request.POST.get("author", "").strip()
        department = request.POST.get("department", "").strip()
        course_code = request.POST.get("course_code", "").strip()
        share_type = request.POST.get("share_type", "share")
        price = request.POST.get("price", "").strip()

        file = request.FILES.get("file")
        image = request.FILES.get("image")

                          
        if not title:
            return render(request, "add_item.html", {
                "student": student,
                "error": "Item title is required."
            })

                             
        allowed_categories = [
            "books",
            "notes",
            "equipment",
            "previous_questions",
            "course_materials",
        ]

        if category not in allowed_categories:
            return render(request, "add_item.html", {
                "student": student,
                "error": "Please select a valid category."
            })

                                              
        if category == "equipment":

            if share_type not in ["share", "rent", "sell"]:
                share_type = "share"

            if share_type == "share":
                price = None

            elif share_type in ["rent", "sell"]:

                if not price:
                    return render(request, "add_item.html", {
                        "student": student,
                        "error": "Price is required for Rent or Sell."
                    })

                                         
        else:
            share_type = "share"
            price = None

                         
        ResourceItem.objects.create(
            student=student,
            title=title,
            category=category,
            description=description,
            author=author,
            department=department,
            course_code=course_code,
            share_type=share_type,
            price=price if price else None,
            file=file,
            image=image,
        )

        messages.success(
            request,
            "Item added successfully!"
        )

        return redirect("my_resources")

    return render(request, "add_item.html", {
        "student": student
    })


                                            
              
                                            

def my_resources(request):

    student = get_logged_student(request)

    if not student:
        request.session.flush()
        return redirect("login")

                                          
    all_items = ResourceItem.objects.filter(
        student=student
    )

                     
    total_items = all_items.count()

    books_count = all_items.filter(
        category="books"
    ).count()

    notes_count = all_items.filter(
        category="notes"
    ).count()

    equipment_count = all_items.filter(
        category="equipment"
    ).count()

    previous_questions_count = all_items.filter(
        category="previous_questions"
    ).count()

    course_materials_count = all_items.filter(
        category="course_materials"
    ).count()

                     
    selected_category = request.GET.get("category", "")

    items = all_items

    if selected_category:
        items = items.filter(
            category=selected_category
        )

                  
    items = items.order_by("-created_at")

    context = {
        "student": student,
        "items": items,
        "total_items": total_items,
        "books_count": books_count,
        "notes_count": notes_count,
        "equipment_count": equipment_count,
        "previous_questions_count": previous_questions_count,
        "course_materials_count": course_materials_count,
        "selected_category": selected_category,
    }

    return render(request, "my_resources.html", context)


                                            
               
                                            

def edit_item(request, id):

    student = get_logged_student(request)

    if not student:
        request.session.flush()
        return redirect("login")

                             
    item = ResourceItem.objects.filter(
        id=id,
        student=student
    ).first()

    if not item:
        messages.error(
            request,
            "Item not found or you do not have permission."
        )
        return redirect("my_resources")

    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        category = request.POST.get("category", "").strip()
        description = request.POST.get("description", "").strip()
        author = request.POST.get("author", "").strip()
        department = request.POST.get("department", "").strip()
        course_code = request.POST.get("course_code", "").strip()
        share_type = request.POST.get("share_type", "share")
        price = request.POST.get("price", "").strip()

                          
        if not title:
            return render(request, "edit_item.html", {
                "student": student,
                "item": item,
                "error": "Item title is required."
            })

                             
        allowed_categories = [
            "books",
            "notes",
            "equipment",
            "previous_questions",
            "course_materials",
        ]

        if category not in allowed_categories:
            return render(request, "edit_item.html", {
                "student": student,
                "item": item,
                "error": "Please select a valid category."
            })

                                        
        if category == "equipment":

            if share_type not in ["share", "rent", "sell"]:
                share_type = "share"

            if share_type == "share":
                price = None

            elif share_type in ["rent", "sell"]:

                if not price:
                    return render(request, "edit_item.html", {
                        "student": student,
                        "item": item,
                        "error": "Price is required for Rent or Sell."
                    })

                                         
        else:
            share_type = "share"
            price = None

                                 
        item.title = title
        item.category = category
        item.description = description
        item.author = author
        item.department = department
        item.course_code = course_code
        item.share_type = share_type
        item.price = price if price else None

                                                 
        new_image = request.FILES.get("image")

        if new_image:
            item.image = new_image

                                               
        new_file = request.FILES.get("file")

        if new_file:
            item.file = new_file

        item.save()

        messages.success(
            request,
            "Item updated successfully!"
        )

        return redirect("my_resources")

    return render(request, "edit_item.html", {
        "student": student,
        "item": item
    })


                                            
                 
                                            

def delete_item(request, id):

    student = get_logged_student(request)

    if not student:
        request.session.flush()
        return redirect("login")

                                        
    item = ResourceItem.objects.filter(
        id=id,
        student=student
    ).first()

    if not item:
        messages.error(
            request,
            "Item not found or you do not have permission."
        )
        return redirect("my_resources")

                                   
    if request.method == "POST":

        item.delete()

        messages.success(
            request,
            "Item deleted successfully!"
        )

    return redirect("my_resources")


                                            
            
                                            

def about(request):
    return render(request, "about.html")
