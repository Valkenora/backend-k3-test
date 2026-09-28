from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['entity_type', 'entity_id', 'action', 'performed_by', 'timestamp']
    list_filter = ['entity_type', 'action']
    readonly_fields = ['entity_type', 'entity_id', 'action', 'performed_by', 'timestamp', 'remarks']
    search_fields = ['entity_type', 'action']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False