from django.contrib import admin
from .models import HIRADocument, HIRAGroup, HIRAActivity


class HIRAActivityInline(admin.TabularInline):
    model = HIRAActivity
    extra = 1
    readonly_fields = ['initial_score', 'initial_level', 'initial_acceptable',
                       'residual_score', 'residual_level', 'residual_acceptable']


class HIRAGroupInline(admin.StackedInline):
    model = HIRAGroup
    extra = 1


@admin.register(HIRADocument)
class HIRADocumentAdmin(admin.ModelAdmin):
    list_display = ['document_number', 'work_package', 'work_area', 'status', 'created_by', 'created_at']
    list_filter = ['status']
    search_fields = ['document_number', 'work_package']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [HIRAGroupInline]


@admin.register(HIRAGroup)
class HIRAGroupAdmin(admin.ModelAdmin):
    list_display = ['location_function', 'hira_document']
    inlines = [HIRAActivityInline]


@admin.register(HIRAActivity)
class HIRAActivityAdmin(admin.ModelAdmin):
    list_display = ['activity_name', 'activity_type', 'initial_score', 'initial_level',
                    'initial_acceptable', 'residual_score', 'residual_level', 'residual_acceptable']
    readonly_fields = ['initial_score', 'initial_level', 'initial_acceptable',
                       'residual_score', 'residual_level', 'residual_acceptable']