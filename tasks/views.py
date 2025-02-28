from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskModelForm


def show_task(request):
    return render(request, 'dashboard/dashboard.html')


def admin_dashboard(request):
    return render(request, "dashboard/admin-dashboard.html")


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")


def create_task(request):
    form = TaskModelForm()

    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'task-form.html', {"form": form, "message": "Task added successfully!"})

    context = {"form": form}
    return render(request, "task-form.html", context)
