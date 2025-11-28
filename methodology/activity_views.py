"""
Activity views for CRUDV operations.

Provides list, create, view, edit, and delete operations for activities
within workflows.
"""

import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError

from methodology.models import Playbook, Workflow, Activity
from methodology.services.activity_service import ActivityService

logger = logging.getLogger(__name__)


# ==================== LIST ====================

@login_required
def activity_list(request, playbook_pk, workflow_pk):
    """
    List all activities in a workflow.
    
    Displays activities grouped by phase if phases exist, otherwise shows
    flat list ordered by sequence. Includes permission checks and activity
    count statistics.
    
    Template: activities/list.html
    Template Context:
        - playbook: Playbook instance
        - workflow: Workflow instance
        - activities_by_phase: Dict of phase -> activities list
        - has_phases: Boolean indicating if any activities have phases
        - total_activities: Count of all activities
        - can_edit: Boolean indicating if user can create/edit activities
    
    :param request: Django request object
    :param playbook_pk: Playbook primary key
    :param workflow_pk: Workflow primary key
    :return: Rendered list template
    :raises Http404: If playbook or workflow not found
    """
    logger.info(f"User {request.user.username} accessing activity list for workflow {workflow_pk}")
    
    # Get workflow and playbook with permission check
    playbook = get_object_or_404(Playbook, pk=playbook_pk)
    workflow = get_object_or_404(Workflow, pk=workflow_pk, playbook=playbook)
    
    # Check if user has access to this playbook
    if playbook.source == 'owned' and playbook.author != request.user:
        logger.warning(f"User {request.user.username} attempted to access workflow {workflow_pk} they don't own")
        messages.error(request, "You don't have permission to view this workflow's activities.")
        return redirect('playbook_list')
    
    # Get activities grouped by phase
    activities_by_phase = ActivityService.get_activities_grouped_by_phase(workflow)
    total_activities = sum(len(acts) for acts in activities_by_phase.values())
    
    # Check if workflow has phases (more than just "Unassigned")
    has_phases = len(activities_by_phase) > 1 or (
        len(activities_by_phase) == 1 and 'Unassigned' not in activities_by_phase
    )
    
    logger.info(f"Loaded {total_activities} activities with {len(activities_by_phase)} phases for workflow {workflow_pk}")
    
    context = {
        'playbook': playbook,
        'workflow': workflow,
        'activities_by_phase': activities_by_phase,
        'has_phases': has_phases,
        'total_activities': total_activities,
        'can_edit': workflow.can_edit(request.user),
    }
    
    return render(request, 'activities/list.html', context)


# ==================== CREATE ====================

@login_required
def activity_create(request, playbook_pk, workflow_pk):
    """
    Create new activity in workflow.
    
    GET: Display create form
    POST: Validate and create activity, redirect to list
    
    Template: activities/create.html
    Template Context:
        - playbook: Playbook instance
        - workflow: Workflow instance
        - status_choices: List of status options
        - form_data: Dict with form values (on validation error)
        - errors: Dict with field errors (on validation error)
    
    :param request: Django request object
    :param playbook_pk: Playbook primary key
    :param workflow_pk: Workflow primary key
    :return: Rendered form template or redirect
    :raises Http404: If playbook or workflow not found
    """
    logger.info(f"User {request.user.username} accessing activity create for workflow {workflow_pk}")
    
    # Get workflow and playbook with permission check
    playbook = get_object_or_404(Playbook, pk=playbook_pk)
    workflow = get_object_or_404(Workflow, pk=workflow_pk, playbook=playbook)
    
    # Check edit permission
    if not workflow.can_edit(request.user):
        logger.warning(f"User {request.user.username} attempted to create activity without permission")
        messages.error(request, "You don't have permission to add activities to this workflow.")
        return redirect('activity_list', playbook_pk=playbook_pk, workflow_pk=workflow_pk)
    
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        phase = request.POST.get('phase', '').strip() or None
        order = request.POST.get('order', '').strip()
        status = request.POST.get('status', 'not_started')
        has_dependencies = request.POST.get('has_dependencies') == 'on'
        
        # Convert order to int if provided
        order_int = None
        if order:
            try:
                order_int = int(order)
            except ValueError:
                messages.error(request, 'Order must be a number.')
                return _render_create_form(request, playbook, workflow, request.POST, {'order': 'Must be a number'})
        
        # Validate and create
        try:
            activity = ActivityService.create_activity(
                workflow=workflow,
                name=name,
                description=description,
                phase=phase,
                order=order_int,
                status=status,
                has_dependencies=has_dependencies
            )
            logger.info(f"Activity '{name}' created successfully in workflow {workflow_pk}")
            messages.success(request, f"Activity '{activity.name}' created successfully!")
            return redirect('activity_list', playbook_pk=playbook_pk, workflow_pk=workflow_pk)
            
        except ValidationError as e:
            logger.warning(f"Activity creation validation error: {str(e)}")
            messages.error(request, str(e))
            return _render_create_form(request, playbook, workflow, request.POST, {})
    
    # GET request - show form
    return _render_create_form(request, playbook, workflow, {}, {})


def _render_create_form(request, playbook, workflow, form_data, errors):
    """Helper to render create form with context."""
    context = {
        'playbook': playbook,
        'workflow': workflow,
        'status_choices': Activity.STATUS_CHOICES,
        'form_data': form_data,
        'errors': errors,
    }
    return render(request, 'activities/create.html', context)


# ==================== STUBS (Future Features) ====================

@login_required
def activity_detail(request, playbook_pk, workflow_pk, activity_pk):
    """
    View activity details (STUB - to be implemented in VIEW feature).
    
    :param request: Django request object
    :param playbook_pk: Playbook primary key
    :param workflow_pk: Workflow primary key
    :param activity_pk: Activity primary key
    :return: Redirect to activity list
    """
    logger.info(f"User {request.user.username} attempted to view activity {activity_pk} (stub)")
    messages.info(request, 'Activity detail view coming soon.')
    return redirect('activity_list', playbook_pk=playbook_pk, workflow_pk=workflow_pk)


@login_required
def activity_edit(request, playbook_pk, workflow_pk, activity_pk):
    """
    Edit activity (STUB - to be implemented in EDIT feature).
    
    :param request: Django request object
    :param playbook_pk: Playbook primary key
    :param workflow_pk: Workflow primary key
    :param activity_pk: Activity primary key
    :return: Redirect to activity list
    """
    logger.info(f"User {request.user.username} attempted to edit activity {activity_pk} (stub)")
    messages.info(request, 'Activity edit functionality coming soon.')
    return redirect('activity_list', playbook_pk=playbook_pk, workflow_pk=workflow_pk)


@login_required
def activity_delete(request, playbook_pk, workflow_pk, activity_pk):
    """
    Delete activity (STUB - to be implemented in DELETE feature).
    
    :param request: Django request object
    :param playbook_pk: Playbook primary key
    :param workflow_pk: Workflow primary key
    :param activity_pk: Activity primary key
    :return: Redirect to activity list
    """
    logger.info(f"User {request.user.username} attempted to delete activity {activity_pk} (stub)")
    messages.info(request, 'Activity delete functionality coming soon.')
    return redirect('activity_list', playbook_pk=playbook_pk, workflow_pk=workflow_pk)
