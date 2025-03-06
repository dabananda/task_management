from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskModelForm
from tasks.models import Task
from django.db.models import Count, Q


def show_task(request):
    return render(request, 'dashboard/dashboard.html')


def admin_dashboard(request):
    counts = Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status="COMPLETED")),
        in_progress=Count('id', filter=Q(status="IN_PROGRESS")),
        pending=Count('id', filter=Q(status="PENDING")),
    )

    base_query = Task.objects.select_related(
        "task_details").prefetch_related("assigned_to")

    type = request.GET.get('type', 'all')

    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in-progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')
    elif type == 'all':
        tasks = base_query.all()

    context = {
        "tasks": tasks,
        "counts": counts
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
