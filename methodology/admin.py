"""Admin configuration for methodology models."""

from django.contrib import admin
from methodology.models import Playbook, PlaybookVersion, Workflow, Activity


@admin.register(Playbook)
class PlaybookAdmin(admin.ModelAdmin):
    """Admin configuration for Playbook model."""
    list_display = ('name', 'author', 'category', 'status', 'source', 'version', 'created_at')
    list_filter = ('status', 'category', 'source', 'visibility')
    search_fields = ('name', 'description', 'tags')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PlaybookVersion)
class PlaybookVersionAdmin(admin.ModelAdmin):
    """Admin configuration for PlaybookVersion model."""
    list_display = ('playbook', 'version_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('playbook__name', 'change_summary')
    readonly_fields = ('created_at',)


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    """Admin configuration for Workflow model."""
    list_display = ('name', 'playbook', 'order', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description', 'playbook__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('playbook', 'order')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin configuration for Activity model."""
    list_display = ('name', 'workflow', 'phase', 'order', 'has_dependencies')
    list_filter = ('phase', 'has_dependencies', 'created_at')
    search_fields = ('name', 'description', 'workflow__name', 'workflow__playbook__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('workflow', 'order')
    fieldsets = (
        ('Basic Information', {
            'fields': ('workflow', 'name', 'description')
        }),
        ('Organization', {
            'fields': ('order', 'phase', 'has_dependencies')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
