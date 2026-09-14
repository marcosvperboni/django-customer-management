from datetime import date

from rest_framework import serializers

from apps.customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "full_name",
            "document",
            "email",
            "phone",
            "birth_date",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_birth_date(self, value):
        if value and value > date.today():
            raise serializers.ValidationError("Birth date cannot be in the future.")
        return value
