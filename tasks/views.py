from django.shortcuts import render
from django.http import HttpResponse


def show_task(request):
    return render(request, 'dashboard/dashboard.html')


def admin_dashboard(request):
    return render(request, "dashboard/admin-dashboard.html")


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")
