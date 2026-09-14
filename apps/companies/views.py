from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.companies.models import Company
from apps.companies.serializers import CompanySerializer
from apps.core.mixins import AuditLoggingMixin


class CompanyViewSet(AuditLoggingMixin, viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["status", "industry"]
    search_fields = ["trade_name", "legal_name", "cnpj", "email"]
    ordering_fields = ["trade_name", "created_at"]
