from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm
from tasks.models import Employee


def show_task(request):
    return render(request, 'dashboard/dashboard.html')


def admin_dashboard(request):
    return render(request, "dashboard/admin-dashboard.html")


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")


def create_task(request):
    employees = Employee.objects.all()
    form = TaskForm(employees=employees)
    context = {"form": form}
    return render(request, "task-form.html", context)
