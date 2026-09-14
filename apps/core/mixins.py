from __future__ import annotations

from typing import Any

from rest_framework.serializers import ValidationError

from apps.core.models import AuditAction, AuditLogEntry


def _json_safe(value: Any) -> Any:
    if isinstance(value, str | int | float | bool) or value is None:
        return value
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, list | tuple | set):
        return [_json_safe(item) for item in value]
    return str(value)


class AuditLoggingMixin:
    """Writes an AuditLogEntry for every create/update/destroy performed via the API."""

    def _log(self, action: str, instance) -> None:
        user = self.request.user if self.request.user.is_authenticated else None
        AuditLogEntry.objects.create(
            user=user,
            action=action,
            model_label=instance._meta.label_lower,
            object_id=str(instance.pk),
            object_repr=str(instance)[:255],
            changes=_json_safe(getattr(self, "_pending_changes", {})),
        )

    def perform_create(self, serializer):
        self._pending_changes = dict(serializer.validated_data)
        instance = serializer.save()
        self._log(AuditAction.CREATE, instance)

    def perform_update(self, serializer):
        self._pending_changes = dict(serializer.validated_data)
        instance = serializer.save()
        self._log(AuditAction.UPDATE, instance)

    def perform_destroy(self, instance):
        pk, repr_ = instance.pk, str(instance)
        super().perform_destroy(instance)
        user = self.request.user if self.request.user.is_authenticated else None
        AuditLogEntry.objects.create(
            user=user,
            action=AuditAction.DELETE,
            model_label=instance._meta.label_lower,
            object_id=str(pk),
            object_repr=repr_[:255],
        )


class ExactlyOnePartyValidatorMixin:
    """Ensures a record is linked to exactly one of `customer` or `company`."""

    def validate(self, attrs):
        attrs = super().validate(attrs)
        customer = attrs.get("customer", getattr(self.instance, "customer", None))
        company = attrs.get("company", getattr(self.instance, "company", None))
        if bool(customer) == bool(company):
            raise ValidationError("Exactly one of 'customer' or 'company' must be set.")
        return attrs
