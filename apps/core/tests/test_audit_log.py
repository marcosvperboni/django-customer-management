import pytest
from django.urls import reverse
from rest_framework import status

from apps.core.models import AuditAction, AuditLogEntry
from apps.customers.tests.factories import CustomerFactory, generate_valid_cpf

pytestmark = pytest.mark.django_db


def test_create_writes_audit_log_entry(auth_client, user):
    payload = {
        "full_name": "Audited Customer",
        "document": generate_valid_cpf(4242),
        "email": "audited@example.com",
        "phone": "11988887777",
    }
    response = auth_client.post(reverse("customer-list"), payload)
    assert response.status_code == status.HTTP_201_CREATED

    entry = AuditLogEntry.objects.get(model_label="customers.customer", object_id=str(response.data["id"]))
    assert entry.action == AuditAction.CREATE
    assert entry.user == user


def test_delete_writes_audit_log_entry(auth_client):
    customer = CustomerFactory()
    auth_client.delete(reverse("customer-detail", args=[customer.pk]))

    entry = AuditLogEntry.objects.get(
        model_label="customers.customer", object_id=str(customer.pk), action=AuditAction.DELETE
    )
    assert entry.object_repr == customer.full_name
