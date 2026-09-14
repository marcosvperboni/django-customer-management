from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_task_assignment_email(task_id: int) -> None:
    from apps.crm.models import Task

    try:
        task = Task.objects.select_related("assigned_to").get(pk=task_id)
    except Task.DoesNotExist:
        return

    if not task.assigned_to or not task.assigned_to.email:
        return

    send_mail(
        subject=f"New task assigned: {task.title}",
        message=(
            f"You have been assigned to task '{task.title}', due on {task.due_date}.\n\n"
            f"{task.description}"
        ),
        from_email=None,
        recipient_list=[task.assigned_to.email],
        fail_silently=True,
    )
