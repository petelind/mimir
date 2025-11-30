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


# Phase 5: Register tools with FastMCP
# Phase 5: Add Activity tools
# Phase 5: Add initialize_mcp() function
