import datetime

import pytest
from django.core import mail
from django.urls import reverse
from rest_framework import status

from apps.crm.tests.factories import TaskFactory
from apps.customers.tests.factories import CustomerFactory

pytestmark = pytest.mark.django_db


def test_create_task(auth_client):
    customer = CustomerFactory()
    payload = {
        "customer": customer.pk,
        "title": "Follow up call",
        "due_date": (datetime.date.today() + datetime.timedelta(days=3)).isoformat(),
    }
    response = auth_client.post(reverse("task-list"), payload)
    assert response.status_code == status.HTTP_201_CREATED


def test_create_task_rejects_past_due_date(auth_client):
    customer = CustomerFactory()
    payload = {
        "customer": customer.pk,
        "title": "Late task",
        "due_date": (datetime.date.today() - datetime.timedelta(days=1)).isoformat(),
    }
    response = auth_client.post(reverse("task-list"), payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "due_date" in response.data


def test_assigning_task_sends_notification_email(auth_client, user):
    customer = CustomerFactory()
    payload = {
        "customer": customer.pk,
        "title": "Prepare proposal",
        "due_date": (datetime.date.today() + datetime.timedelta(days=1)).isoformat(),
        "assigned_to": user.pk,
    }
    response = auth_client.post(reverse("task-list"), payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert len(mail.outbox) == 1
    assert user.email in mail.outbox[0].to


def test_update_task_status(auth_client):
    task = TaskFactory()
    response = auth_client.patch(reverse("task-detail", args=[task.pk]), {"status": "DONE"})
    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.status == "DONE"


def test_filter_tasks_by_status(auth_client):
    TaskFactory(status="PENDING")
    TaskFactory(status="DONE")
    response = auth_client.get(reverse("task-list"), {"status": "DONE"})
    assert response.data["count"] == 1


def test_delete_task(auth_client):
    task = TaskFactory()
    response = auth_client.delete(reverse("task-detail", args=[task.pk]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
