from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.core.mixins import AuditLoggingMixin
from apps.customers.models import Customer
from apps.customers.serializers import CustomerSerializer


class CustomerViewSet(AuditLoggingMixin, viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["status"]
    search_fields = ["full_name", "document", "email"]
    ordering_fields = ["full_name", "created_at"]
