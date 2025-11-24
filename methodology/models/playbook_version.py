"""
PlaybookVersion model for tracking version history.

Each save of a playbook creates a new version entry.
Versions are integer-based (v1, v2, v3...).
"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PlaybookVersion(models.Model):
    """Tracks version history for playbooks."""
    
    playbook = models.ForeignKey('Playbook', on_delete=models.CASCADE, related_name='versions')
    version_number = models.IntegerField()
    snapshot_data = models.JSONField()
    change_summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-version_number']
        constraints = [
            models.UniqueConstraint(fields=['playbook', 'version_number'], name='unique_version_per_playbook')
        ]
    
    def __str__(self):
        return f"{self.playbook.name} v{self.version_number}"
