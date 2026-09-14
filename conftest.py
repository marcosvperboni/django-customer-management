import pytest
from rest_framework.test import APIClient

from apps.accounts.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(email="user@example.com", password="StrongPass123!")


@pytest.fixture
def staff_user(db):
    return User.objects.create_user(email="staff@example.com", password="StrongPass123!", is_staff=True)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def staff_client(api_client, staff_user):
    api_client.force_authenticate(user=staff_user)
    return api_client
