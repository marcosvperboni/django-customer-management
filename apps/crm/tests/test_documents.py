import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status

from apps.crm.tests.factories import DocumentFactory
from apps.customers.tests.factories import CustomerFactory

pytestmark = pytest.mark.django_db


def _upload(name="contract.pdf", size=1024):
    return SimpleUploadedFile(name, b"x" * size, content_type="application/pdf")


def test_create_document(auth_client):
    customer = CustomerFactory()
    payload = {
        "customer": customer.pk,
        "title": "Signed contract",
        "document_type": "CONTRACT",
        "file": _upload(),
    }
    response = auth_client.post(reverse("document-list"), payload, format="multipart")
    assert response.status_code == status.HTTP_201_CREATED


def test_create_document_rejects_oversized_file(auth_client):
    customer = CustomerFactory()
    payload = {
        "customer": customer.pk,
        "title": "Huge file",
        "file": _upload(size=11 * 1024 * 1024),
    }
    response = auth_client.post(reverse("document-list"), payload, format="multipart")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "file" in response.data


def test_delete_document(auth_client):
    document = DocumentFactory(file=_upload())
    response = auth_client.delete(reverse("document-detail", args=[document.pk]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
