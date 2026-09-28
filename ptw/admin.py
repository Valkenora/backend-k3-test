from django.contrib import admin
from .models import WorkPermit


@admin.register(WorkPermit)
class WorkPermitAdmin(admin.ModelAdmin):
    list_display = [
        'permit_type', 'work_location', 'work_description',
        'status', 'submitted_by', 'created_at'
    ]
    list_filter = ['permit_type', 'status']
    search_fields = ['work_location', 'work_description', 'person_in_charge']
    readonly_fields = [
        'submitted_at', 'endorsed_at', 'approved_at',
        'retracted_at', 'closed_at', 'created_at', 'updated_at'
    ]