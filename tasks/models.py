from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=150)
    start_date = models.DateField()


class Task(models.Model):
    STATUS_CHOISES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In_Progress'),
        ('COMPLETED', 'Completed'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)
    assigned_to = models.ManyToManyField(Employee, related_name='tasks')
    title = models.CharField(max_length=150)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOISES, default='PENDING')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    )
    task = models.OneToOneField(
        Task, on_delete=models.CASCADE, related_name='task_details')
    assigned_to = models.CharField(max_length=200)
    priority = models.CharField(
        max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
