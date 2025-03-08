from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from users.forms import RegisterForm, CustomRegistrationForm


def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    return render(request, "registration/register.html", {"form": form})


def log_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

    return render(request, "login/login.html")


def signout(request):
    if request.method == "POST":
        logout(request)
        return redirect("log-in")
