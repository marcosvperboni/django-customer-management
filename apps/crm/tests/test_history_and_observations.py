import pytest
from django.urls import reverse
from rest_framework import status

from apps.crm.tests.factories import ObservationFactory, RelationshipHistoryFactory
from apps.customers.tests.factories import CustomerFactory

pytestmark = pytest.mark.django_db


def test_create_relationship_history_entry(auth_client):
    customer = CustomerFactory()
    payload = {
        "customer": customer.pk,
        "interaction_type": "MEETING",
        "description": "Kickoff meeting with the client.",
        "occurred_at": "2026-01-15T10:00:00Z",
    }
    response = auth_client.post(reverse("relationship-history-list"), payload)
    assert response.status_code == status.HTTP_201_CREATED


def test_relationship_history_requires_exactly_one_party(auth_client):
    payload = {
        "interaction_type": "CALL",
        "description": "No party attached.",
        "occurred_at": "2026-01-15T10:00:00Z",
    }
    response = auth_client.post(reverse("relationship-history-list"), payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_list_relationship_history(auth_client):
    RelationshipHistoryFactory.create_batch(2)
    response = auth_client.get(reverse("relationship-history-list"))
    assert response.data["count"] == 2


def test_create_observation(auth_client):
    customer = CustomerFactory()
    payload = {"customer": customer.pk, "content": "Client prefers morning calls."}
    response = auth_client.post(reverse("observation-list"), payload)
    assert response.status_code == status.HTTP_201_CREATED


def test_update_observation(auth_client):
    observation = ObservationFactory()
    response = auth_client.patch(
        reverse("observation-detail", args=[observation.pk]), {"content": "Updated note."}
    )
    assert response.status_code == status.HTTP_200_OK


def test_delete_observation(auth_client):
    observation = ObservationFactory()
    response = auth_client.delete(reverse("observation-detail", args=[observation.pk]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
