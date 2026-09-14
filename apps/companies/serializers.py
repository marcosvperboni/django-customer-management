from rest_framework import serializers

from apps.companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "trade_name",
            "legal_name",
            "cnpj",
            "email",
            "phone",
            "industry",
            "website",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
