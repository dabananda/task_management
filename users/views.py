from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from users.forms import RegisterForm, CustomRegistrationForm
from django.contrib import messages
from users.forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator


def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(
                request, "A confirmation email has been sent. Please check it out")
            # login(request, user)
            return redirect("log-in")
        else:
            print("Form is not valid")

    return render(request, "registration/register.html", {"form": form})


def log_in(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")

    return render(request, "login/login.html", {'form': form})


def signout(request):
    if request.method == "POST":
        logout(request)
        return redirect("log-in")


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("log-in")
        else:
            return HttpResponse("Invalid id or token")
    except User.DoesNotExist:
        return HttpResponse("User doesn't exist")
