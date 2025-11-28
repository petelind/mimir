"""Workflow views for CRUDV operations."""

import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError

from methodology.models import Playbook, Workflow
from methodology.services.workflow_service import WorkflowService

logger = logging.getLogger(__name__)


@login_required
def workflow_create(request, playbook_pk):
    """
    Create new workflow in playbook.
    
    GET: Show creation form
    POST: Create workflow and redirect to detail
    """
    playbook = get_object_or_404(Playbook, pk=playbook_pk)
    
    # Only owner can create workflows
    if not playbook.can_edit(request.user):
        messages.error(request, "You can only create workflows in playbooks you own.")
        return redirect('playbook_detail', pk=playbook_pk)
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        
        # Validate name
        if not name:
            messages.error(request, "Name is required")
            return render(request, 'workflows/create.html', {
                'playbook': playbook,
                'name': name,
                'description': description
            })
        
        try:
            workflow = WorkflowService.create_workflow(
                playbook=playbook,
                name=name,
                description=description
            )
            
            logger.info(f"User {request.user.username} created workflow {workflow.pk}")
            messages.success(request, f"Workflow '{workflow.name}' created in {playbook.name}")
            return redirect('workflow_detail', playbook_pk=playbook.pk, pk=workflow.pk)
            
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, 'workflows/create.html', {
                'playbook': playbook,
                'name': name,
                'description': description
            })
    
    # GET request
    return render(request, 'workflows/create.html', {
        'playbook': playbook
    })


@login_required
def workflow_detail(request, playbook_pk, pk):
    """View workflow details."""
    playbook = get_object_or_404(Playbook, pk=playbook_pk)
    workflow = get_object_or_404(Workflow, pk=pk, playbook=playbook)
    
    return render(request, 'workflows/detail.html', {
        'playbook': playbook,
        'workflow': workflow,
        'can_edit': workflow.can_edit(request.user)
    })


@login_required
def workflow_list(request, playbook_pk):
    """List workflows for playbook."""
    playbook = get_object_or_404(Playbook, pk=playbook_pk)
    workflows = WorkflowService.get_workflows_for_playbook(playbook_pk)
    
    return render(request, 'workflows/list.html', {
        'playbook': playbook,
        'workflows': workflows,
        'can_edit': playbook.can_edit(request.user)
    })


@login_required
def workflow_edit(request, playbook_pk, pk):
    """Edit workflow."""
    playbook = get_object_or_404(Playbook, pk=playbook_pk)
    workflow = get_object_or_404(Workflow, pk=pk, playbook=playbook)
    
    # Only owner can edit
    if not workflow.can_edit(request.user):
        messages.error(request, "You can only edit workflows in playbooks you own.")
        return redirect('workflow_detail', playbook_pk=playbook_pk, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        order = request.POST.get('order', workflow.order)
        
        if not name:
            messages.error(request, "Name is required")
            return render(request, 'workflows/edit.html', {
                'playbook': playbook,
                'workflow': workflow,
                'name': name,
                'description': description
            })
        
        try:
            updated = WorkflowService.update_workflow(
                workflow_id=workflow.pk,
                name=name,
                description=description,
                order=int(order)
            )
            
            logger.info(f"User {request.user.username} updated workflow {workflow.pk}")
            messages.success(request, f"Workflow '{updated.name}' updated successfully")
            return redirect('workflow_detail', playbook_pk=playbook.pk, pk=updated.pk)
            
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, 'workflows/edit.html', {
                'playbook': playbook,
                'workflow': workflow,
                'name': name,
                'description': description
            })
    
    # GET request
    return render(request, 'workflows/edit.html', {
        'playbook': playbook,
        'workflow': workflow
    })


@login_required
def workflow_delete(request, playbook_pk, pk):
    """Delete workflow."""
    playbook = get_object_or_404(Playbook, pk=playbook_pk)
    workflow = get_object_or_404(Workflow, pk=pk, playbook=playbook)
    
    # Only owner can delete
    if not workflow.can_edit(request.user):
        messages.error(request, "You can only delete workflows in playbooks you own.")
        return redirect('workflow_detail', playbook_pk=playbook_pk, pk=pk)
    
    if request.method == 'POST':
        workflow_name = workflow.name
        
        try:
            WorkflowService.delete_workflow(workflow.pk)
            logger.info(f"User {request.user.username} deleted workflow {pk}")
            messages.success(request, f"Workflow '{workflow_name}' deleted successfully")
            return redirect('workflow_list', playbook_pk=playbook.pk)
            
        except Exception as e:
            logger.error(f"Error deleting workflow {pk}: {e}")
            messages.error(request, "Error deleting workflow")
            return redirect('workflow_detail', playbook_pk=playbook_pk, pk=pk)
    
    # GET request - show confirmation (or redirect to detail)
    return redirect('workflow_detail', playbook_pk=playbook_pk, pk=pk)


@login_required
def workflow_duplicate(request, playbook_pk, pk):
    """Duplicate workflow."""
    playbook = get_object_or_404(Playbook, pk=playbook_pk)
    workflow = get_object_or_404(Workflow, pk=pk, playbook=playbook)
    
    # Only owner can duplicate
    if not workflow.can_edit(request.user):
        messages.error(request, "You can only duplicate workflows in playbooks you own.")
        return redirect('workflow_detail', playbook_pk=playbook_pk, pk=pk)
    
    if request.method == 'POST':
        new_name = request.POST.get('new_name', f"{workflow.name} (Copy)").strip()
        
        try:
            duplicate = WorkflowService.duplicate_workflow(
                workflow_id=workflow.pk,
                new_name=new_name
            )
            
            logger.info(f"User {request.user.username} duplicated workflow {pk} as {duplicate.pk}")
            messages.success(request, f"Workflow duplicated as '{duplicate.name}'")
            return redirect('workflow_detail', playbook_pk=playbook.pk, pk=duplicate.pk)
            
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('workflow_detail', playbook_pk=playbook_pk, pk=pk)
    
    # GET request - redirect to detail
    return redirect('workflow_detail', playbook_pk=playbook_pk, pk=pk)
