from datetime import date

from rest_framework import serializers

from apps.core.mixins import ExactlyOnePartyValidatorMixin
from apps.crm.models import Address, Contact, Document, Observation, RelationshipHistory, Task


class ContactSerializer(ExactlyOnePartyValidatorMixin, serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "id",
            "customer",
            "company",
            "full_name",
            "role",
            "email",
            "phone",
            "is_primary",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class AddressSerializer(ExactlyOnePartyValidatorMixin, serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "customer",
            "company",
            "address_type",
            "street",
            "number",
            "complement",
            "neighborhood",
            "city",
            "state",
            "zip_code",
            "country",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_state(self, value):
        if len(value) != 2 or not value.isalpha():
            raise serializers.ValidationError("State must be a 2-letter code, e.g. 'SP'.")
        return value.upper()


MAX_DOCUMENT_SIZE_BYTES = 10 * 1024 * 1024


class DocumentSerializer(ExactlyOnePartyValidatorMixin, serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "id",
            "customer",
            "company",
            "title",
            "document_type",
            "file",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_file(self, value):
        if value.size > MAX_DOCUMENT_SIZE_BYTES:
            raise serializers.ValidationError("File size must not exceed 10MB.")
        return value


class TaskSerializer(ExactlyOnePartyValidatorMixin, serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "customer",
            "company",
            "title",
            "description",
            "due_date",
            "status",
            "priority",
            "assigned_to",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_due_date(self, value):
        if self.instance is None and value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past for a new task.")
        return value


class RelationshipHistorySerializer(ExactlyOnePartyValidatorMixin, serializers.ModelSerializer):
    class Meta:
        model = RelationshipHistory
        fields = [
            "id",
            "customer",
            "company",
            "interaction_type",
            "description",
            "occurred_at",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class ObservationSerializer(ExactlyOnePartyValidatorMixin, serializers.ModelSerializer):
    class Meta:
        model = Observation
        fields = ["id", "customer", "company", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
