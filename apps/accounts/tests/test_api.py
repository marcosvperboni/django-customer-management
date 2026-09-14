import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status

from apps.accounts.models import User

pytestmark = pytest.mark.django_db


def test_register_creates_user(api_client):
    response = api_client.post(
        reverse("register"),
        {"email": "new@example.com", "password": "StrongPass123!", "first_name": "New"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email="new@example.com").exists()


def test_register_rejects_weak_password(api_client):
    response = api_client.post(reverse("register"), {"email": "weak@example.com", "password": "123"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_returns_jwt_pair(api_client, user):
    response = api_client.post(reverse("login"), {"email": user.email, "password": "StrongPass123!"})
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


def test_login_rejects_wrong_password(api_client, user):
    response = api_client.post(reverse("login"), {"email": user.email, "password": "wrong"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_returns_new_access_token(api_client, user):
    login = api_client.post(reverse("login"), {"email": user.email, "password": "StrongPass123!"})
    response = api_client.post(reverse("token-refresh"), {"refresh": login.data["refresh"]})
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data


def test_me_requires_authentication(api_client):
    response = api_client.get(reverse("me"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_me_returns_current_user(auth_client, user):
    response = auth_client.get(reverse("me"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user.email


def test_change_password_with_wrong_current_password(auth_client):
    response = auth_client.post(
        reverse("change-password"),
        {"current_password": "wrong", "new_password": "AnotherStrong123!"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_change_password_succeeds(auth_client, user):
    response = auth_client.post(
        reverse("change-password"),
        {"current_password": "StrongPass123!", "new_password": "AnotherStrong123!"},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    user.refresh_from_db()
    assert user.check_password("AnotherStrong123!")


def test_regular_user_cannot_create_users(auth_client):
    response = auth_client.post(reverse("user-list"), {"email": "blocked@example.com", "password": "x"})
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_staff_user_can_list_users(staff_client, user):
    response = staff_client.get(reverse("user-list"))
    assert response.status_code == status.HTTP_200_OK


def test_staff_user_can_create_group(staff_client):
    response = staff_client.post(reverse("group-list"), {"name": "Managers"})
    assert response.status_code == status.HTTP_201_CREATED
    assert Group.objects.filter(name="Managers").exists()


def test_authenticated_user_can_list_permissions(auth_client):
    response = auth_client.get(reverse("permission-list"))
    assert response.status_code == status.HTTP_200_OK


def test_user_delete_restricted_to_staff(auth_client, staff_user):
    response = auth_client.delete(reverse("user-detail", args=[staff_user.pk]))
    assert response.status_code == status.HTTP_403_FORBIDDEN
