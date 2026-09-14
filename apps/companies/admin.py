from django.contrib import admin

from apps.companies.models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["trade_name", "legal_name", "cnpj", "email", "status", "created_at"]
    list_filter = ["status", "industry"]
    search_fields = ["trade_name", "legal_name", "cnpj", "email"]
