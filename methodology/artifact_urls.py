"""URL configuration for artifact views."""

from django.urls import path
from methodology import artifact_views

urlpatterns = [
    # List view for artifacts in a playbook
    path('playbooks/<int:playbook_id>/artifacts/', artifact_views.artifact_list, name='artifact_list'),
    
    # Delete artifact
    path('artifacts/<int:pk>/delete/', artifact_views.artifact_delete, name='artifact_delete'),
]
