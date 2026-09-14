from django.contrib import admin

from apps.customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["full_name", "document", "email", "phone", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["full_name", "document", "email"]
