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
from requests_app.models import ResourceRequest, ProductRequest

def otp_expired(created_at):
    return created_at < timezone.now() - timedelta(minutes=10)

def login(request):

    if request.method == "POST":

        registration_id = request.POST.get(
            "registration_id",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        ).strip()


        student = Student.objects.filter(registration_id=registration_id).first()


        if student and check_password(password, student.password):

            request.session["student_id"] = student.id
            request.session["full_name"] = student.full_name
            request.session["registration_id"] = student.registration_id

            request.session.modified = True

            return redirect("home")


        else:

            return render(
                request,
                "Login.html",
                {
                    "error": "Invalid ID or Password"
                }
            )


                                         
    return render(
        request,
        "Login.html"
    )

def signup(request):

    if request.method == "POST":

        full_name = request.POST.get(
            "full_name",
            ""
        ).strip()

        registration_id = request.POST.get(
            "registration_id",
            ""
        ).strip()

        department = request.POST.get(
            "department",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        ).strip()


                         
        if not email.endswith("@uap-bd.edu"):

            messages.error(
                request,
                "Only UAP email allowed!"
            )

            return redirect("signup")


                              
        if Student.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Email already exists!"
            )

            return redirect("signup")


                                        
        if Student.objects.filter(
            registration_id=registration_id
        ).exists():

            messages.error(
                request,
                "Registration ID already exists!"
            )

            return redirect("signup")


                      
        otp = str(
            random.randint(
                100000,
                999999
            )
        )


                        
        SignupOTP.objects.filter(
            email=email
        ).delete()


                      
        SignupOTP.objects.create(
            email=email,
            otp=otp
        )


                  
        send_mail(
            "Signup Verification OTP",
            f"Your OTP is {otp}",
            settings.EMAIL_HOST_USER,
            [email],
        )


                               
        request.session["signup_data"] = {

            "full_name": full_name,

            "registration_id": registration_id,

            "department": department,

            "email": email,

            "phone": phone,

            "password": make_password(password),
        }


        return redirect(
            "verify_signup_otp"
        )


    return render(
        request,
        "Signup.html"
    )

def verify_signup_otp(request):

    if request.method == "POST":

        user_otp = request.POST.get(
            "otp",
            ""
        ).strip()


        signup_data = request.session.get(
            "signup_data"
        )


        if not signup_data:

            return redirect(
                "signup"
            )


        email = signup_data.get(
            "email"
        )


        otp_record = SignupOTP.objects.filter(
            email=email,
            otp=user_otp
        ).first()


        if otp_record and not otp_expired(otp_record.created_at):

            Student.objects.create(

                full_name=signup_data.get(
                    "full_name"
                ),

                registration_id=signup_data.get(
                    "registration_id"
                ),

                department=signup_data.get(
                    "department"
                ),

                email=signup_data.get(
                    "email"
                ),

                phone=signup_data.get(
                    "phone"
                ),

                password=signup_data.get(
                    "password"
                ),
            )


                        
            otp_record.delete()


                                          
            request.session.pop(
                "signup_data",
                None
            )


            messages.success(
                request,
                "Account created successfully!"
            )


            return redirect(
                "login"
            )


        else:

            return render(
                request,
                "VerifySignupOTP.html",
                {
                    "error": "Invalid or Wrong OTP"
                }
            )


    return render(
        request,
        "VerifySignupOTP.html"
    )

def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get(
            "email",
            ""
        ).strip()


        student = Student.objects.filter(
            email=email
        ).first()


        if student:

                            
            PasswordResetOTP.objects.filter(
                student=student
            ).delete()


                          
            otp = str(
                random.randint(
                    100000,
                    999999
                )
            )


                      
            PasswordResetOTP.objects.create(
                student=student,
                otp=otp
            )


                      
            send_mail(

                subject="Password Reset OTP",

                message=f"Your OTP is {otp}",

                from_email=settings.EMAIL_HOST_USER,

                recipient_list=[
                    email
                ],
            )


            request.session[
                "reset_email"
            ] = email


            return redirect(
                "verify_otp"
            )


        else:

            return render(
                request,
                "ForgotPassword.html",
                {
                    "error": "Email not found"
                }
            )


    return render(
        request,
        "ForgotPassword.html"
    )

def verify_otp(request):

    if request.method == "POST":

        otp = request.POST.get(
            "otp",
            ""
        ).strip()


        email = request.session.get(
            "reset_email"
        )


        if not email:

            return redirect(
                "forgot_password"
            )


        student = Student.objects.filter(
            email=email
        ).first()


        if not student:

            return redirect(
                "forgot_password"
            )


        check = PasswordResetOTP.objects.filter(
            student=student,
            otp=otp
        ).first()


        if check:

            request.session[
                "otp_verified"
            ] = True


            return redirect(
                "reset_password"
            )


        else:

            return render(
                request,
                "VerifyOTP.html",
                {
                    "error": "Wrong OTP"
                }
            )


    return render(
        request,
        "VerifyOTP.html"
    )

def reset_password(request):

    if not request.session.get(
        "otp_verified"
    ):

        return redirect(
            "forgot_password"
        )


    if request.method == "POST":

        password = request.POST.get(
            "password",
            ""
        ).strip()


        email = request.session.get(
            "reset_email"
        )


        student = Student.objects.filter(
            email=email
        ).first()


        if not student:

            return redirect(
                "forgot_password"
            )


        student.password = make_password(password)

        student.save()


                          
        PasswordResetOTP.objects.filter(
            student=student
        ).delete()


                             
        request.session.pop(
            "reset_email",
            None
        )

        request.session.pop(
            "otp_verified",
            None
        )


        messages.success(
            request,
            "Password changed successfully!"
        )


        return redirect(
            "login"
        )


    return render(
        request,
        "ResetPassword.html"
    )

def profile(request):

    student_id = request.session.get(
        "student_id"
    )


    if not student_id:

        messages.error(
            request,
            "Please login first."
        )

        return redirect(
            "login"
        )


    student = Student.objects.filter(
        id=student_id
    ).first()


    if not student:

        request.session.flush()

        messages.error(
            request,
            "Student account not found. Please login again."
        )

        return redirect(
            "login"
        )


    return render(
        request,
        "profile.html",
        {
            "student": student
        }
    )

def logout_view(request):

    request.session.flush()


    messages.success(
        request,
        "Logged out successfully!"
    )


    return redirect(
        "login"
    )
