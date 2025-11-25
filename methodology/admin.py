"""Admin configuration for methodology models."""

from django.contrib import admin
from methodology.models.activity import Activity
from methodology.models.playbook import Playbook


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin configuration for Activity model."""
    
    list_display = [
        'user', 
        'action_type', 
        'playbook', 
        'description', 
        'timestamp'
    ]
    list_filter = [
        'action_type', 
        'timestamp', 
        'user'
    ]
    search_fields = [
        'user__username', 
        'description', 
        'action_type'
    ]
    readonly_fields = [
        'timestamp'
    ]
    ordering = [
        '-timestamp'
    ]
    
    fieldsets = (
        ('Activity Information', {
            'fields': ('user', 'action_type', 'description', 'timestamp')
        }),
        ('Related Objects', {
            'fields': ('playbook',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queries with select_related."""
        return super().get_queryset(request).select_related('user', 'playbook')


# Register Playbook if not already registered
@admin.register(Playbook)
class PlaybookAdmin(admin.ModelAdmin):
    """Admin configuration for Playbook model."""
    
    list_display = [
        'name', 
        'author', 
        'category', 
        'status', 
        'version', 
        'updated_at'
    ]
    list_filter = [
        'category', 
        'status', 
        'source', 
        'visibility'
    ]
    search_fields = [
        'name', 
        'description', 
        'author__username'
    ]
    readonly_fields = [
        'created_at', 
        'updated_at'
    ]
    ordering = [
        '-updated_at'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'tags')
        }),
        ('Status & Visibility', {
            'fields': ('status', 'visibility', 'source', 'version')
        }),
        ('Ownership', {
            'fields': ('author',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )