from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskModelForm
from tasks.models import Task


def show_task(request):
    return render(request, 'dashboard/dashboard.html')


def admin_dashboard(request):
    tasks = Task.objects.all()
    total_tasks = tasks.count()
    pending_tasks = Task.objects.filter(status="PENDING").count()
    completed_tasks = Task.objects.filter(status="COMPLETED").count()
    in_progress_tasks = Task.objects.filter(status="IN_PROGRESS").count()

    context = {
        "tasks": tasks,
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,
        "in_progress_tasks": in_progress_tasks
    }

    return render(request, "dashboard/admin-dashboard.html", context)


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
