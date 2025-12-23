"""URL configuration for artifact views."""

from django.urls import path
from methodology import artifact_views

# Artifact URLs
urlpatterns = [
    path('playbooks/<int:playbook_pk>/artifacts/create/', artifact_views.artifact_create, name='artifact_create'),
    path('artifacts/<int:pk>/', artifact_views.artifact_detail, name='artifact_detail'),
    path('artifacts/<int:pk>/edit/', artifact_views.artifact_edit, name='artifact_edit'),
]
