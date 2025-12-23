"""
Artifact views for CRUD operations.

Provides views for creating, viewing, and editing artifacts within playbooks.
"""

import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError

from methodology.models import Playbook, Activity, Artifact
from methodology.services.artifact_service import ArtifactService

logger = logging.getLogger(__name__)


# ==================== CREATE ====================


@login_required
def artifact_create(request, playbook_pk):
    """
    Create new artifact for playbook.

    GET: Display create form
    POST: Validate and create artifact, redirect to playbook detail

    Template: artifacts/create.html
    Template Context:
        - playbook: Playbook instance
        - activities: QuerySet of Activity instances for producer selection
        - artifact_types: List of type choices
        - form_data: Dict with form values (on validation error)
        - errors: Dict with field errors (on validation error)

    :param request: Django request object
    :param playbook_pk: Playbook primary key
    :return: Rendered form template or redirect
    :raises Http404: If playbook not found
    """
    logger.info(
        f"User {request.user.username} accessing artifact create for playbook {playbook_pk}"
    )

    # Get playbook with permission check
    playbook = get_object_or_404(Playbook, pk=playbook_pk)

    # Check edit permission
    if not playbook.is_owned_by(request.user):
        logger.warning(
            f"User {request.user.username} attempted to create artifact without permission"
        )
        messages.error(
            request, "You don't have permission to add artifacts to this playbook."
        )
        return redirect("playbook_detail", pk=playbook_pk)

    if request.method == "POST":
        # Extract form data
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        artifact_type = request.POST.get("type", "Document").strip()
        is_required = request.POST.get("is_required") == "on"
        produced_by_id = request.POST.get("produced_by", "").strip()
        template_file = request.FILES.get("template_file")

        # Get producer activity
        if not produced_by_id:
            messages.error(request, "Producer activity is required.")
            return _render_create_form(request, playbook, request.POST, {})

        try:
            produced_by = Activity.objects.select_related("workflow").get(
                pk=int(produced_by_id), workflow__playbook=playbook
            )
        except (Activity.DoesNotExist, ValueError):
            messages.error(request, "Invalid producer activity selected.")
            return _render_create_form(request, playbook, request.POST, {})

        # Validate and create
        try:
            artifact = ArtifactService.create_artifact(
                playbook=playbook,
                produced_by=produced_by,
                name=name,
                description=description,
                type=artifact_type,
                is_required=is_required,
                template_file=template_file,
            )
            logger.info(
                f"Artifact '{name}' created successfully in playbook {playbook_pk}"
            )
            messages.success(
                request, f"Artifact '{artifact.name}' created successfully!"
            )
            return redirect("playbook_detail", pk=playbook_pk)

        except ValidationError as e:
            logger.warning(f"Artifact creation validation error: {str(e)}")
            messages.error(request, str(e))
            return _render_create_form(request, playbook, request.POST, {})

    # GET request - show form
    return _render_create_form(request, playbook, {}, {})


def _render_create_form(request, playbook, form_data, errors):
    """Helper to render create form with context."""
    # Get all activities in playbook for producer selection
    # Use select_related to avoid N+1 queries
    activities = (
        Activity.objects.filter(workflow__playbook=playbook)
        .select_related("workflow")
        .order_by("workflow__order", "order")
    )

    context = {
        "playbook": playbook,
        "activities": activities,
        "artifact_types": Artifact.ARTIFACT_TYPES,
        "form_data": form_data,
        "errors": errors,
    }
    return render(request, "artifacts/create.html", context)


# ==================== VIEW ====================


@login_required
def artifact_detail(request, pk):
    """
    Display artifact details.

    Displays full artifact information including name, description, type,
    producer activity, consumer activities, and template file.

    Template: artifacts/detail.html
    Template Context:
        - artifact: Artifact instance
        - playbook: Playbook instance
        - producer: Activity instance (artifact.produced_by)
        - consumers: QuerySet of ArtifactInput instances
        - can_edit: Boolean indicating if user can edit

    :param request: Django request object
    :param pk: Artifact primary key
    :return: Rendered detail template
    :raises Http404: If artifact not found
    """
    logger.info(f"User {request.user.username} viewing artifact {pk}")

    # Get artifact with related objects
    artifact = get_object_or_404(
        Artifact.objects.select_related(
            "produced_by", "produced_by__workflow", "playbook"
        ).prefetch_related("inputs__activity", "inputs__activity__workflow"),
        pk=pk,
    )

    # Check if user has access
    if artifact.playbook.source == "owned" and artifact.playbook.author != request.user:
        logger.warning(
            f"User {request.user.username} attempted to access artifact {pk} they don't own"
        )
        messages.error(request, "You don't have permission to view this artifact.")
        return redirect("playbook_list")

    # Get consumers
    consumers = ArtifactService.get_artifact_consumers(artifact)

    context = {
        "artifact": artifact,
        "playbook": artifact.playbook,
        "producer": artifact.produced_by,
        "consumers": consumers,
        "can_edit": artifact.playbook.is_owned_by(request.user),
    }

    logger.info(f"Artifact detail rendered for user {request.user.username}")
    return render(request, "artifacts/detail.html", context)


# ==================== EDIT ====================


@login_required
def artifact_edit(request, pk):
    """
    Edit existing artifact.

    GET: Display edit form with current values
    POST: Validate and update artifact, redirect to detail

    Template: artifacts/edit.html
    Template Context:
        - artifact: Artifact instance
        - playbook: Playbook instance
        - activities: QuerySet of Activity instances
        - artifact_types: List of type choices
        - form_data: Dict with form values (on validation error)
        - errors: Dict with field errors (on validation error)

    :param request: Django request object
    :param pk: Artifact primary key
    :return: Rendered form template or redirect
    :raises Http404: If artifact not found
    """
    logger.info(f"User {request.user.username} accessing artifact edit for {pk}")

    # Get artifact with permission check
    artifact = get_object_or_404(
        Artifact.objects.select_related("produced_by", "playbook"), pk=pk
    )

    # Check edit permission
    if not artifact.playbook.is_owned_by(request.user):
        logger.warning(
            f"User {request.user.username} attempted to edit artifact without permission"
        )
        messages.error(request, "You don't have permission to edit this artifact.")
        return redirect("artifact_detail", pk=pk)

    if request.method == "POST":
        # Extract form data
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        artifact_type = request.POST.get("type", "Document").strip()
        is_required = request.POST.get("is_required") == "on"
        produced_by_id = request.POST.get("produced_by", "").strip()
        template_file = request.FILES.get("template_file")

        # Prepare update data
        update_data = {
            "name": name,
            "description": description,
            "type": artifact_type,
            "is_required": is_required,
        }

        # Handle producer change
        if produced_by_id:
            try:
                produced_by = Activity.objects.get(
                    pk=int(produced_by_id), workflow__playbook=artifact.playbook
                )
                update_data["produced_by"] = produced_by
            except (Activity.DoesNotExist, ValueError):
                messages.error(request, "Invalid producer activity selected.")
                return _render_edit_form(request, artifact, request.POST, {})

        # Handle template file
        if template_file:
            update_data["template_file"] = template_file

        # Validate and update
        try:
            artifact = ArtifactService.update_artifact(pk, **update_data)
            logger.info(f"Artifact '{name}' updated successfully")
            messages.success(
                request, f"Artifact '{artifact.name}' updated successfully!"
            )
            return redirect("artifact_detail", pk=pk)

        except ValidationError as e:
            logger.warning(f"Artifact update validation error: {str(e)}")
            messages.error(request, str(e))
            return _render_edit_form(request, artifact, request.POST, {})

    # GET request - show form with current values
    form_data = {
        "name": artifact.name,
        "description": artifact.description,
        "type": artifact.type,
        "is_required": artifact.is_required,
        "produced_by": artifact.produced_by_id,
    }
    return _render_edit_form(request, artifact, form_data, {})


def _render_edit_form(request, artifact, form_data, errors):
    """Helper to render edit form with context."""
    # Get all activities in playbook for producer selection
    activities = (
        Activity.objects.filter(workflow__playbook=artifact.playbook)
        .select_related("workflow")
        .order_by("workflow__order", "order")
    )

    context = {
        "artifact": artifact,
        "playbook": artifact.playbook,
        "activities": activities,
        "artifact_types": Artifact.ARTIFACT_TYPES,
        "form_data": form_data,
        "errors": errors,
    }
    return render(request, "artifacts/edit.html", context)
