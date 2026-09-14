import pytest
from django.urls import reverse
from rest_framework import status

from apps.customers.models import Customer
from apps.customers.tests.factories import CustomerFactory, generate_valid_cpf

pytestmark = pytest.mark.django_db


def test_list_requires_authentication(api_client):
    response = api_client.get(reverse("customer-list"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_customers(auth_client):
    CustomerFactory.create_batch(3)
    response = auth_client.get(reverse("customer-list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 3


def test_create_customer(auth_client):
    payload = {
        "full_name": "Jane Doe",
        "document": generate_valid_cpf(999),
        "email": "jane@example.com",
        "phone": "11988887777",
    }
    response = auth_client.post(reverse("customer-list"), payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert Customer.objects.filter(email="jane@example.com").exists()


def test_create_customer_rejects_invalid_cpf(auth_client):
    payload = {
        "full_name": "Jane Doe",
        "document": "11111111111",
        "email": "jane2@example.com",
        "phone": "11988887777",
    }
    response = auth_client.post(reverse("customer-list"), payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "document" in response.data


def test_create_customer_rejects_duplicate_email(auth_client):
    existing = CustomerFactory()
    payload = {
        "full_name": "Another Person",
        "document": generate_valid_cpf(1000),
        "email": existing.email,
        "phone": "11988887777",
    }
    response = auth_client.post(reverse("customer-list"), payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_customer_rejects_future_birth_date(auth_client):
    payload = {
        "full_name": "Time Traveler",
        "document": generate_valid_cpf(1001),
        "email": "traveler@example.com",
        "phone": "11988887777",
        "birth_date": "2999-01-01",
    }
    response = auth_client.post(reverse("customer-list"), payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "birth_date" in response.data


def test_retrieve_customer(auth_client):
    customer = CustomerFactory()
    response = auth_client.get(reverse("customer-detail", args=[customer.pk]))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["full_name"] == customer.full_name


def test_retrieve_missing_customer_returns_404(auth_client):
    response = auth_client.get(reverse("customer-detail", args=[999999]))
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_customer(auth_client):
    customer = CustomerFactory()
    response = auth_client.patch(
        reverse("customer-detail", args=[customer.pk]), {"full_name": "Updated Name"}
    )
    assert response.status_code == status.HTTP_200_OK
    customer.refresh_from_db()
    assert customer.full_name == "Updated Name"


def test_full_update_customer(auth_client):
    customer = CustomerFactory()
    payload = {
        "full_name": "Replaced Name",
        "document": customer.document,
        "email": customer.email,
        "phone": "11977776666",
    }
    response = auth_client.put(reverse("customer-detail", args=[customer.pk]), payload)
    assert response.status_code == status.HTTP_200_OK
    customer.refresh_from_db()
    assert customer.phone == "11977776666"


def test_delete_customer(auth_client):
    customer = CustomerFactory()
    response = auth_client.delete(reverse("customer-detail", args=[customer.pk]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Customer.objects.filter(pk=customer.pk).exists()


def test_filter_customers_by_status(auth_client):
    CustomerFactory(status="ACTIVE")
    CustomerFactory(status="INACTIVE")
    response = auth_client.get(reverse("customer-list"), {"status": "ACTIVE"})
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1


def test_search_customers_by_name(auth_client):
    CustomerFactory(full_name="Alice Wonderland")
    CustomerFactory(full_name="Bob Builder")
    response = auth_client.get(reverse("customer-list"), {"search": "Alice"})
    assert response.data["count"] == 1
