from django.db import models
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()

    def __str__(self):
        return self.name


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
    status = models.CharField(
        max_length=15, choices=STATUS_CHOISES, default='PENDING')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


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
    priority = models.CharField(
        max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Task details from {self.task.title}"


@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employess_on_task_creation(sender, instance, action, **kwargs):
    if action == "post_add":
        assigned_emails = [
            employee.email for employee in instance.assigned_to.all()
        ]

        send_mail(
            "New Task Assigned",
            f"You have been assigned to task: {instance.title}",
            "satyajitroy2k20@gmail.com",
            assigned_emails,
        )
