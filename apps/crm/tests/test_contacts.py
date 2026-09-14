import pytest
from django.urls import reverse
from rest_framework import status

from apps.companies.tests.factories import CompanyFactory
from apps.crm.models import Contact
from apps.crm.tests.factories import ContactFactory
from apps.customers.tests.factories import CustomerFactory

pytestmark = pytest.mark.django_db


def test_list_requires_authentication(api_client):
    response = api_client.get(reverse("contact-list"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_contact_for_customer(auth_client):
    customer = CustomerFactory()
    payload = {
        "customer": customer.pk,
        "full_name": "Contact Person",
        "email": "contact@example.com",
        "phone": "11988887777",
    }
    response = auth_client.post(reverse("contact-list"), payload)
    assert response.status_code == status.HTTP_201_CREATED


def test_create_contact_for_company(auth_client):
    company = CompanyFactory()
    payload = {
        "company": company.pk,
        "full_name": "Contact Person",
        "phone": "11988887777",
    }
    response = auth_client.post(reverse("contact-list"), payload)
    assert response.status_code == status.HTTP_201_CREATED


def test_create_contact_without_party_fails(auth_client):
    payload = {"full_name": "Nobody", "phone": "11988887777"}
    response = auth_client.post(reverse("contact-list"), payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_contact_with_both_parties_fails(auth_client):
    customer = CustomerFactory()
    company = CompanyFactory()
    payload = {
        "customer": customer.pk,
        "company": company.pk,
        "full_name": "Nobody",
        "phone": "11988887777",
    }
    response = auth_client.post(reverse("contact-list"), payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_contact(auth_client):
    contact = ContactFactory()
    response = auth_client.patch(reverse("contact-detail", args=[contact.pk]), {"role": "CFO"})
    assert response.status_code == status.HTTP_200_OK
    contact.refresh_from_db()
    assert contact.role == "CFO"


def test_delete_contact(auth_client):
    contact = ContactFactory()
    response = auth_client.delete(reverse("contact-detail", args=[contact.pk]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Contact.objects.filter(pk=contact.pk).exists()


def test_filter_contacts_by_customer(auth_client):
    customer = CustomerFactory()
    ContactFactory(customer=customer)
    ContactFactory()
    response = auth_client.get(reverse("contact-list"), {"customer": customer.pk})
    assert response.data["count"] == 1
