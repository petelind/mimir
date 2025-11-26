"""Business logic services for playbook operations."""
import logging
from typing import Dict, List, Optional, Tuple
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Playbook, Visibility, Status, Category
from .repository import PlaybookRepository

logger = logging.getLogger(__name__)


class PlaybookService:
    """Service layer for playbook business logic.
    
    Provides high-level operations that combine repository access
    with business rules and validation. Shared between MCP and Web UI.
    """
    
    def __init__(self, repository: Optional[PlaybookRepository] = None):
        """Initialize service with repository."""
        self.repository = repository or PlaybookRepository()
        logger.debug("PlaybookService initialized")
    
    def validate_basic_info(self, user: User, data: Dict) -> Tuple[bool, Dict]:
        """Validate basic playbook information for Step 1 of wizard.
        
        Args:
            user: The user creating the playbook
            data: Dictionary with basic info fields
            
        Returns:
            Tuple of (is_valid, errors_dict)
        """
        logger.info(f"Service: Validating basic info for user {user.id}")
        
        errors = {}
        
        # Name validation
        name = data.get('name', '').strip()
        if not name:
            errors['name'] = 'Name is required.'
        elif len(name) < 3:
            errors['name'] = 'Name must be at least 3 characters.'
        elif len(name) > 100:
            errors['name'] = 'Name must not exceed 100 characters.'
        elif self.repository.name_exists(user, name):
            errors['name'] = 'A playbook with this name already exists. Please choose a different name.'
        
        # Description validation
        description = data.get('description', '').strip()
        if not description:
            errors['description'] = 'Description is required.'
        elif len(description) < 10:
            errors['description'] = 'Description must be at least 10 characters.'
        elif len(description) > 500:
            errors['description'] = 'Description must not exceed 500 characters.'
        
        # Category validation
        category = data.get('category')
        if not category:
            errors['category'] = 'Please select a category.'
        elif category not in [choice.value for choice in Category]:
            errors['category'] = 'Invalid category selected.'
        
        # Tags validation (optional)
        tags = data.get('tags', [])
        if isinstance(tags, list):
            for i, tag in enumerate(tags):
                if not isinstance(tag, str) or len(tag.strip()) == 0:
                    errors.setdefault('tags', []).append(f'Tag {i+1} must be a non-empty string.')
        elif tags:
            errors['tags'] = 'Tags must be a list of strings.'
        
        # Visibility validation
        visibility = data.get('visibility')
        if not visibility:
            errors['visibility'] = 'Please select a visibility option.'
        elif visibility not in [choice.value for choice in Visibility]:
            errors['visibility'] = 'Invalid visibility option.'
        
        is_valid = len(errors) == 0
        
        if is_valid:
            logger.info(f"Service: Basic info validation passed for user {user.id}")
        else:
            logger.warning(f"Service: Basic info validation failed for user {user.id}: {errors}")
        
        return is_valid, errors
    
    def create_from_wizard(self, user: User, step1_data: Dict, 
                          step2_data: Optional[Dict] = None, 
                          step3_data: Optional[Dict] = None) -> Playbook:
        """Create a playbook from wizard data.
        
        Args:
            user: The user creating the playbook
            step1_data: Basic information from Step 1
            step2_data: Workflow data from Step 2 (optional)
            step3_data: Publishing settings from Step 3 (optional)
            
        Returns:
            Created Playbook instance
            
        Raises:
            ValidationError: If any step data is invalid
        """
        logger.info(f"Service: Creating playbook from wizard for user {user.id}")
        
        # Validate Step 1 (required)
        is_valid, errors = self.validate_basic_info(user, step1_data)
        if not is_valid:
            raise ValidationError(f"Step 1 validation failed: {errors}")
        
        # Prepare playbook data
        playbook_data = {
            'name': step1_data['name'].strip(),
            'description': step1_data['description'].strip(),
            'category': step1_data['category'],
            'tags': step1_data.get('tags', []),
            'visibility': step1_data.get('visibility', Visibility.PRIVATE),
        }
        
        # Apply Step 3 publishing settings if provided
        if step3_data:
            status = step3_data.get('status', Status.DRAFT)
            if status in [choice.value for choice in Status]:
                playbook_data['status'] = status
            
            # Note: version is auto-set by model on creation
            logger.debug(f"Service: Applied Step 3 settings: status={status}")
        
        # Create playbook
        playbook = self.repository.create_playbook(user, playbook_data)
        
        # Handle Step 2 workflow creation
        if step2_data and not step2_data.get('skip_workflows', False):
            workflows_data = step2_data.get('workflows', [])
            if workflows_data:
                from .services import WorkflowService
                workflow_service = WorkflowService()
                
                logger.info(f"Service: Creating {len(workflows_data)} workflows for playbook {playbook.pk}")
                
                for workflow_data in workflows_data:
                    try:
                        success, workflow, errors = workflow_service.create_workflow(
                            playbook=playbook,
                            name=workflow_data['name'],
                            description=workflow_data['description'],
                            created_by=user
                        )
                        if success and workflow:
                            logger.debug(f"Service: Created workflow '{workflow.name}' (ID: {workflow.pk})")
                        else:
                            logger.error(f"Service: Failed to create workflow '{workflow_data.get('name', 'unknown')}': {errors}")
                    except Exception as e:
                        logger.error(f"Service: Failed to create workflow '{workflow_data.get('name', 'unknown')}': {e}")
                        # Continue with other workflows but don't fail the entire playbook creation
                        continue
            else:
                logger.info(f"Service: Step 2 provided but no workflows to create")
        else:
            logger.info(f"Service: Step 2 skipped or not provided")
        
        logger.info(f"Service: Playbook created successfully: {playbook.name} (ID: {playbook.pk})")
        return playbook
    
    def get_playbook_for_user(self, user: User, playbook_id: int) -> Optional[Playbook]:
        """Get a playbook for the user if they have access.
        
        Args:
            user: The user requesting the playbook
            playbook_id: The playbook ID
            
        Returns:
            Playbook instance or None
        """
        logger.debug(f"Service: Getting playbook {playbook_id} for user {user.id}")
        
        playbook = self.repository.get_by_id(user, playbook_id)
        
        if playbook and playbook.is_visible_to_user(user):
            logger.debug(f"Service: User {user.id} has access to playbook {playbook_id}")
            return playbook
        
        logger.warning(f"Service: User {user.id} does not have access to playbook {playbook_id}")
        return None
    
    def list_user_playbooks(self, user: User, status_filter: Optional[str] = None) -> List[Playbook]:
        """List playbooks accessible to the user.
        
        Args:
            user: The user whose playbooks to list
            status_filter: Optional status filter
            
        Returns:
            List of accessible Playbook instances
        """
        logger.debug(f"Service: Listing playbooks for user {user.id}")
        
        playbooks = self.repository.list_by_user(user, status_filter)
        
        # Filter by visibility rules
        accessible = [p for p in playbooks if p.is_visible_to_user(user)]
        
        logger.debug(f"Service: Found {len(accessible)} accessible playbooks for user {user.id}")
        return accessible
    
    def update_playbook(self, user: User, playbook_id: int, data: Dict) -> Optional[Playbook]:
        """Update a playbook with validation.
        
        Args:
            user: The user updating the playbook
            playbook_id: The playbook ID to update
            data: Fields to update
            
        Returns:
            Updated Playbook instance or None
        """
        logger.info(f"Service: Updating playbook {playbook_id} for user {user.id}")
        
        # Get playbook
        playbook = self.get_playbook_for_user(user, playbook_id)
        if not playbook:
            logger.warning(f"Service: Cannot update playbook {playbook_id} - not found or no access")
            return None
        
        # Validate name uniqueness if being updated
        if 'name' in data:
            new_name = data['name'].strip()
            if new_name != playbook.name:
                if self.repository.name_exists(user, new_name, exclude_id=playbook_id):
                    raise ValidationError({'name': 'A playbook with this name already exists.'})
        
        # Update via repository
        updated = self.repository.update_playbook(user, playbook_id, data)
        
        if updated:
            logger.info(f"Service: Playbook {playbook_id} updated successfully")
        else:
            logger.error(f"Service: Failed to update playbook {playbook_id}")
        
        return updated
    
    def delete_playbook(self, user: User, playbook_id: int) -> bool:
        """Delete a playbook if user has permission.
        
        Args:
            user: The user deleting the playbook
            playbook_id: The playbook ID to delete
            
        Returns:
            True if deleted, False otherwise
        """
        logger.info(f"Service: Deleting playbook {playbook_id} for user {user.id}")
        
        # Check access
        playbook = self.get_playbook_for_user(user, playbook_id)
        if not playbook:
            logger.warning(f"Service: Cannot delete playbook {playbook_id} - not found or no access")
            return False
        
        # Only allow creator to delete
        if playbook.created_by != user:
            logger.warning(f"Service: User {user.id} not creator of playbook {playbook_id}")
            return False
        
        return self.repository.delete_playbook(user, playbook_id)


class WorkflowService:
    """Service layer for workflow business logic and validation."""
    
    def __init__(self):
        """Initialize service with repository."""
        from .repository import WorkflowRepository
        self.repository = WorkflowRepository()
    
    def validate_workflow_data(self, playbook, name, description, workflow_id=None):
        """Validate workflow data for creation or update.
        
        Args:
            playbook: Playbook instance
            name: Workflow name
            description: Workflow description
            workflow_id: ID for update validation (None for create)
            
        Returns:
            Tuple of (is_valid: bool, errors: dict)
        """
        logger.info(f"Service: Validating workflow data for playbook {playbook.id}")
        
        errors = {}
        
        # Name validation
        if not name or not name.strip():
            errors['name'] = 'Workflow name is required.'
        elif len(name.strip()) < 3:
            errors['name'] = 'Workflow name must be at least 3 characters.'
        elif len(name.strip()) > 200:
            errors['name'] = 'Workflow name cannot exceed 200 characters.'
        
        # Description validation
        if not description or not description.strip():
            errors['description'] = 'Workflow description is required.'
        elif len(description.strip()) < 10:
            errors['description'] = 'Workflow description must be at least 10 characters.'
        elif len(description.strip()) > 2000:
            errors['description'] = 'Workflow description cannot exceed 2000 characters.'
        
        # Check for duplicate name within same playbook
        # Skip database check for temporary playbooks (not saved yet)
        if not errors.get('name') and hasattr(playbook, 'pk') and playbook.pk:
            existing = self.repository.list_by_playbook(playbook).filter(
                name=name.strip()
            ).exclude(id=workflow_id).first()
            if existing:
                errors['name'] = 'A workflow with this name already exists in this playbook.'
        
        is_valid = not bool(errors)
        
        if is_valid:
            logger.info(f"Service: Workflow validation passed")
        else:
            logger.warning(f"Service: Workflow validation failed: {errors}")
        
        return is_valid, errors
    
    def create_workflow(self, playbook, name, description, created_by, status='draft'):
        """Create a new workflow with validation.
        
        Args:
            playbook: Playbook instance
            name: Workflow name
            description: Workflow description
            created_by: User instance
            status: Workflow status
            
        Returns:
            Tuple of (success: bool, workflow: Workflow or None, errors: dict)
        """
        logger.info(f"Service: Creating workflow for playbook {playbook.id}")
        
        # Validate data
        is_valid, errors = self.validate_workflow_data(playbook, name, description)
        
        if not is_valid:
            logger.warning(f"Service: Workflow creation failed validation: {errors}")
            return False, None, errors
        
        # Create workflow
        try:
            workflow = self.repository.create(
                playbook=playbook,
                name=name.strip(),
                description=description.strip(),
                created_by=created_by,
                status=status
            )
            
            logger.info(f"Service: Workflow created successfully: {workflow.id}")
            return True, workflow, {}
            
        except Exception as e:
            logger.error(f"Service: Failed to create workflow: {e}")
            return False, None, {'general': 'Failed to create workflow.'}
    
    def update_workflow(self, workflow, name=None, description=None, status=None):
        """Update an existing workflow with validation.
        
        Args:
            workflow: Workflow instance
            name: New name (optional)
            description: New description (optional)
            status: New status (optional)
            
        Returns:
            Tuple of (success: bool, workflow: Workflow or None, errors: dict)
        """
        logger.info(f"Service: Updating workflow {workflow.id}")
        
        # Prepare update data
        updates = {}
        if name is not None:
            updates['name'] = name
        if description is not None:
            updates['description'] = description
        if status is not None:
            updates['status'] = status
        
        # Validate changes
        test_name = updates.get('name', workflow.name)
        test_description = updates.get('description', workflow.description)
        
        is_valid, errors = self.validate_workflow_data(
            workflow.playbook, test_name, test_description, workflow.id
        )
        
        if not is_valid:
            logger.warning(f"Service: Workflow update failed validation: {errors}")
            return False, None, errors
        
        # Update workflow
        try:
            updated_workflow = self.repository.update(workflow, **updates)
            logger.info(f"Service: Workflow {workflow.id} updated successfully")
            return True, updated_workflow, {}
            
        except Exception as e:
            logger.error(f"Service: Failed to update workflow {workflow.id}: {e}")
            return False, None, {'general': 'Failed to update workflow.'}
    
    def delete_workflow(self, workflow):
        """Delete a workflow.
        
        Args:
            workflow: Workflow instance
            
        Returns:
            True if deleted, False otherwise
        """
        logger.info(f"Service: Deleting workflow {workflow.id}")
        
        try:
            self.repository.delete(workflow)
            logger.info(f"Service: Workflow {workflow.id} deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Service: Failed to delete workflow {workflow.id}: {e}")
            return False
    
    def reorder_workflows(self, playbook, workflow_ids):
        """Reorder workflows within a playbook.
        
        Args:
            playbook: Playbook instance
            workflow_ids: List of workflow IDs in desired order
            
        Returns:
            True if reordered, False otherwise
        """
        logger.info(f"Service: Reordering workflows for playbook {playbook.id}")
        
        try:
            self.repository.reorder(playbook, workflow_ids)
            logger.info(f"Service: Workflows reordered successfully")
            return True
            
        except Exception as e:
            logger.error(f"Service: Failed to reorder workflows: {e}")
            return False
