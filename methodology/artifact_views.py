"""
View layer for Artifact operations.

Provides Django views for artifact CRUD operations, list/search functionality,
and deletion with dependency warnings.
"""

import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from methodology.models import Playbook, Activity, Artifact, ArtifactInput
from methodology.services.artifact_service import ArtifactService

logger = logging.getLogger(__name__)


@login_required
def artifact_list(request, playbook_id):
    """
    Display artifacts list for playbook with search/filter.
    
    :param request: Django HttpRequest with GET params
    :param playbook_id: Playbook ID as int from URL
    :returns: HttpResponse with rendered template
    
    Template: artifacts/list.html
    Context:
        - playbook: Playbook instance
        - artifacts: QuerySet of Artifact instances (filtered)
        - search_query: str or None. Example: "API"
        - type_filter: str or None. Example: "Document"
        - required_filter: bool or None. Example: True
        - activity_filter: int or None (activity ID)
        - activities: QuerySet of Activity instances for filter dropdown
        - total_count: int - total artifacts before filtering
        - filtered_count: int - artifacts after filtering
    
    GET Parameters:
        - q: Search query for name/description
        - type: Type filter
        - required: Required filter ("true"/"false")
        - activity: Activity ID filter
    """
    playbook = get_object_or_404(Playbook, pk=playbook_id)
    
    # Check permissions
    if not playbook.is_owned_by(request.user):
        messages.error(request, "You don't have permission to view this playbook's artifacts.")
        logger.warning(f"User {request.user.username} attempted to access artifacts for playbook {playbook_id} without permission")
        return redirect('playbook_list')
    
    # Get filter parameters from request
    search_query = request.GET.get('q', '').strip() or None
    type_filter = request.GET.get('type', '').strip() or None
    required_param = request.GET.get('required', '').strip()
    activity_filter = request.GET.get('activity', '').strip() or None
    
    # Convert required parameter to boolean
    required_filter = None
    if required_param == 'true':
        required_filter = True
    elif required_param == 'false':
        required_filter = False
    
    # Convert activity filter to int
    if activity_filter:
        try:
            activity_filter = int(activity_filter)
        except ValueError:
            activity_filter = None
    
    # Get total count before filtering
    total_count = Artifact.objects.filter(playbook=playbook).count()
    
    # Search and filter artifacts
    artifacts = ArtifactService.search_artifacts(
        playbook=playbook,
        search_query=search_query,
        type_filter=type_filter,
        required_filter=required_filter,
        activity_filter=activity_filter
    )
    
    filtered_count = artifacts.count()
    
    # Get all activities in playbook for filter dropdown
    activities = Activity.objects.filter(
        workflow__playbook=playbook
    ).select_related('workflow').order_by('workflow__order', 'order')
    
    # Get artifact types for filter dropdown
    artifact_types = [choice[0] for choice in Artifact.ARTIFACT_TYPES]
    
    logger.info(f"User {request.user.username} viewing artifacts list for playbook {playbook_id}: {filtered_count}/{total_count} artifacts")
    
    context = {
        'playbook': playbook,
        'artifacts': artifacts,
        'search_query': search_query,
        'type_filter': type_filter,
        'required_filter': required_filter,
        'activity_filter': activity_filter,
        'activities': activities,
        'artifact_types': artifact_types,
        'total_count': total_count,
        'filtered_count': filtered_count,
    }
    
    # If HTMX request, return only the table partial
    if request.headers.get('HX-Request'):
        return render(request, 'artifacts/_table.html', context)
    
    return render(request, 'artifacts/list.html', context)


@login_required
def artifact_delete(request, pk):
    """
    Delete artifact with confirmation modal.
    
    :param request: Django HttpRequest with GET/POST
    :param pk: Artifact ID as int from URL
    :returns: HttpResponse with modal or redirect
    
    GET: Returns delete confirmation modal
    POST: Deletes artifact and redirects to list
    
    Template: artifacts/_delete_modal.html (for GET)
    Context:
        - artifact: Artifact instance
        - consumer_count: int - number of consuming activities
        - consumers: QuerySet of ArtifactInput instances
        - has_template: bool - whether artifact has template file
    """
    artifact = get_object_or_404(Artifact, pk=pk)
    
    # Check permissions
    if not artifact.is_owned_by(request.user):
        messages.error(request, "You don't have permission to delete this artifact.")
        logger.warning(f"User {request.user.username} attempted to delete artifact {pk} without permission")
        return redirect('playbook_list')
    
    if request.method == 'POST':
        # Delete artifact
        playbook_id = artifact.playbook.id
        artifact_name = artifact.name
        
        try:
            result = ArtifactService.delete_artifact(artifact)
            
            messages.success(request, f"Artifact '{artifact_name}' has been deleted successfully.")
            logger.info(f"User {request.user.username} deleted artifact {pk} '{artifact_name}': {result}")
            
            return redirect('artifact_list', playbook_id=playbook_id)
            
        except ValidationError as e:
            messages.error(request, str(e))
            logger.error(f"Failed to delete artifact {pk}: {str(e)}")
            return redirect('artifact_list', playbook_id=playbook_id)
    
    # GET request - return modal
    consumer_count = artifact.consumer_count()
    consumers = artifact.consuming_activities.select_related('activity', 'activity__workflow')
    has_template = bool(artifact.template_file)
    
    logger.info(f"User {request.user.username} opened delete confirmation for artifact {pk} (consumers: {consumer_count}, has_template: {has_template})")
    
    context = {
        'artifact': artifact,
        'consumer_count': consumer_count,
        'consumers': consumers,
        'has_template': has_template,
    }
    
    return render(request, 'artifacts/_delete_modal.html', context)
