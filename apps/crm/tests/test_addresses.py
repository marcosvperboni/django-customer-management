import pytest
from django.urls import reverse
from rest_framework import status

from apps.crm.tests.factories import AddressFactory
from apps.customers.tests.factories import CustomerFactory

pytestmark = pytest.mark.django_db


def test_create_address(auth_client):
    customer = CustomerFactory()
    payload = {
        "customer": customer.pk,
        "street": "Rua Augusta",
        "number": "500",
        "neighborhood": "Consolacao",
        "city": "Sao Paulo",
        "state": "SP",
        "zip_code": "01305-000",
    }
    response = auth_client.post(reverse("address-list"), payload)
    assert response.status_code == status.HTTP_201_CREATED


def test_create_address_rejects_invalid_zip_code(auth_client):
    customer = CustomerFactory()
    payload = {
        "customer": customer.pk,
        "street": "Rua Augusta",
        "number": "500",
        "neighborhood": "Consolacao",
        "city": "Sao Paulo",
        "state": "SP",
        "zip_code": "invalid",
    }
    response = auth_client.post(reverse("address-list"), payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "zip_code" in response.data


def test_create_address_rejects_invalid_state(auth_client):
    customer = CustomerFactory()
    payload = {
        "customer": customer.pk,
        "street": "Rua Augusta",
        "number": "500",
        "neighborhood": "Consolacao",
        "city": "Sao Paulo",
        "state": "S",
        "zip_code": "01305-000",
    }
    response = auth_client.post(reverse("address-list"), payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "state" in response.data


def test_update_address(auth_client):
    address = AddressFactory()
    response = auth_client.patch(reverse("address-detail", args=[address.pk]), {"city": "Campinas"})
    assert response.status_code == status.HTTP_200_OK


def test_delete_address(auth_client):
    address = AddressFactory()
    response = auth_client.delete(reverse("address-detail", args=[address.pk]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
