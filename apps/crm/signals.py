from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.crm.models import Task
from apps.crm.tasks import send_task_assignment_email


@receiver(post_save, sender=Task)
def notify_task_assignment(sender, instance: Task, created, **kwargs):
    if instance.assigned_to_id:
        send_task_assignment_email.delay(instance.pk)
