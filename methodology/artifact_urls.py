"""URL configuration for artifact views."""

from django.urls import path
from methodology import artifact_views

# Artifact URLs
urlpatterns = [
    path(
        "playbooks/<int:playbook_pk>/artifacts/create/",
        artifact_views.artifact_create,
        name="artifact_create",
    ),
    path(
        "playbooks/<int:playbook_id>/artifacts/",
        artifact_views.artifact_list,
        name="artifact_list",
    ),
    path("artifacts/<int:pk>/", artifact_views.artifact_detail, name="artifact_detail"),
    path(
        "artifacts/<int:pk>/edit/", artifact_views.artifact_edit, name="artifact_edit"
    ),
    path(
        "artifacts/<int:pk>/delete/",
        artifact_views.artifact_delete,
        name="artifact_delete",
    ),
    # Flow management URLs
    path(
        "activities/<int:activity_id>/manage-inputs/",
        artifact_views.activity_manage_inputs,
        name="activity_manage_inputs",
    ),
    path(
        "artifacts/<int:artifact_id>/add-consumer/",
        artifact_views.artifact_add_consumer,
        name="artifact_add_consumer",
    ),
    path(
        "artifacts/<int:artifact_id>/remove-consumer/<int:input_id>/",
        artifact_views.artifact_remove_consumer,
        name="artifact_remove_consumer",
    ),
    path(
        "artifact-inputs/<int:input_id>/toggle-required/",
        artifact_views.artifact_toggle_input_required,
        name="artifact_toggle_input_required",
    ),
    path(
        "playbooks/<int:playbook_id>/artifacts/flow-diagram/",
        artifact_views.artifact_flow_diagram,
        name="artifact_flow_diagram",
    ),
    path(
        "activities/<int:activity_id>/bulk-add-inputs/",
        artifact_views.activity_bulk_add_inputs,
        name="activity_bulk_add_inputs",
    ),
    path(
        "activities/<int:activity_id>/copy-inputs/",
        artifact_views.activity_copy_inputs,
        name="activity_copy_inputs",
    ),
]
