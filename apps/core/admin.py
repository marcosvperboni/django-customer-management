from django.contrib import admin

from apps.core.models import AuditLogEntry


@admin.register(AuditLogEntry)
class AuditLogEntryAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "user", "action", "model_label", "object_id", "object_repr")
    list_filter = ("action", "model_label")
    search_fields = ("object_repr", "object_id")
    readonly_fields = [f.name for f in AuditLogEntry._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
