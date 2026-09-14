from __future__ import annotations

from django.conf import settings
from django.db import models
from django.db.models import Q

from apps.companies.models import Company
from apps.core.models import TimeStampedModel
from apps.core.validators import validate_phone, validate_zip_code
from apps.customers.models import Customer


class PartyLinkedModel(TimeStampedModel):
    """Abstract base for records that belong to exactly one Customer or Company."""

    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE, related_name="+")
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE, related_name="+")

    class Meta:
        abstract = True

    @property
    def party(self) -> Customer | Company | None:
        return self.customer or self.company

    def __str__(self) -> str:
        return f"{self._meta.verbose_name} for {self.party}"


def exactly_one_party_constraint(*, name: str) -> models.CheckConstraint:
    return models.CheckConstraint(
        condition=(Q(customer__isnull=False) & Q(company__isnull=True))
        | (Q(customer__isnull=True) & Q(company__isnull=False)),
        name=name,
    )


class Contact(PartyLinkedModel):
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=16, validators=[validate_phone])
    is_primary = models.BooleanField(default=False)

    class Meta:
        constraints = [exactly_one_party_constraint(name="contact_exactly_one_party")]
        ordering = ["full_name"]

    def __str__(self) -> str:
        return self.full_name


class AddressType(models.TextChoices):
    MAIN = "MAIN", "Main"
    BILLING = "BILLING", "Billing"
    SHIPPING = "SHIPPING", "Shipping"


class Address(PartyLinkedModel):
    address_type = models.CharField(max_length=16, choices=AddressType.choices, default=AddressType.MAIN)
    street = models.CharField(max_length=200)
    number = models.CharField(max_length=20)
    complement = models.CharField(max_length=100, blank=True)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=9, validators=[validate_zip_code])
    country = models.CharField(max_length=60, default="Brazil")

    class Meta:
        constraints = [exactly_one_party_constraint(name="address_exactly_one_party")]
        verbose_name_plural = "addresses"

    def __str__(self) -> str:
        return f"{self.street}, {self.number} - {self.city}/{self.state}"


class DocumentType(models.TextChoices):
    CONTRACT = "CONTRACT", "Contract"
    ID = "ID", "Identification"
    PROOF_OF_ADDRESS = "PROOF_OF_ADDRESS", "Proof of address"
    OTHER = "OTHER", "Other"


def document_upload_path(instance: Document, filename: str) -> str:
    return f"documents/{instance.party.pk}/{filename}"


class Document(PartyLinkedModel):
    title = models.CharField(max_length=150)
    document_type = models.CharField(max_length=20, choices=DocumentType.choices, default=DocumentType.OTHER)
    file = models.FileField(upload_to=document_upload_path)

    class Meta:
        constraints = [exactly_one_party_constraint(name="document_exactly_one_party")]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


class TaskStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    IN_PROGRESS = "IN_PROGRESS", "In progress"
    DONE = "DONE", "Done"
    CANCELLED = "CANCELLED", "Cancelled"


class TaskPriority(models.TextChoices):
    LOW = "LOW", "Low"
    MEDIUM = "MEDIUM", "Medium"
    HIGH = "HIGH", "High"


class Task(PartyLinkedModel):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.CharField(max_length=16, choices=TaskStatus.choices, default=TaskStatus.PENDING)
    priority = models.CharField(max_length=16, choices=TaskPriority.choices, default=TaskPriority.MEDIUM)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_tasks",
    )

    class Meta:
        constraints = [exactly_one_party_constraint(name="task_exactly_one_party")]
        ordering = ["due_date"]

    def __str__(self) -> str:
        return self.title


class InteractionType(models.TextChoices):
    CALL = "CALL", "Call"
    EMAIL = "EMAIL", "Email"
    MEETING = "MEETING", "Meeting"
    NOTE = "NOTE", "Note"
    STATUS_CHANGE = "STATUS_CHANGE", "Status change"


class RelationshipHistory(PartyLinkedModel):
    interaction_type = models.CharField(max_length=16, choices=InteractionType.choices)
    description = models.TextField()
    occurred_at = models.DateTimeField()

    class Meta:
        constraints = [exactly_one_party_constraint(name="history_exactly_one_party")]
        ordering = ["-occurred_at"]
        verbose_name_plural = "relationship history entries"

    def __str__(self) -> str:
        return f"{self.interaction_type} - {self.occurred_at:%Y-%m-%d}"


class Observation(PartyLinkedModel):
    content = models.TextField()

    class Meta:
        constraints = [exactly_one_party_constraint(name="observation_exactly_one_party")]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.content[:50]
