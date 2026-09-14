import pytest
from django.urls import reverse
from rest_framework import status

from apps.companies.models import Company
from apps.companies.tests.factories import CompanyFactory, generate_valid_cnpj

pytestmark = pytest.mark.django_db


def test_list_requires_authentication(api_client):
    response = api_client.get(reverse("company-list"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_company(auth_client):
    payload = {
        "trade_name": "Acme",
        "legal_name": "Acme Ltda",
        "cnpj": generate_valid_cnpj(555),
        "email": "acme@example.com",
        "phone": "1133334444",
    }
    response = auth_client.post(reverse("company-list"), payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert Company.objects.filter(email="acme@example.com").exists()


def test_create_company_rejects_invalid_cnpj(auth_client):
    payload = {
        "trade_name": "Acme",
        "legal_name": "Acme Ltda",
        "cnpj": "11111111111111",
        "email": "acme2@example.com",
        "phone": "1133334444",
    }
    response = auth_client.post(reverse("company-list"), payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "cnpj" in response.data


def test_create_company_rejects_duplicate_cnpj(auth_client):
    existing = CompanyFactory()
    payload = {
        "trade_name": "Duplicate",
        "legal_name": "Duplicate Ltda",
        "cnpj": existing.cnpj,
        "email": "duplicate@example.com",
        "phone": "1133334444",
    }
    response = auth_client.post(reverse("company-list"), payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_retrieve_company(auth_client):
    company = CompanyFactory()
    response = auth_client.get(reverse("company-detail", args=[company.pk]))
    assert response.status_code == status.HTTP_200_OK


def test_update_company(auth_client):
    company = CompanyFactory()
    response = auth_client.patch(reverse("company-detail", args=[company.pk]), {"industry": "Technology"})
    assert response.status_code == status.HTTP_200_OK
    company.refresh_from_db()
    assert company.industry == "Technology"


def test_delete_company(auth_client):
    company = CompanyFactory()
    response = auth_client.delete(reverse("company-detail", args=[company.pk]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Company.objects.filter(pk=company.pk).exists()


def test_filter_company_by_status(auth_client):
    CompanyFactory(status="ACTIVE")
    CompanyFactory(status="INACTIVE")
    response = auth_client.get(reverse("company-list"), {"status": "ACTIVE"})
    assert response.data["count"] == 1
