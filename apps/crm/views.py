from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.core.mixins import AuditLoggingMixin
from apps.crm.models import Address, Contact, Document, Observation, RelationshipHistory, Task
from apps.crm.serializers import (
    AddressSerializer,
    ContactSerializer,
    DocumentSerializer,
    ObservationSerializer,
    RelationshipHistorySerializer,
    TaskSerializer,
)


class ContactViewSet(AuditLoggingMixin, viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["customer", "company", "is_primary"]
    search_fields = ["full_name", "email"]
    ordering_fields = ["full_name", "created_at"]


class AddressViewSet(AuditLoggingMixin, viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["customer", "company", "address_type", "city", "state"]
    search_fields = ["street", "city", "zip_code"]
    ordering_fields = ["created_at"]


class DocumentViewSet(AuditLoggingMixin, viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["customer", "company", "document_type"]
    search_fields = ["title"]
    ordering_fields = ["created_at"]


class TaskViewSet(AuditLoggingMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["customer", "company", "status", "priority", "assigned_to"]
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "created_at"]


class RelationshipHistoryViewSet(AuditLoggingMixin, viewsets.ModelViewSet):
    queryset = RelationshipHistory.objects.all()
    serializer_class = RelationshipHistorySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["customer", "company", "interaction_type"]
    search_fields = ["description"]
    ordering_fields = ["occurred_at"]


class ObservationViewSet(AuditLoggingMixin, viewsets.ModelViewSet):
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["customer", "company"]
    search_fields = ["content"]
    ordering_fields = ["created_at"]
