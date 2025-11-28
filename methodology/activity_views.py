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


# ==================== VIEW ====================

@login_required
def activity_detail(request, playbook_pk, workflow_pk, activity_pk):
    """
    View activity details.
    
    Displays full activity information including name, description, phase,
    status, dependencies, order, and timestamps.
    
    Template: activities/detail.html
    Template Context:
        - playbook: Playbook instance
        - workflow: Workflow instance
        - activity: Activity instance
        - can_edit: Boolean indicating if user can edit
    
    :param request: Django request object
    :param playbook_pk: Playbook primary key
    :param workflow_pk: Workflow primary key
    :param activity_pk: Activity primary key
    :return: Rendered detail template
    :raises Http404: If playbook, workflow, or activity not found
    """
    logger.info(f"User {request.user.username} viewing activity {activity_pk}")
    
    # Get instances with permission check
    playbook = get_object_or_404(Playbook, pk=playbook_pk)
    workflow = get_object_or_404(Workflow, pk=workflow_pk, playbook=playbook)
    activity = get_object_or_404(Activity, pk=activity_pk, workflow=workflow)
    
    # Check if user has access
    if playbook.source == 'owned' and playbook.author != request.user:
        logger.warning(f"User {request.user.username} attempted to access activity {activity_pk} they don't own")
        messages.error(request, "You don't have permission to view this activity.")
        return redirect('playbook_list')
    
    context = {
        'playbook': playbook,
        'workflow': workflow,
        'activity': activity,
        'can_edit': workflow.can_edit(request.user),
    }
    
    logger.info(f"Activity detail rendered for user {request.user.username}")
    return render(request, 'activities/detail.html', context)


# ==================== EDIT ====================

@login_required
def activity_edit(request, playbook_pk, workflow_pk, activity_pk):
    """
    Edit activity.
    
    GET: Display edit form with current values
    POST: Validate and update activity, redirect to detail
    
    Template: activities/edit.html
    Template Context:
        - playbook: Playbook instance
        - workflow: Workflow instance
        - activity: Activity instance
        - status_choices: List of status options
        - form_data: Dict with form values (on validation error)
        - errors: Dict with field errors (on validation error)
    
    :param request: Django request object
    :param playbook_pk: Playbook primary key
    :param workflow_pk: Workflow primary key
    :param activity_pk: Activity primary key
    :return: Rendered form template or redirect
    :raises Http404: If playbook, workflow, or activity not found
    """
    logger.info(f"User {request.user.username} editing activity {activity_pk}")
    
    # Get instances with permission check
    playbook = get_object_or_404(Playbook, pk=playbook_pk)
    workflow = get_object_or_404(Workflow, pk=workflow_pk, playbook=playbook)
    activity = get_object_or_404(Activity, pk=activity_pk, workflow=workflow)
    
    # Check edit permission
    if not workflow.can_edit(request.user):
        logger.warning(f"User {request.user.username} attempted to edit activity without permission")
        messages.error(request, "You don't have permission to edit this activity.")
        return redirect('activity_detail', playbook_pk=playbook_pk, workflow_pk=workflow_pk, activity_pk=activity_pk)
    
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        phase = request.POST.get('phase', '').strip() or None
        order = request.POST.get('order', '').strip()
        status = request.POST.get('status', 'not_started')
        has_dependencies = request.POST.get('has_dependencies') == 'on'
        
        # Convert order to int
        order_int = None
        if order:
            try:
                order_int = int(order)
            except ValueError:
                messages.error(request, 'Order must be a number.')
                return _render_edit_form(request, playbook, workflow, activity, request.POST, {'order': 'Must be a number'})
        
        # Validate and update
        try:
            update_fields = {
                'name': name,
                'description': description,
                'phase': phase,
                'status': status,
                'has_dependencies': has_dependencies,
            }
            if order_int is not None:
                update_fields['order'] = order_int
            
            ActivityService.update_activity(activity_pk, **update_fields)
            logger.info(f"Activity {activity_pk} updated successfully")
            messages.success(request, f"Activity '{name}' updated successfully!")
            return redirect('activity_detail', playbook_pk=playbook_pk, workflow_pk=workflow_pk, activity_pk=activity_pk)
            
        except ValidationError as e:
            logger.warning(f"Activity edit validation error: {str(e)}")
            messages.error(request, str(e))
            return _render_edit_form(request, playbook, workflow, activity, request.POST, {})
    
    # GET request - show form with current values
    form_data = {
        'name': activity.name,
        'description': activity.description,
        'phase': activity.phase or '',
        'order': activity.order,
        'status': activity.status,
        'has_dependencies': activity.has_dependencies,
    }
    return _render_edit_form(request, playbook, workflow, activity, form_data, {})


def _render_edit_form(request, playbook, workflow, activity, form_data, errors):
    """Helper to render edit form with context."""
    context = {
        'playbook': playbook,
        'workflow': workflow,
        'activity': activity,
        'status_choices': Activity.STATUS_CHOICES,
        'form_data': form_data,
        'errors': errors,
    }
    return render(request, 'activities/edit.html', context)


# ==================== DELETE ====================

@login_required
def activity_delete(request, playbook_pk, workflow_pk, activity_pk):
    """
    Delete activity.
    
    GET: Show confirmation page
    POST: Delete activity and redirect to list
    
    Template: activities/delete.html (confirmation)
    Template Context:
        - playbook: Playbook instance
        - workflow: Workflow instance
        - activity: Activity instance
    
    :param request: Django request object
    :param playbook_pk: Playbook primary key
    :param workflow_pk: Workflow primary key
    :param activity_pk: Activity primary key
    :return: Rendered confirmation template or redirect
    :raises Http404: If playbook, workflow, or activity not found
    """
    logger.info(f"User {request.user.username} deleting activity {activity_pk}")
    
    # Get instances with permission check
    playbook = get_object_or_404(Playbook, pk=playbook_pk)
    workflow = get_object_or_404(Workflow, pk=workflow_pk, playbook=playbook)
    activity = get_object_or_404(Activity, pk=activity_pk, workflow=workflow)
    
    # Check edit permission
    if not workflow.can_edit(request.user):
        logger.warning(f"User {request.user.username} attempted to delete activity without permission")
        messages.error(request, "You don't have permission to delete this activity.")
        return redirect('activity_detail', playbook_pk=playbook_pk, workflow_pk=workflow_pk, activity_pk=activity_pk)
    
    if request.method == 'POST':
        # Confirm deletion
        activity_name = activity.name
        try:
            ActivityService.delete_activity(activity_pk)
            logger.info(f"Activity '{activity_name}' deleted successfully")
            messages.success(request, f"Activity '{activity_name}' deleted successfully!")
            return redirect('activity_list', playbook_pk=playbook_pk, workflow_pk=workflow_pk)
        except Exception as e:
            logger.error(f"Error deleting activity {activity_pk}: {str(e)}")
            messages.error(request, f"Failed to delete activity: {str(e)}")
            return redirect('activity_detail', playbook_pk=playbook_pk, workflow_pk=workflow_pk, activity_pk=activity_pk)
    
    # GET request - show confirmation
    context = {
        'playbook': playbook,
        'workflow': workflow,
        'activity': activity,
    }
    return render(request, 'activities/delete.html', context)
