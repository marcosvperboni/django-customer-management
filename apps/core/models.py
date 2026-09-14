from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.validators import validate_phone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        abstract = True


class PartyStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    PROSPECT = "PROSPECT", "Prospect"


class PartyModel(TimeStampedModel):
    """Shared identity/contact fields for Customer and Company aggregates."""

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16, validators=[validate_phone])
    status = models.CharField(max_length=16, choices=PartyStatus.choices, default=PartyStatus.ACTIVE)

    class Meta:
        abstract = True


class AuditAction(models.TextChoices):
    CREATE = "CREATE", "Create"
    UPDATE = "UPDATE", "Update"
    DELETE = "DELETE", "Delete"


class AuditLogEntry(models.Model):
    """Immutable trail of write operations performed through the API."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="audit_entries"
    )
    action = models.CharField(max_length=8, choices=AuditAction.choices)
    model_label = models.CharField(max_length=100)
    object_id = models.CharField(max_length=64)
    object_repr = models.CharField(max_length=255)
    changes = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [models.Index(fields=["model_label", "object_id"])]

    def __str__(self) -> str:
        return f"{self.action} {self.model_label}#{self.object_id} by {self.user_id}"
