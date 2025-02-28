from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm
from tasks.models import Employee, Task


def show_task(request):
    return render(request, 'dashboard/dashboard.html')


def admin_dashboard(request):
    return render(request, "dashboard/admin-dashboard.html")


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")


def create_task(request):
    employees = Employee.objects.all()
    form = TaskForm(employees=employees)

    if request.method == "POST":
        form = TaskForm(request.POST, employees=employees)
        if form.is_valid():
            data = form.cleaned_data
            title = data.get("title")
            description = data.get("description")
            due_date = data.get("due_date")
            assigned_to = data.get("assigned_to")

            task = Task.objects.create(
                title=title, description=description, due_date=due_date)

            for emp_id in assigned_to:
                employee = Employee.objects.get(id=emp_id)
                task.assigned_to.add(employee)

            return HttpResponse("Task added successfully!")

    context = {"form": form}
    return render(request, "task-form.html", context)
