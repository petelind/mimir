"""
Playbook views for CRUDV operations.

Implements 3-step wizard for playbook creation.
"""

import logging
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from methodology.models import Playbook, Workflow, PlaybookVersion
from methodology.forms import (
    PlaybookBasicInfoForm,
    PlaybookWorkflowForm,
    PlaybookPublishingForm
)

logger = logging.getLogger(__name__)


# ==================== LIST ====================

@login_required
def playbook_list(request):
    """List all playbooks for current user."""
    logger.info(f"User {request.user.username} accessing playbook list")
    
    playbooks = Playbook.objects.filter(author=request.user).order_by('-updated_at')
    
    context = {
        'playbooks': playbooks,
        'total_count': playbooks.count()
    }
    
    return render(request, 'playbooks/list.html', context)


# ==================== CREATE WIZARD ====================

@login_required
def playbook_create(request):
    """
    CREATE Wizard - Step 1: Basic Information.
    
    Collects name, description, category, tags, and visibility.
    Stores in session and proceeds to Step 2.
    """
    logger.info(f"User {request.user.username} starting playbook creation wizard - Step 1")
    
    if request.method == 'POST':
        form = PlaybookBasicInfoForm(request.POST)
        
        if form.is_valid():
            logger.info(f"Step 1 form valid for user {request.user.username}")
            
            # Check for duplicate name
            name = form.cleaned_data['name']
            if Playbook.objects.filter(author=request.user, name=name).exists():
                logger.warning(f"Duplicate playbook name '{name}' for user {request.user.username}")
                form.add_error('name', 'A playbook with this name already exists. Please choose a different name.')
            else:
                # Store in session
                wizard_data = {
                    'name': form.cleaned_data['name'],
                    'description': form.cleaned_data['description'],
                    'category': form.cleaned_data['category'],
                    'tags': form.cleaned_data['tags'],
                    'visibility': form.cleaned_data.get('visibility', 'private'),
                }
                request.session['wizard_data'] = wizard_data
                logger.info(f"Step 1 data saved to session for user {request.user.username}")
                
                return redirect('playbook_create_step2')
        else:
            logger.warning(f"Step 1 form invalid for user {request.user.username}: {form.errors}")
    else:
        # Initialize wizard - clear any previous session data
        if 'wizard_data' in request.session:
            del request.session['wizard_data']
        form = PlaybookBasicInfoForm()
    
    context = {
        'form': form,
        'step': 1,
        'step_title': 'Basic Information'
    }
    
    return render(request, 'playbooks/create_wizard_step1.html', context)


@login_required
def playbook_create_step2(request):
    """
    CREATE Wizard - Step 2: Add Workflows.
    
    Optionally add first workflow or skip to Step 3.
    """
    logger.info(f"User {request.user.username} on playbook creation wizard - Step 2")
    
    # Check if Step 1 was completed
    if 'wizard_data' not in request.session:
        logger.warning(f"User {request.user.username} tried to access Step 2 without completing Step 1")
        messages.warning(request, 'Please complete Step 1 first.')
        return redirect('playbook_create')
    
    if request.method == 'POST':
        form = PlaybookWorkflowForm(request.POST)
        
        # Check if user is skipping
        if request.POST.get('skip') == 'true':
            logger.info(f"User {request.user.username} skipping workflow addition")
            return redirect('playbook_create_step3')
        
        if form.is_valid():
            workflow_name = form.cleaned_data.get('workflow_name', '').strip()
            
            if workflow_name:
                # Store workflow data in session
                wizard_data = request.session['wizard_data']
                wizard_data['workflows'] = [{
                    'name': workflow_name,
                    'description': form.cleaned_data.get('workflow_description', '')
                }]
                request.session['wizard_data'] = wizard_data
                logger.info(f"Workflow '{workflow_name}' added to wizard data for user {request.user.username}")
            
            return redirect('playbook_create_step3')
        else:
            logger.warning(f"Step 2 form invalid for user {request.user.username}: {form.errors}")
    else:
        form = PlaybookWorkflowForm()
    
    context = {
        'form': form,
        'step': 2,
        'step_title': 'Add Workflows',
        'wizard_data': request.session.get('wizard_data', {})
    }
    
    return render(request, 'playbooks/create_wizard_step2.html', context)


@login_required
@transaction.atomic
def playbook_create_step3(request):
    """
    CREATE Wizard - Step 3: Publishing.
    
    Review and publish playbook as Draft or Active.
    Creates Playbook, Workflows, and initial PlaybookVersion.
    """
    logger.info(f"User {request.user.username} on playbook creation wizard - Step 3")
    
    # Check if previous steps were completed
    if 'wizard_data' not in request.session:
        logger.warning(f"User {request.user.username} tried to access Step 3 without completing previous steps")
        messages.warning(request, 'Please complete previous steps first.')
        return redirect('playbook_create')
    
    wizard_data = request.session['wizard_data']
    
    if request.method == 'POST':
        form = PlaybookPublishingForm(request.POST)
        
        if form.is_valid():
            status = form.cleaned_data['status']
            logger.info(f"User {request.user.username} publishing playbook with status: {status}")
            
            try:
                # Create playbook
                playbook = Playbook.objects.create(
                    name=wizard_data['name'],
                    description=wizard_data['description'],
                    category=wizard_data['category'],
                    tags=wizard_data.get('tags', []),
                    visibility=wizard_data.get('visibility', 'private'),
                    status=status,
                    version=1,
                    source='owned',
                    author=request.user
                )
                logger.info(f"Playbook '{playbook.name}' (ID: {playbook.pk}) created by {request.user.username}")
                
                # Create workflows if any
                workflows = wizard_data.get('workflows', [])
                for workflow_data in workflows:
                    workflow = Workflow.objects.create(
                        name=workflow_data['name'],
                        description=workflow_data.get('description', ''),
                        playbook=playbook
                    )
                    logger.info(f"Workflow '{workflow.name}' created for playbook {playbook.pk}")
                
                # Create initial version
                snapshot_data = {
                    'name': playbook.name,
                    'description': playbook.description,
                    'category': playbook.category,
                    'tags': playbook.tags,
                    'visibility': playbook.visibility,
                    'status': playbook.status
                }
                
                PlaybookVersion.objects.create(
                    playbook=playbook,
                    version_number=1,
                    snapshot_data=snapshot_data,
                    change_summary='Initial version',
                    created_by=request.user
                )
                logger.info(f"Version 1 created for playbook {playbook.pk}")
                
                # Clear wizard session
                del request.session['wizard_data']
                
                messages.success(request, f"Playbook '{playbook.name}' created successfully!")
                return redirect('playbook_detail', pk=playbook.pk)
                
            except Exception as e:
                logger.error(f"Error creating playbook for user {request.user.username}: {str(e)}", exc_info=True)
                messages.error(request, 'An error occurred while creating the playbook. Please try again.')
        else:
            logger.warning(f"Step 3 form invalid for user {request.user.username}: {form.errors}")
    else:
        form = PlaybookPublishingForm()
    
    context = {
        'form': form,
        'step': 3,
        'step_title': 'Publishing',
        'wizard_data': wizard_data
    }
    
    return render(request, 'playbooks/create_wizard_step3.html', context)


# ==================== DETAIL ====================

@login_required
def playbook_detail(request, pk):
    """View playbook details."""
    logger.info(f"User {request.user.username} viewing playbook {pk}")
    
    playbook = get_object_or_404(Playbook, pk=pk)
    
    # Check if user has access
    if playbook.source == 'owned' and playbook.author != request.user:
        logger.warning(f"User {request.user.username} attempted to access playbook {pk} they don't own")
        messages.error(request, "You don't have permission to view this playbook.")
        return redirect('playbook_list')
    
    context = {
        'playbook': playbook,
        'workflows': playbook.workflows.all(),
        'versions': playbook.versions.all()[:5],  # Latest 5 versions
        'can_edit': playbook.can_edit(request.user)
    }
    
    return render(request, 'playbooks/detail.html', context)


# ==================== LEGACY STUBS ====================

@login_required
def playbook_add(request):
    """Legacy add view - redirects to wizard."""
    return redirect('playbook_create')


@login_required
def playbook_edit(request, pk):
    """Edit playbook (stub - to be implemented in EDIT phase)."""
    playbook = get_object_or_404(Playbook, pk=pk)
    messages.info(request, 'Edit functionality coming soon.')
    return redirect('playbook_detail', pk=pk)
