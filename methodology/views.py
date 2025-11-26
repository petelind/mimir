"""Views for the methodology app."""
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.core.exceptions import ValidationError
from .models import Playbook, Visibility, Status, Category
from .services import PlaybookService

logger = logging.getLogger(__name__)


def index(request):
    """
    Home page - methodology explorer landing page. Public access allowed.
    
    :param request: Django request object. Example: HttpRequest(method='GET', user=<User: admin>)
    :return: Rendered HTML response. Example: HttpResponse(status=200, content="<div>...</div>")
    """
    return render(request, 'methodology/index.html')


@login_required
def playbook_list(request):
    """
    Display list of playbooks as cards with filters and search.
    
    Implements: PB-1.1, PB-1.2, PB-1.3, PB-1.4
    GET /playbooks/
    """
    from .repository import PlaybookRepository
    
    repository = PlaybookRepository()
    playbooks = repository.list_by_user(request.user)
    
    context = {
        'playbooks': [
            {
                'id': p.pk,
                'name': p.name,
                'description': p.description,
                'category': p.category,
                'status': p.status,
                'version': p.version,
                'author': p.created_by.username,
                'created_at': p.created_at.strftime('%Y-%m-%d'),
                'updated_at': p.updated_at.strftime('%Y-%m-%d'),
                'type': 'Playbook',  # For now, all are playbooks
                'family': p.category.title(),  # Use category as family for now
            }
            for p in playbooks
        ],
        'families': sorted(list(set(p['category'].title() for p in playbooks))),
        'page_title': 'Playbooks',
    }
    return render(request, 'playbooks/list.html', context)


@login_required
def playbook_detail(request, playbook_id):
    """
    Display single playbook detail view.
    
    Implements: PB-2.1, PB-2.2
    GET /playbooks/<id>/
    """
    from .repository import PlaybookRepository
    
    repository = PlaybookRepository()
    playbook = repository.get_by_id(request.user, playbook_id)
    
    if not playbook:
        context = {
            'playbook_id': playbook_id,
            'page_title': 'Playbook Not Found',
        }
        return render(request, 'playbooks/404.html', context, status=404)
    
    context = {
        'playbook': {
            'id': playbook.pk,
            'name': playbook.name,
            'description': playbook.description,
            'category': playbook.category,
            'status': playbook.status,
            'version': playbook.version,
            'author': playbook.created_by.username,
            'created_at': playbook.created_at.strftime('%Y-%m-%d'),
            'updated_at': playbook.updated_at.strftime('%Y-%m-%d'),
            'type': 'Playbook',
            'family': playbook.category.title(),
            'tags': playbook.tags,
        },
        'page_title': playbook.name,
    }
    return render(request, 'playbooks/detail.html', context)


@login_required
def playbook_add(request):
    """
    Display form to create a new playbook.
    
    Implements: PB-3.1, PB-3.2, PB-3.3, PB-3.4, PB-3.5
    GET /playbooks/add/
    """
    context = {
        'mode': 'add',
        'page_title': 'Add Playbook',
        'playbook': None,
        'families': ['Design', 'Development', 'Research', 'Management', 'Product', 'Other'],
        'types': ['Playbook'],
        'statuses': ['Draft', 'Active', 'Archived'],
    }
    return render(request, 'playbooks/form.html', context)


@login_required
def playbook_edit(request, playbook_id):
    """
    Display form to edit an existing playbook.
    
    Implements: PB-4.1, PB-4.2, PB-4.3
    GET /playbooks/<id>/edit/
    """
    from .repository import PlaybookRepository
    
    repository = PlaybookRepository()
    playbook = repository.get_by_id(request.user, playbook_id)
    
    if not playbook:
        context = {
            'playbook_id': playbook_id,
            'page_title': 'Playbook Not Found',
        }
        return render(request, 'playbooks/404.html', context, status=404)
    
    context = {
        'mode': 'edit',
        'page_title': f'Edit Playbook: {playbook.name}',
        'playbook': {
            'id': playbook.pk,
            'name': playbook.name,
            'description': playbook.description,
            'category': playbook.category,
            'status': playbook.status,
            'version': playbook.version,
            'author': playbook.created_by.username,
            'created_at': playbook.created_at.strftime('%Y-%m-%d'),
            'updated_at': playbook.updated_at.strftime('%Y-%m-%d'),
            'type': 'Playbook',
            'family': playbook.category.title(),
            'tags': playbook.tags,
        },
        'families': ['Design', 'Development', 'Research', 'Management', 'Product', 'Other'],
        'types': ['Playbook'],
        'statuses': ['Draft', 'Active', 'Archived'],
    }
    return render(request, 'playbooks/form.html', context)


@login_required
def dashboard(request):
    """
    Dashboard stub page (FOB-DASHBOARD-1).
    
    Placeholder view for dashboard. Full implementation tracked separately
    in navigation.feature issues #17-22.
    
    Template: dashboard.html
    Context: None
    
    :param request: Django request object
    :return: Rendered dashboard stub template
    """
    logger.info(f"User {request.user.username} accessed dashboard stub")
    return render(request, 'dashboard.html')


@login_required
def playbook_create_step1(request: HttpRequest) -> HttpResponse:
    """Handle Step 1 of playbook creation wizard.
    
    Template: playbooks/wizard/step1_basic.html
    Context:
        form: Dictionary with form data and validation errors
        visibility_choices: List of (value, label) tuples for visibility field
    
    Args:
        request: Django request object
        
    Returns:
        Rendered HTML response
    """
    logger.info(f"User {request.user.username} accessing playbook creation Step 1")
    
    if request.method == 'GET':
        # Initial form display
        context = {
            'form': {},
            'visibility_choices': [(choice.value, choice.label) for choice in Visibility],
        }
        return render(request, 'playbooks/wizard/step1_basic.html', context)
    
    elif request.method == 'POST':
        # Form submission
        service = PlaybookService()
        
        # Prepare data for validation
        tags_input = request.POST.get('tags', '').strip()
        tags_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()] if tags_input else []
        
        data = {
            'name': request.POST.get('name', '').strip(),
            'description': request.POST.get('description', '').strip(),
            'category': request.POST.get('category', '').strip(),
            'visibility': request.POST.get('visibility', '').strip(),
            'tags': tags_list,
        }
        
        # Validate
        is_valid, errors = service.validate_basic_info(request.user, data)
        
        if is_valid:
            logger.info(f"Step 1 validation passed for user {request.user.id}")
            
            # Store Step 1 data in session for next steps
            request.session['playbook_wizard_step1'] = data
            
            # Redirect to Step 2
            messages.success(request, 'Basic information saved successfully.')
            return redirect('playbook_create_step2')
        else:
            logger.warning(f"Step 1 validation failed for user {request.user.id}: {errors}")
            
            # Return form with errors
            context = {
                'form': {**data, 'errors': errors},
                'visibility_choices': [(choice.value, choice.label) for choice in Visibility],
            }
            
            # Add field-specific errors for template rendering
            for field, field_errors in errors.items():
                # Always store as list for template iteration
                if isinstance(field_errors, list):
                    context['form'][f'{field}_errors'] = field_errors
                else:
                    context['form'][f'{field}_errors'] = [field_errors]
            
            return render(request, 'playbooks/wizard/step1_basic.html', context)


@login_required
def playbook_create_step2(request: HttpRequest) -> HttpResponse:
    """Handle Step 2 of playbook creation wizard.
    
    Template: playbooks/wizard/step2_workflows.html
    Context:
        step1_data: Data from Step 1
        workflows: List of added workflows
        form: Workflow form data and errors (if any)
    
    Args:
        request: Django request object
        
    Returns:
        Rendered HTML response
    """
    logger.info(f"User {request.user.username} accessing playbook creation Step 2")
    
    # Check if Step 1 data exists
    step1_data = request.session.get('playbook_wizard_step1')
    if not step1_data:
        logger.warning(f"No Step 1 data found for user {request.user.id}, redirecting to Step 1")
        messages.error(request, 'Please complete Step 1 first.')
        return redirect('playbook_create_step1')
    
    # Get workflows from session (stored as list of dicts)
    session_workflows = request.session.get('playbook_wizard_workflows', [])
    
    if request.method == 'GET':
        # Display Step 2 with current workflows
        context = {
            'step1_data': step1_data,
            'workflows': session_workflows,
            'form': {},
        }
        return render(request, 'playbooks/wizard/step2_workflows.html', context)
    
    elif request.method == 'POST':
        from .services import WorkflowService
        
        service = WorkflowService()
        
        # Handle different actions
        action = request.POST.get('action', '')
        
        if action == 'add_workflow':
            # Add a new workflow
            workflow_data = {
                'name': request.POST.get('workflow_name', '').strip(),
                'description': request.POST.get('workflow_description', '').strip(),
            }
            
            # Create temporary playbook for validation (won't be saved)
            from .models import Playbook, Visibility, Status, Category
            temp_playbook = Playbook(
                name=step1_data['name'],
                description=step1_data['description'],
                category=Category(step1_data['category']),
                visibility=Visibility(step1_data['visibility']),
                created_by=request.user
            )
            
            # Validate workflow data
            is_valid, errors = service.validate_workflow_data(
                temp_playbook, 
                workflow_data['name'], 
                workflow_data['description']
            )
            
            # Check for duplicate in session workflows
            if is_valid:
                for existing_workflow in session_workflows:
                    if existing_workflow['name'].lower() == workflow_data['name'].lower():
                        errors['name'] = 'A workflow with this name already exists in this playbook.'
                        is_valid = False
                        break
            
            if is_valid:
                # Add to session workflows
                workflow_dict = {
                    'id': f"temp_{len(session_workflows) + 1}",  # Temporary ID
                    'name': workflow_data['name'],
                    'description': workflow_data['description'],
                    'status': 'draft',
                    'order': len(session_workflows),
                }
                session_workflows.append(workflow_dict)
                request.session['playbook_wizard_workflows'] = session_workflows
                
                logger.info(f"Added workflow to session: {workflow_data['name']}")
                messages.success(request, f'Workflow "{workflow_data["name"]}" added.')
                
                # Clear form
                context = {
                    'step1_data': step1_data,
                    'workflows': session_workflows,
                    'form': {},
                }
            else:
                # Return form with errors
                context = {
                    'step1_data': step1_data,
                    'workflows': session_workflows,
                    'form': {**workflow_data, 'errors': errors},
                }
                
                # Add field-specific errors for template rendering
                for field, field_errors in errors.items():
                    if isinstance(field_errors, list):
                        context['form'][f'{field}_errors'] = field_errors
                    else:
                        context['form'][f'{field}_errors'] = [field_errors]
            
            return render(request, 'playbooks/wizard/step2_workflows.html', context)
        
        elif action == 'remove_workflow':
            # Remove a workflow
            workflow_id = request.POST.get('workflow_id')
            session_workflows = [w for w in session_workflows if w['id'] != workflow_id]
            
            # Reorder remaining workflows
            for i, workflow in enumerate(session_workflows):
                workflow['order'] = i
            
            request.session['playbook_wizard_workflows'] = session_workflows
            logger.info(f"Removed workflow {workflow_id}")
            messages.success(request, 'Workflow removed.')
            
            context = {
                'step1_data': step1_data,
                'workflows': session_workflows,
                'form': {},
            }
            return render(request, 'playbooks/wizard/step2_workflows.html', context)
        
        elif action == 'skip':
            # Skip adding workflows
            step2_data = {
                'skip_workflows': True,
                'workflows': [],
            }
            request.session['playbook_wizard_step2'] = step2_data
            request.session['playbook_wizard_workflows'] = []  # Clear workflows
            
            logger.info(f"User {request.user.id} skipped adding workflows")
            return redirect('playbook_create_step3')
        
        elif action == 'continue':
            # Continue to Step 3 with workflows
            step2_data = {
                'skip_workflows': False,
                'workflows': session_workflows,
            }
            request.session['playbook_wizard_step2'] = step2_data
            
            logger.info(f"User {request.user.id} continuing to Step 3 with {len(session_workflows)} workflows")
            return redirect('playbook_create_step3')
        
        else:
            # Default: show the form
            context = {
                'step1_data': step1_data,
                'workflows': session_workflows,
                'form': {},
            }
            return render(request, 'playbooks/wizard/step2_workflows.html', context)


@login_required
def playbook_create_step3(request: HttpRequest) -> HttpResponse:
    """Handle Step 3 of playbook creation wizard.
    
    Template: playbooks/wizard/step3_publish.html
    
    Args:
        request: Django request object
        
    Returns:
        Rendered HTML response
    """
    logger.info(f"User {request.user.username} accessing playbook creation Step 3")
    
    # Check if previous steps data exists
    step1_data = request.session.get('playbook_wizard_step1')
    step2_data = request.session.get('playbook_wizard_step2')
    
    if not step1_data:
        logger.warning(f"No Step 1 data found for user {request.user.id}, redirecting to Step 1")
        messages.error(request, 'Please complete Step 1 first.')
        return redirect('playbook_create_step1')
    
    if request.method == 'GET':
        context = {
            'step1_data': step1_data,
            'step2_data': step2_data or {},
            'status_choices': Status.choices,
            'visibility_choices': Visibility.choices,
        }
        return render(request, 'playbooks/wizard/step3_publish.html', context)
    
    elif request.method == 'POST':
        # Get publishing settings
        step3_data = {
            'status': request.POST.get('status', Status.DRAFT),
        }
        
        try:
            # Create playbook from wizard data
            service = PlaybookService()
            playbook = service.create_from_wizard(
                user=request.user,
                step1_data=step1_data,
                step2_data=step2_data,
                step3_data=step3_data
            )
            
            # Clear wizard session data
            if 'playbook_wizard_step1' in request.session:
                del request.session['playbook_wizard_step1']
            if 'playbook_wizard_step2' in request.session:
                del request.session['playbook_wizard_step2']
            if 'playbook_wizard_workflows' in request.session:
                del request.session['playbook_wizard_workflows']
            
            logger.info(f"Playbook created successfully: {playbook.name} (ID: {playbook.pk})")
            messages.success(request, f'Playbook "{playbook.name}" created successfully!')
            
            return redirect('playbook_detail', playbook_id=playbook.pk)
            
        except ValidationError as e:
            logger.error(f"Validation error creating playbook: {e}")
            messages.error(request, f'Error creating playbook: {e}')
            
            context = {
                'step1_data': step1_data,
                'step2_data': step2_data or {},
                'status_choices': Status.choices,
                'visibility_choices': Visibility.choices,
            }
            return render(request, 'playbooks/wizard/step3_publish.html', context)

