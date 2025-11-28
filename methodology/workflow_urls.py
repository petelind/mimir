"""URL patterns for workflow operations."""

from django.urls import path
from methodology import workflow_views

urlpatterns = [
    # Scoped to playbook
    path('<int:playbook_pk>/workflows/', workflow_views.workflow_list, name='workflow_list'),
    path('<int:playbook_pk>/workflows/create/', workflow_views.workflow_create, name='workflow_create'),
    path('<int:playbook_pk>/workflows/<int:pk>/', workflow_views.workflow_detail, name='workflow_detail'),
    path('<int:playbook_pk>/workflows/<int:pk>/edit/', workflow_views.workflow_edit, name='workflow_edit'),
    path('<int:playbook_pk>/workflows/<int:pk>/delete/', workflow_views.workflow_delete, name='workflow_delete'),
    path('<int:playbook_pk>/workflows/<int:pk>/duplicate/', workflow_views.workflow_duplicate, name='workflow_duplicate'),
]
