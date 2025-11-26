"""Admin configuration for methodology models."""
from django.contrib import admin
from .models import Playbook, Workflow


@admin.register(Playbook)
class PlaybookAdmin(admin.ModelAdmin):
    """Admin interface for Playbook model."""
    
    list_display = [
        'name', 'created_by', 'category', 'status', 
        'visibility', 'version', 'updated_at'
    ]
    list_filter = [
        'category', 'status', 'visibility', 'created_by'
    ]
    search_fields = ['name', 'description']
    readonly_fields = ['version', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category')
        }),
        ('Metadata', {
            'fields': ('tags', 'visibility', 'status', 'version')
        }),
        ('Timestamps', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Make created_by readonly for existing objects."""
        if obj:  # Editing existing object
            return self.readonly_fields + ['created_by']
        return self.readonly_fields
    
    def save_model(self, request, obj, form, change):
        """Set created_by on creation."""
        if not change:  # Creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    """Admin interface for Workflow model."""
    
    list_display = [
        'name', 'playbook', 'status', 'order', 'created_by', 'created_at'
    ]
    list_filter = [
        'status', 'created_at', 'playbook'
    ]
    search_fields = ['name', 'description', 'playbook__name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'playbook')
        }),
        ('Settings', {
            'fields': ('status', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Make created_by readonly for existing objects."""
        if obj:  # Editing existing object
            return self.readonly_fields + ['created_by']
        return self.readonly_fields
    
    def save_model(self, request, obj, form, change):
        """Set created_by on creation."""
        if not change:  # Creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
