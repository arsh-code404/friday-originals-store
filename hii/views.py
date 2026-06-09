from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils import timezone

from datetime import datetime, timedelta

import random
import re

from .models import CustomerProfile
from hii.models import Contact, Product

def signup_view(request):
    if request.method == "POST":
        first_name = (request.POST.get("first_name") or "").strip()
        middle_name = (request.POST.get("middle_name") or "").strip()
        phone = (request.POST.get("phone") or "").strip()
        email = (request.POST.get("email") or "").strip().lower()
        password = request.POST.get("password") or ""
        confirm_password = request.POST.get("confirm_password") or ""

        form_data = request.POST

        # REQUIRED FIELD CHECK
        if not first_name or not phone or not email or not password or not confirm_password:
            messages.error(request, "Please fill all required fields.")
            return render(request, "signup.html", {"form_data": form_data})

        # NAME VALIDATION
        if len(first_name) < 2:
            messages.error(request, "First name is too short.")
            return render(request, "signup.html", {"form_data": form_data})

        # EMAIL VALIDATION
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            messages.error(request, "Enter a valid email address.")
            return render(request, "signup.html", {"form_data": form_data})

        # PHONE VALIDATION
        if not phone.isdigit():
            messages.error(request, "Phone number must contain digits only.")
            return render(request, "signup.html", {"form_data": form_data})

        if len(phone) != 10:
            messages.error(request, "Phone number must be exactly 10 digits.")
            return render(request, "signup.html", {"form_data": form_data})

        # PASSWORD VALIDATION
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html", {"form_data": form_data})

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return render(request, "signup.html", {"form_data": form_data})

        # DUPLICATE CHECKS
        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "signup.html", {"form_data": form_data})

        if CustomerProfile.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already registered.")
            return render(request, "signup.html", {"form_data": form_data})

        # CREATE USER
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=middle_name
        )

        # CREATE PROFILE
        CustomerProfile.objects.create(
            user=user,
            middle_name=middle_name,
            phone=phone
        )

        # LOGIN
        login(
            request,
            user,
            backend="django.contrib.auth.backends.ModelBackend"
        )

        # KEEP EXACT MESSAGE
        messages.success(
            request,
            f"Account created successfully\n {first_name}."
        )

        next_url = request.session.get("next_url", "/")
        request.session.pop("next_url", None)


        request.session["skip_home_reveal"] = True
        return redirect(next_url)

    return render(request, "signup.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user:
            login(request, user)

            messages.success(
                request,
                f"Welcome back\n {user.first_name or user.username}"
            )

            next_url = request.session.get("next_url", "/")
            request.session.pop("next_url", None)

            request.session["skip_home_reveal"] = True
            return redirect(next_url)

        messages.error(request, "Invalid email or password")
        return redirect("login")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("/")

def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip().lower()

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return redirect("forgot_password")

        otp = str(random.randint(100000, 999999))

        request.session["reset_email"] = email
        request.session["reset_otp"] = otp

        expiry = timezone.now() + timedelta(minutes=10)

        request.session["reset_expiry"] = expiry.isoformat()

        send_mail(
            subject="Friday Originals Password Reset OTP",
            message=f"""
Your Friday Originals OTP is:

{otp}

This OTP will expire in 10 minutes.

If you did not request this, ignore this email.
            """,
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(
            request,
            "OTP sent successfully to your email."
        )

        return redirect("verify_otp")

    return render(request, "forgot_password.html")


def verify_otp(request):

    if request.method == "POST":

        entered_otp = request.POST.get("otp", "").strip()

        session_otp = request.session.get("reset_otp")
        expiry = request.session.get("reset_expiry")

        if not session_otp or not expiry:
            messages.error(request, "OTP session expired.")
            return redirect("forgot_password")

        expiry_time = timezone.datetime.fromisoformat(expiry)

        if timezone.now() > expiry_time:
            messages.error(request, "OTP expired.")
            return redirect("forgot_password")

        if entered_otp != session_otp:
            messages.error(request, "Invalid OTP.")
            return redirect("verify_otp")

        request.session["otp_verified"] = True

        messages.success(
            request,
            "OTP verified successfully."
        )

        return redirect("reset_password")

    return render(request, "verify_otp.html")


def reset_password(request):

    if not request.session.get("otp_verified"):
        return redirect("forgot_password")

    if request.method == "POST":

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("reset_password")

        if len(password) < 8:
            messages.error(
                request,
                "Password must be at least 8 characters."
            )
            return redirect("reset_password")

        email = request.session.get("reset_email")

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("forgot_password")

        user.set_password(password)
        user.save()

        request.session.pop("reset_email", None)
        request.session.pop("reset_otp", None)
        request.session.pop("reset_expiry", None)
        request.session.pop("otp_verified", None)

        messages.success(
            request,
            "Password reset successfully."
        )

        return redirect("login")

    return render(request, "reset_password.html")


@login_required
def profile_view(request):
    profile, created = CustomerProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "phone": ""
        }
    )

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()

        name_parts = full_name.split(maxsplit=1)

        request.user.first_name = name_parts[0] if name_parts else ""
        request.user.last_name = name_parts[1] if len(name_parts) > 1 else ""
        request.user.email = request.POST.get("email", "").strip()

        request.user.save()

        profile.phone = request.POST.get("phone", "").strip()
        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("profile")

    return render(request, "profile.html", {
        "profile": profile
    })
# MAIN PAGES

def index(request):
    products = Product.objects.all()
    response = render(request, "index.html", {"products": products})

    if request.session.get("skip_home_reveal"):
        del request.session["skip_home_reveal"]

    return response


def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {"products": products})


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == "POST":
        first = request.POST.get('first')
        last = request.POST.get('last')
        service = request.POST.get('service')
        email = request.POST.get('email')
        commnt = request.POST.get('commnt')

        contact = Contact(
            first=first,
            last=last,
            service=service,
            email=email,
            commnt=commnt,
            date=datetime.today()
        )

        contact.save()

        messages.success(request, "Your message has been delivered!")
        return redirect('contact')

    return render(request, 'contact.html')


# PRODUCT PAGE

def product(request, pk):
    product = get_object_or_404(Product, id=pk)

    cart = request.session.get('cart', {})

    return render(request, "product.html", {
        "product": product,
        "cart": cart
    })


# ADD TO CART

def add_to_cart(request, pk):
    if not request.user.is_authenticated:
        request.session["next_url"] = request.META.get("HTTP_REFERER", "/")

        return JsonResponse({
            "login_required": True
        })

    cart = request.session.get("cart", {})

    qty = int(request.POST.get("quantity", 1))

    pk = str(pk)

    if pk in cart:
        cart[pk] += qty
    else:
        cart[pk] = qty

    request.session["cart"] = cart

    total_items = sum(cart.values())

    return JsonResponse({
        "login_required": False,
        "cartq": total_items
    })




