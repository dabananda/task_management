from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Task


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


# @receiver(post_delete, sender=Task)
# def notify_employess_on_task_deletion(sender, instance, **kwargs):
#     if instance.details:
#         instance.details.delete()
