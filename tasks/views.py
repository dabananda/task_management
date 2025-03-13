from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskModelForm, TaskDetailModelForm
from tasks.models import Task
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required


# Check for manager
def is_manager(user):
    return user.groups.filter(name="Manager").exists()


# Check for manager
def is_employee(user):
    return user.groups.filter(name="Employee").exists()


def show_task(request):
    return render(request, 'dashboard/dashboard.html')


@user_passes_test(is_manager, login_url="no-permission")
def manager_dashboard(request):
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


@user_passes_test(is_employee, login_url="no-permission")
def employee_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

@login_required
@permission_required("tasks.add_task", login_url="no-permission")
def create_task(request):
    task_form = TaskModelForm()
    task_detail_form = TaskDetailModelForm()

    if request.method == "POST":
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task created successfully!")
            return redirect('create-task')

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task-form.html", context)


@login_required
@permission_required("tasks.change_task", login_url="no-permission")
def update_task(request, id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)
    if task.task_details:
        task_detail_form = TaskDetailModelForm(instance=task.task_details)

    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(
            request.POST, instance=task.task_details)
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task updated successfully!")
            return redirect('update-task', id)

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task-form.html", context)


@login_required
@permission_required("tasks.delete_task", login_url="no-permission")
def delete_task(request, id):
    if request.method == "POST":
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, "Task deleted successfully")
        return redirect("admin-dashboard")
    else:
        messages.error(request, "Something went wrong!")
        return redirect("admin-dashboard")
