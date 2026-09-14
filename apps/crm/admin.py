from django.contrib import admin

from apps.crm.models import Address, Contact, Document, Observation, RelationshipHistory, Task


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["full_name", "role", "email", "phone", "is_primary", "customer", "company"]
    search_fields = ["full_name", "email"]
    list_filter = ["is_primary"]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["street", "city", "state", "address_type", "customer", "company"]
    search_fields = ["street", "city", "zip_code"]
    list_filter = ["address_type", "state"]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "document_type", "customer", "company", "created_at"]
    list_filter = ["document_type"]
    search_fields = ["title"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "priority", "due_date", "assigned_to", "customer", "company"]
    list_filter = ["status", "priority"]
    search_fields = ["title", "description"]


@admin.register(RelationshipHistory)
class RelationshipHistoryAdmin(admin.ModelAdmin):
    list_display = ["interaction_type", "occurred_at", "customer", "company"]
    list_filter = ["interaction_type"]
    search_fields = ["description"]


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ["content", "customer", "company", "created_at"]
    search_fields = ["content"]
