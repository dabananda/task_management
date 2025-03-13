from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout
from users.forms import CustomRegistrationForm, CreateGroupForm
from django.contrib import messages
from users.forms import LoginForm, AssignRuleForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch

# Test for admin


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


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


@login_required
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


@user_passes_test(is_admin, login_url="no-permission")
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr="all_groups")
    ).all()
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = "No group assigned"
    return render(request, "admin/dashboard.html", {"users": users})


@user_passes_test(is_admin, login_url="no-permission")
def assign_rule(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRuleForm()

    if request.method == "POST":
        form = AssignRuleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(
                request, f"{user} has been assigned to {role} role successfully!")
            return redirect("admin-dashboard")

    return render(request, "admin/assign_role.html", {"form": form})


@user_passes_test(is_admin, login_url="no-permission")
def create_group(request):
    form = CreateGroupForm

    if request.method == "POST":
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(
                request, f"{group} group has been created successfully!")
            return redirect('crete-group')

    return render(request, "admin/create_group.html", {"form": form})


@user_passes_test(is_admin, login_url="no-permission")
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, "admin/group_list.html", {"groups": groups})
