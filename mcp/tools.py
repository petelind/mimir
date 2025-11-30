"""
MCP Tool Definitions for Mimir.

Thin wrappers around existing service layer methods.
Adds: permission checks, user context, version incrementing.
"""
import logging
from typing import Literal
from decimal import Decimal

logger = logging.getLogger(__name__)


def get_current_user():
    """
    Get current user from MCP context.
    
    Will be implemented in Phase 5 with FastMCP integration.
    For now, skeleton raises NotImplementedError.
    """
    logger.info('MCP: get_current_user() called')
    raise NotImplementedError('User context not yet implemented (Phase 5)')


# ============================================================================
# PLAYBOOK MCP TOOLS
# ============================================================================

def create_playbook_tool(name: str, description: str, category: str) -> dict:
    """
    Create draft playbook.
    
    Thin wrapper over PlaybookService.create_playbook().
    
    :param name: Playbook name. Example: "React Development"
    :param description: Description. Example: "Modern React patterns"
    :param category: Category. Example: "development"
    :return: Created playbook dict with id, name, version, status
    :raises ValueError: if name empty or duplicate
    
    Example:
        >>> result = create_playbook_tool(
        ...     name="React Dev",
        ...     description="React patterns",
        ...     category="development"
        ... )
        >>> result['status']
        'draft'
        >>> result['version']
        '0.1'
    """
    logger.info(f'MCP Tool: create_playbook called - name="{name}", category={category}')
    
    # Phase 5: Get user from MCP context
    user = get_current_user()
    
    # Call existing service
    from methodology.services import PlaybookService
    playbook = PlaybookService.create_playbook(
        name=name,
        description=description,
        category=category,
        author=user,
        status='draft'  # MCP always creates drafts
    )
    
    result = {
        'id': playbook.id,
        'name': playbook.name,
        'description': playbook.description,
        'category': playbook.category,
        'status': playbook.status,
        'version': str(playbook.version),
    }
    logger.info(f'MCP Tool: Created playbook id={playbook.id}, version={playbook.version}')
    return result


def list_playbooks_tool(status: Literal["draft", "released", "active", "all"] = "all") -> list:
    """
    List playbooks filtered by status.
    
    :param status: Filter by status or "all". Example: "draft"
    :return: List of playbook dicts
    """
    logger.info(f'MCP Tool: list_playbooks called - status={status}')
    
    user = get_current_user()
    
    from methodology.services import PlaybookService
    status_filter = None if status == "all" else status
    playbooks = PlaybookService.list_playbooks(user, status=status_filter)
    
    result = [
        {
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'category': p.category,
            'status': p.status,
            'version': str(p.version),
        }
        for p in playbooks
    ]
    logger.info(f'MCP Tool: Returning {len(result)} playbooks')
    return result


def get_playbook_tool(playbook_id: int) -> dict:
    """
    Get playbook details with workflows.
    
    :param playbook_id: Playbook ID. Example: 1
    :return: Playbook dict with nested workflows
    :raises ValueError: if not found or not owned by user
    """
    logger.info(f'MCP Tool: get_playbook called - id={playbook_id}')
    
    user = get_current_user()
    
    from methodology.models import Playbook
    try:
        playbook = Playbook.objects.prefetch_related('workflows').get(
            id=playbook_id,
            author=user
        )
    except Playbook.DoesNotExist:
        logger.error(f'MCP Tool: Playbook id={playbook_id} not found for user')
        raise ValueError(f'Playbook {playbook_id} not found')
    
    result = {
        'id': playbook.id,
        'name': playbook.name,
        'description': playbook.description,
        'category': playbook.category,
        'status': playbook.status,
        'version': str(playbook.version),
        'workflows': [
            {
                'id': w.id,
                'name': w.name,
                'description': w.description,
                'order': w.order,
            }
            for w in playbook.workflows.all()
        ]
    }
    logger.info(f'MCP Tool: Playbook has {len(result["workflows"])} workflows')
    return result


def update_playbook_tool(playbook_id: int, name: str = None,
                        description: str = None, category: str = None) -> dict:
    """
    Update DRAFT playbook. Auto-increments version.
    
    :param playbook_id: Playbook ID. Example: 1
    :param name: New name or None
    :param description: New description or None
    :param category: New category or None
    :return: Updated playbook dict
    :raises PermissionError: if playbook is released
    :raises ValueError: if not found or not owned
    """
    logger.info(f'MCP Tool: update_playbook called - id={playbook_id}')
    
    user = get_current_user()
    
    from methodology.models import Playbook
    try:
        playbook = Playbook.objects.get(id=playbook_id, author=user)
    except Playbook.DoesNotExist:
        logger.error(f'MCP Tool: Playbook id={playbook_id} not found for user')
        raise ValueError(f'Playbook {playbook_id} not found')
    
    # Permission check
    if playbook.status == 'released':
        logger.error(f'MCP Tool: Cannot update released playbook id={playbook_id}')
        raise PermissionError(f'Cannot modify released playbook "{playbook.name}". Use create_pip instead.')
    
    # Build update data
    update_data = {}
    if name is not None:
        update_data['name'] = name
    if description is not None:
        update_data['description'] = description
    if category is not None:
        update_data['category'] = category
    
    if update_data:
        from methodology.services import PlaybookService
        old_version = playbook.version
        
        # Update playbook
        playbook = PlaybookService.update_playbook(playbook_id, **update_data)
        
        # Increment version
        playbook.version += Decimal('0.1')
        playbook.save()
        
        logger.info(f'MCP Tool: Updated playbook, version {old_version} → {playbook.version}')
    
    return {
        'id': playbook.id,
        'name': playbook.name,
        'description': playbook.description,
        'category': playbook.category,
        'status': playbook.status,
        'version': str(playbook.version),
    }


def delete_playbook_tool(playbook_id: int) -> dict:
    """
    Delete DRAFT playbook (cascades to workflows/activities).
    
    :param playbook_id: Playbook ID. Example: 1
    :return: Confirmation dict
    :raises PermissionError: if playbook is released
    :raises ValueError: if not found or not owned
    """
    logger.info(f'MCP Tool: delete_playbook called - id={playbook_id}')
    
    user = get_current_user()
    
    from methodology.models import Playbook
    try:
        playbook = Playbook.objects.get(id=playbook_id, author=user)
    except Playbook.DoesNotExist:
        logger.error(f'MCP Tool: Playbook id={playbook_id} not found for user')
        raise ValueError(f'Playbook {playbook_id} not found')
    
    # Permission check
    if playbook.status == 'released':
        logger.error(f'MCP Tool: Cannot delete released playbook id={playbook_id}')
        raise PermissionError(f'Cannot delete released playbook "{playbook.name}"')
    
    playbook_name = playbook.name
    workflow_count = playbook.workflows.count()
    
    from methodology.services import PlaybookService
    PlaybookService.delete_playbook(playbook_id)
    
    logger.info(f'MCP Tool: Deleted playbook "{playbook_name}" with {workflow_count} workflows')
    return {'deleted': True, 'playbook_id': playbook_id}


# ============================================================================
# WORKFLOW MCP TOOLS
# ============================================================================

def create_workflow_tool(playbook_id: int, name: str, description: str = "") -> dict:
    """
    Create workflow in DRAFT playbook. Increments parent version.
    
    :param playbook_id: Parent playbook ID. Example: 1
    :param name: Workflow name. Example: "Design Phase"
    :param description: Workflow description (optional)
    :return: Created workflow dict
    :raises PermissionError: if parent playbook is released
    :raises ValueError: if playbook not found or duplicate workflow name
    """
    logger.info(f'MCP Tool: create_workflow called - playbook_id={playbook_id}, name="{name}"')
    
    user = get_current_user()
    
    from methodology.models import Playbook
    try:
        playbook = Playbook.objects.get(id=playbook_id, author=user)
    except Playbook.DoesNotExist:
        logger.error(f'MCP Tool: Playbook id={playbook_id} not found for user')
        raise ValueError(f'Playbook {playbook_id} not found')
    
    # Permission check
    if playbook.status == 'released':
        logger.error(f'MCP Tool: Cannot add workflow to released playbook id={playbook_id}')
        raise PermissionError(f'Cannot modify released playbook "{playbook.name}". Use create_pip instead.')
    
    # Call existing service
    from methodology.services import WorkflowService
    old_version = playbook.version
    workflow = WorkflowService.create_workflow(playbook, name, description)
    
    # Increment parent version
    playbook.version += Decimal('0.1')
    playbook.save()
    
    logger.info(f'MCP Tool: Created workflow id={workflow.id}, parent version {old_version} → {playbook.version}')
    
    return {
        'id': workflow.id,
        'name': workflow.name,
        'description': workflow.description,
        'order': workflow.order,
        'playbook_id': playbook.id,
    }


def list_workflows_tool(playbook_id: int) -> list:
    """
    List workflows for playbook.
    
    :param playbook_id: Parent playbook ID. Example: 1
    :return: List of workflow dicts
    :raises ValueError: if playbook not found
    """
    logger.info(f'MCP Tool: list_workflows called - playbook_id={playbook_id}')
    
    user = get_current_user()
    
    from methodology.models import Playbook
    try:
        playbook = Playbook.objects.get(id=playbook_id, author=user)
    except Playbook.DoesNotExist:
        logger.error(f'MCP Tool: Playbook id={playbook_id} not found for user')
        raise ValueError(f'Playbook {playbook_id} not found')
    
    from methodology.services import WorkflowService
    workflows = WorkflowService.get_workflows_for_playbook(playbook_id)
    
    result = [
        {
            'id': w.id,
            'name': w.name,
            'description': w.description,
            'order': w.order,
            'playbook_id': w.playbook_id,
        }
        for w in workflows
    ]
    logger.info(f'MCP Tool: Returning {len(result)} workflows')
    return result


def get_workflow_tool(workflow_id: int) -> dict:
    """
    Get workflow details with activities.
    
    :param workflow_id: Workflow ID. Example: 1
    :return: Workflow dict with nested activities
    :raises ValueError: if not found or not owned
    """
    logger.info(f'MCP Tool: get_workflow called - id={workflow_id}')
    
    user = get_current_user()
    
    from methodology.models import Workflow
    try:
        workflow = Workflow.objects.prefetch_related('activities').get(
            id=workflow_id,
            playbook__author=user
        )
    except Workflow.DoesNotExist:
        logger.error(f'MCP Tool: Workflow id={workflow_id} not found for user')
        raise ValueError(f'Workflow {workflow_id} not found')
    
    result = {
        'id': workflow.id,
        'name': workflow.name,
        'description': workflow.description,
        'order': workflow.order,
        'playbook_id': workflow.playbook_id,
        'activities': [
            {
                'id': a.id,
                'name': a.name,
                'order': a.order,
            }
            for a in workflow.activities.all()
        ]
    }
    logger.info(f'MCP Tool: Workflow has {len(result["activities"])} activities')
    return result


def update_workflow_tool(workflow_id: int, name: str = None,
                        description: str = None, order: int = None) -> dict:
    """
    Update workflow in DRAFT playbook. Increments parent version.
    
    :param workflow_id: Workflow ID. Example: 1
    :param name: New name or None
    :param description: New description or None
    :param order: New order or None
    :return: Updated workflow dict
    :raises PermissionError: if parent playbook is released
    :raises ValueError: if not found
    """
    logger.info(f'MCP Tool: update_workflow called - id={workflow_id}')
    
    user = get_current_user()
    
    from methodology.models import Workflow
    try:
        workflow = Workflow.objects.select_related('playbook').get(
            id=workflow_id,
            playbook__author=user
        )
    except Workflow.DoesNotExist:
        logger.error(f'MCP Tool: Workflow id={workflow_id} not found for user')
        raise ValueError(f'Workflow {workflow_id} not found')
    
    # Permission check
    if workflow.playbook.status == 'released':
        logger.error(f'MCP Tool: Cannot update workflow in released playbook')
        raise PermissionError(f'Cannot modify released playbook "{workflow.playbook.name}". Use create_pip instead.')
    
    # Build update data
    update_data = {}
    if name is not None:
        update_data['name'] = name
    if description is not None:
        update_data['description'] = description
    if order is not None:
        update_data['order'] = order
    
    if update_data:
        from methodology.services import WorkflowService
        old_version = workflow.playbook.version
        
        # Update workflow
        workflow = WorkflowService.update_workflow(workflow_id, **update_data)
        
        # Increment parent version
        workflow.playbook.version += Decimal('0.1')
        workflow.playbook.save()
        
        logger.info(f'MCP Tool: Updated workflow, parent version {old_version} → {workflow.playbook.version}')
    
    return {
        'id': workflow.id,
        'name': workflow.name,
        'description': workflow.description,
        'order': workflow.order,
        'playbook_id': workflow.playbook_id,
    }


def delete_workflow_tool(workflow_id: int) -> dict:
    """
    Delete workflow in DRAFT playbook. Increments parent version.
    
    :param workflow_id: Workflow ID. Example: 1
    :return: Confirmation dict
    :raises PermissionError: if parent playbook is released
    :raises ValueError: if not found
    """
    logger.info(f'MCP Tool: delete_workflow called - id={workflow_id}')
    
    user = get_current_user()
    
    from methodology.models import Workflow
    try:
        workflow = Workflow.objects.select_related('playbook').get(
            id=workflow_id,
            playbook__author=user
        )
    except Workflow.DoesNotExist:
        logger.error(f'MCP Tool: Workflow id={workflow_id} not found for user')
        raise ValueError(f'Workflow {workflow_id} not found')
    
    # Permission check
    if workflow.playbook.status == 'released':
        logger.error(f'MCP Tool: Cannot delete workflow in released playbook')
        raise PermissionError(f'Cannot modify released playbook "{workflow.playbook.name}". Use create_pip instead.')
    
    workflow_name = workflow.name
    playbook = workflow.playbook
    activity_count = workflow.activities.count()
    old_version = playbook.version
    
    from methodology.services import WorkflowService
    WorkflowService.delete_workflow(workflow_id)
    
    # Increment parent version
    playbook.version += Decimal('0.1')
    playbook.save()
    
    logger.info(f'MCP Tool: Deleted workflow "{workflow_name}" ({activity_count} activities), parent version {old_version} → {playbook.version}')
    return {'deleted': True, 'workflow_id': workflow_id}


# ============================================================================
# ACTIVITY MCP TOOLS
# ============================================================================

def create_activity_tool(workflow_id: int, name: str, guidance: str = "",
                        phase: str = None, predecessor_id: int = None) -> dict:
    """
    Create activity in workflow (DRAFT playbook). Increments grandparent version.
    
    :param workflow_id: Parent workflow ID. Example: 1
    :param name: Activity name. Example: "Design Component"
    :param guidance: Rich Markdown guidance (optional)
    :param phase: Phase grouping (optional)
    :param predecessor_id: Predecessor activity ID (optional, must be in same workflow)
    :return: Created activity dict
    :raises PermissionError: if grandparent playbook is released
    :raises ValueError: if workflow not found or validation fails
    """
    logger.info(f'MCP Tool: create_activity called - workflow_id={workflow_id}, name="{name}"')
    
    user = get_current_user()
    
    from methodology.models import Workflow, Activity
    try:
        workflow = Workflow.objects.select_related('playbook').get(
            id=workflow_id,
            playbook__author=user
        )
    except Workflow.DoesNotExist:
        logger.error(f'MCP Tool: Workflow id={workflow_id} not found for user')
        raise ValueError(f'Workflow {workflow_id} not found')
    
    # Permission check on grandparent playbook
    if workflow.playbook.status == 'released':
        logger.error(f'MCP Tool: Cannot add activity to workflow in released playbook')
        raise PermissionError(f'Cannot modify released playbook "{workflow.playbook.name}". Use create_pip instead.')
    
    # Get predecessor if specified
    predecessor = None
    if predecessor_id:
        try:
            predecessor = Activity.objects.get(id=predecessor_id, workflow=workflow)
        except Activity.DoesNotExist:
            logger.error(f'MCP Tool: Predecessor id={predecessor_id} not found in workflow {workflow_id}')
            raise ValueError(f'Predecessor activity {predecessor_id} not found in workflow')
    
    # Call existing service
    from methodology.services import ActivityService
    old_version = workflow.playbook.version
    activity = ActivityService.create_activity(
        workflow=workflow,
        name=name,
        guidance=guidance,
        phase=phase,
        predecessor=predecessor
    )
    
    # Increment grandparent version
    workflow.playbook.version += Decimal('0.1')
    workflow.playbook.save()
    
    logger.info(f'MCP Tool: Created activity id={activity.id}, grandparent version {old_version} → {workflow.playbook.version}')
    
    return {
        'id': activity.id,
        'name': activity.name,
        'guidance': activity.guidance,
        'phase': activity.phase,
        'order': activity.order,
        'workflow_id': workflow.id,
        'predecessor_id': predecessor.id if predecessor else None,
    }


def list_activities_tool(workflow_id: int) -> list:
    """
    List activities for workflow.
    
    :param workflow_id: Parent workflow ID. Example: 1
    :return: List of activity dicts
    :raises ValueError: if workflow not found
    """
    logger.info(f'MCP Tool: list_activities called - workflow_id={workflow_id}')
    
    user = get_current_user()
    
    from methodology.models import Workflow
    try:
        workflow = Workflow.objects.get(id=workflow_id, playbook__author=user)
    except Workflow.DoesNotExist:
        logger.error(f'MCP Tool: Workflow id={workflow_id} not found for user')
        raise ValueError(f'Workflow {workflow_id} not found')
    
    from methodology.services import ActivityService
    activities = ActivityService.get_activities_for_workflow(workflow_id)
    
    result = [
        {
            'id': a.id,
            'name': a.name,
            'guidance': a.guidance,
            'phase': a.phase,
            'order': a.order,
            'workflow_id': a.workflow_id,
            'predecessor_id': a.predecessor_id,
            'successor_id': a.successor_id,
        }
        for a in activities
    ]
    logger.info(f'MCP Tool: Returning {len(result)} activities')
    return result


def get_activity_tool(activity_id: int) -> dict:
    """
    Get activity details with dependencies.
    
    :param activity_id: Activity ID. Example: 1
    :return: Activity dict with predecessor/successor info
    :raises ValueError: if not found or not owned
    """
    logger.info(f'MCP Tool: get_activity called - id={activity_id}')
    
    user = get_current_user()
    
    from methodology.models import Activity
    try:
        activity = Activity.objects.select_related(
            'predecessor', 'successor', 'workflow__playbook'
        ).get(
            id=activity_id,
            workflow__playbook__author=user
        )
    except Activity.DoesNotExist:
        logger.error(f'MCP Tool: Activity id={activity_id} not found for user')
        raise ValueError(f'Activity {activity_id} not found')
    
    result = {
        'id': activity.id,
        'name': activity.name,
        'guidance': activity.guidance,
        'phase': activity.phase,
        'order': activity.order,
        'workflow_id': activity.workflow_id,
        'predecessor': {
            'id': activity.predecessor.id,
            'name': activity.predecessor.name,
        } if activity.predecessor else None,
        'successor': {
            'id': activity.successor.id,
            'name': activity.successor.name,
        } if activity.successor else None,
    }
    logger.info(f'MCP Tool: Activity with predecessor={activity.predecessor_id}, successor={activity.successor_id}')
    return result


def update_activity_tool(activity_id: int, name: str = None, guidance: str = None,
                        phase: str = None, order: int = None) -> dict:
    """
    Update activity in DRAFT playbook. Increments grandparent version.
    
    Note: Use set_predecessor_tool() to change dependencies.
    
    :param activity_id: Activity ID. Example: 1
    :param name: New name or None
    :param guidance: New guidance or None
    :param phase: New phase or None
    :param order: New order or None
    :return: Updated activity dict
    :raises PermissionError: if grandparent playbook is released
    :raises ValueError: if not found
    """
    logger.info(f'MCP Tool: update_activity called - id={activity_id}')
    
    user = get_current_user()
    
    from methodology.models import Activity
    try:
        activity = Activity.objects.select_related('workflow__playbook').get(
            id=activity_id,
            workflow__playbook__author=user
        )
    except Activity.DoesNotExist:
        logger.error(f'MCP Tool: Activity id={activity_id} not found for user')
        raise ValueError(f'Activity {activity_id} not found')
    
    # Permission check
    if activity.workflow.playbook.status == 'released':
        logger.error(f'MCP Tool: Cannot update activity in released playbook')
        raise PermissionError(f'Cannot modify released playbook. Use create_pip instead.')
    
    # Build update data
    update_data = {}
    if name is not None:
        update_data['name'] = name
    if guidance is not None:
        update_data['guidance'] = guidance
    if phase is not None:
        update_data['phase'] = phase
    if order is not None:
        update_data['order'] = order
    
    if update_data:
        from methodology.services import ActivityService
        old_version = activity.workflow.playbook.version
        
        # Update activity
        activity = ActivityService.update_activity(activity_id, **update_data)
        
        # Increment grandparent version
        activity.workflow.playbook.version += Decimal('0.1')
        activity.workflow.playbook.save()
        
        logger.info(f'MCP Tool: Updated activity, grandparent version {old_version} → {activity.workflow.playbook.version}')
    
    return {
        'id': activity.id,
        'name': activity.name,
        'guidance': activity.guidance,
        'phase': activity.phase,
        'order': activity.order,
        'workflow_id': activity.workflow_id,
    }


def delete_activity_tool(activity_id: int) -> dict:
    """
    Delete activity in DRAFT playbook. Increments grandparent version.
    
    :param activity_id: Activity ID. Example: 1
    :return: Confirmation dict
    :raises PermissionError: if grandparent playbook is released
    :raises ValueError: if not found
    """
    logger.info(f'MCP Tool: delete_activity called - id={activity_id}')
    
    user = get_current_user()
    
    from methodology.models import Activity
    try:
        activity = Activity.objects.select_related('workflow__playbook').get(
            id=activity_id,
            workflow__playbook__author=user
        )
    except Activity.DoesNotExist:
        logger.error(f'MCP Tool: Activity id={activity_id} not found for user')
        raise ValueError(f'Activity {activity_id} not found')
    
    # Permission check
    if activity.workflow.playbook.status == 'released':
        logger.error(f'MCP Tool: Cannot delete activity in released playbook')
        raise PermissionError(f'Cannot modify released playbook. Use create_pip instead.')
    
    activity_name = activity.name
    playbook = activity.workflow.playbook
    old_version = playbook.version
    
    from methodology.services import ActivityService
    ActivityService.delete_activity(activity_id)
    
    # Increment grandparent version
    playbook.version += Decimal('0.1')
    playbook.save()
    
    logger.info(f'MCP Tool: Deleted activity "{activity_name}", grandparent version {old_version} → {playbook.version}')
    return {'deleted': True, 'activity_id': activity_id}


def set_predecessor_tool(activity_id: int, predecessor_id: int) -> dict:
    """
    Set activity predecessor (validates no circular dependencies).
    
    :param activity_id: Activity ID. Example: 2
    :param predecessor_id: Predecessor activity ID. Example: 1
    :return: Updated activity dict
    :raises PermissionError: if grandparent playbook is released
    :raises ValueError: if validation fails or circular dependency detected
    """
    logger.info(f'MCP Tool: set_predecessor called - activity_id={activity_id}, predecessor_id={predecessor_id}')
    
    user = get_current_user()
    
    from methodology.models import Activity
    try:
        activity = Activity.objects.select_related('workflow__playbook').get(
            id=activity_id,
            workflow__playbook__author=user
        )
        predecessor = Activity.objects.get(id=predecessor_id, workflow=activity.workflow)
    except Activity.DoesNotExist as e:
        logger.error(f'MCP Tool: Activity not found or not in same workflow')
        raise ValueError('Activity or predecessor not found') from e
    
    # Permission check
    if activity.workflow.playbook.status == 'released':
        logger.error(f'MCP Tool: Cannot modify dependencies in released playbook')
        raise PermissionError(f'Cannot modify released playbook. Use create_pip instead.')
    
    # Call service (validates circular dependencies)
    from methodology.services import ActivityService
    old_version = activity.workflow.playbook.version
    ActivityService.set_predecessor(activity, predecessor)
    
    # Increment grandparent version
    activity.workflow.playbook.version += Decimal('0.1')
    activity.workflow.playbook.save()
    
    logger.info(f'MCP Tool: Set predecessor, grandparent version {old_version} → {activity.workflow.playbook.version}')
    
    return {
        'activity_id': activity.id,
        'predecessor_id': predecessor.id,
        'updated': True,
    }


# Phase 5: Register all tools with FastMCP
# Phase 5: Add initialize_mcp() function
# Phase 5: Add user context management
