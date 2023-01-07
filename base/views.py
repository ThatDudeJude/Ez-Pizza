from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token import token_generator

# from django.db.models import Q
# from django.contrib.auth.forms import UserCreationForm
from .models import User
from shop.models import (
    Pasta,
    Platter,
    Salad,
    Sicillian,
    Topping,
    Regular,
    Sub,
    ShoppingCartItem,
    SpecialSicillian,
    SpecialRegular,
)
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash

# from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm

from django.contrib import messages

from .forms import (
    RegisterUserForm,
    UpdateProfileForm,
    UpdatePasswordForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
)


# Create your views here.
account_auth_page = False


def login_user(request):
    if request.user.is_authenticated:
        return redirect("index")

    auth = "login"
    account_auth_page = True
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "email does not exist.")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Wrong password.")

    context = {"auth": auth, "account_auth_page": account_auth_page}
    return render(request, "base/login_register.html", context)


def logout_user(request):
    logout(request)
    return redirect("index")


def register_user(request):
    auth = "register"
    account_auth_page = True
    form = RegisterUserForm()
    context = {"auth": auth, "form": form, "account_auth_page": account_auth_page}
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        print("submitting")
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("index")
        else:
            context = {"auth": auth, "form": form}

    return render(request, "base/login_register.html", context)


@login_required(login_url="/user/login")
def get_user_profile(request, action):
    if action == "view":
        context = {"profile": request.user, "type": "view"}
        return render(request, "base/profile.html", context)
    else:
        form = UpdateProfileForm(instance=request.user)

        context = {"form": form, "type": "update"}

        if request.method == "POST":
            form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            context = {"profile": request.user, "type": "view"}
            return render(request, "base/profile.html", context)

        return render(request, "base/profile.html", context)


@login_required(login_url="/user/login/")
def password_change(request):
    form = UpdatePasswordForm(user=request.user)

    if request.method == "POST":
        form = UpdatePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            logout(request)
            return render(request, "base/password_change_done.html")

    context = {"form": form}
    return render(request, "base/password_change_form.html", context)


def password_reset(request):
    form = CustomPasswordResetForm()
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        email = request.POST.get("email")
        if form.is_valid():
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                context = {
                    "form": form,
                    "message": "The email address you entered does not exist in our accounts.",
                }
                return render(request, "base/password_reset_form.html", context)
            else:
                user = User.objects.get(email=email)
                protocol = "https" if request.is_secure() else "http"
                opts = {
                    "use_https": request.is_secure(),
                    "request": request,
                    "subject_template_name": "base/password_reset_subject.txt",
                    "email_template_name": "base/password_reset_email.html",
                    "extra_email_context": {
                        "email": "ezPizza@gmail.com",
                        "site_name": "ezPizza",
                        "domain": request.get_host(),
                        "protocol": protocol,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": token_generator.make_token(user),
                    },
                }
                form.save(**opts)
                return render(request, "base/password_reset_done.html")
    context = {"form": form}
    return render(request, "base/password_reset_form.html", context)


def confirm_password_reset(request, uidb64, token):

    if request.method == "GET":
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, TypeError, ValueError, OverflowError):
            user = None

        else:
            if token_generator.check_token(user, token) and user is not None:
                form = CustomSetPasswordForm(user=user)

                context = {"form": form}

                return render(request, "base/password_reset_confirm.html", context)

        return render(request, "error.html", {"message": "Bad request!"})

    if request.method == "POST":
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
        form = CustomSetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            logout(request)
            return render(request, "base/password_change_done.html")
        else:
            context = {"form": form}

            return render(request, "base/password_reset_confirm.html", context)


def index(request):

    regular_pizzas = Regular.objects.all()
    sicillian_pizzas = Sicillian.objects.all()
    toppings = Topping.objects.all()
    subs = Sub.objects.all()
    pastas = Pasta.objects.all()
    salads = Salad.objects.all()
    platters = Platter.objects.all()
    special_regular = SpecialRegular.objects.first()
    special_sicillian = SpecialSicillian.objects.first()

    context = {
        "user": request.user,
        "regular_pizzas": regular_pizzas,
        "sicillian_pizzas": sicillian_pizzas,
        "toppings": toppings,
        "subs": subs,
        "pastas": pastas,
        "salads": salads,
        "platters": platters,
        "special_regular": special_regular,
        "special_sicillian": special_sicillian,
    }

    return render(request, "base/index.html", context)
