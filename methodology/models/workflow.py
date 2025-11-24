"""
Workflow model stub for playbook creation.

Minimal implementation to support playbook wizard Step 2.
Full workflow functionality will be implemented in Act 3.
"""

from django.db import models


class Workflow(models.Model):
    """Workflow stub for playbook creation."""
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    playbook = models.ForeignKey('Playbook', on_delete=models.CASCADE, related_name='workflows')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return self.name
