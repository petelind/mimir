"""Repository pattern for playbook data access."""
import logging
from typing import List, Optional
from django.contrib.auth.models import User
from .models import Playbook, Workflow, Visibility, Status, Category

logger = logging.getLogger(__name__)


class PlaybookRepository:
    """Repository for Playbook data access operations.
    
    Provides a clean interface for playbook CRUD operations,
    abstracting the Django ORM. Can be swapped for other
    storage backends (e.g., Neo4j) in the future.
    """
    
    def create_playbook(self, user: User, data: dict) -> Playbook:
        """Create a new playbook for the given user.
        
        Args:
            user: The user creating the playbook
            data: Dictionary with playbook fields
            
        Returns:
            Created Playbook instance
            
        Raises:
            ValidationError: If data is invalid
        """
        logger.info(f"Repository: Creating playbook for user {user.id}")
        
        playbook = Playbook(
            created_by=user,
            name=data.get('name', ''),
            description=data.get('description', ''),
            category=data.get('category', Category.OTHER),
            tags=data.get('tags', []),
            visibility=data.get('visibility', Visibility.PRIVATE),
            status=data.get('status', Status.DRAFT)
        )
        
        # Full model validation
        playbook.full_clean()
        playbook.save()
        
        logger.info(f"Repository: Playbook created with ID {playbook.pk}")
        return playbook
    
    def get_by_id(self, user: User, playbook_id: int) -> Optional[Playbook]:
        """Get a playbook by ID for the given user.
        
        Args:
            user: The user requesting the playbook
            playbook_id: The playbook ID
            
        Returns:
            Playbook instance or None if not found
        """
        logger.debug(f"Repository: Getting playbook {playbook_id} for user {user.id}")
        
        try:
            playbook = Playbook.objects.get(pk=playbook_id, created_by=user)
            logger.debug(f"Repository: Found playbook {playbook_id}")
            return playbook
        except Playbook.DoesNotExist:
            logger.warning(f"Repository: Playbook {playbook_id} not found for user {user.id}")
            return None
    
    def list_by_user(self, user: User, status_filter: Optional[str] = None) -> List[Playbook]:
        """List all playbooks for the given user.
        
        Args:
            user: The user whose playbooks to list
            status_filter: Optional status filter (draft, active, archived)
            
        Returns:
            List of Playbook instances
        """
        logger.debug(f"Repository: Listing playbooks for user {user.id}")
        
        queryset = Playbook.objects.filter(created_by=user)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        playbooks = list(queryset.order_by('-updated_at'))
        logger.debug(f"Repository: Found {len(playbooks)} playbooks for user {user.id}")
        
        return playbooks
    
    def name_exists(self, user: User, name: str, exclude_id: Optional[int] = None) -> bool:
        """Check if a playbook name already exists for the user.
        
        Args:
            user: The user to check against
            name: The playbook name to check
            exclude_id: Optional playbook ID to exclude from check (for updates)
            
        Returns:
            True if name exists, False otherwise
        """
        logger.debug(f"Repository: Checking if name '{name}' exists for user {user.id}")
        
        queryset = Playbook.objects.filter(created_by=user, name__iexact=name)
        
        if exclude_id:
            queryset = queryset.exclude(pk=exclude_id)
        
        exists = queryset.exists()
        logger.debug(f"Repository: Name '{name}' exists for user {user.id}: {exists}")
        
        return exists
    
    def update_playbook(self, user: User, playbook_id: int, data: dict) -> Optional[Playbook]:
        """Update a playbook with new data.
        
        Args:
            user: The user updating the playbook
            playbook_id: The playbook ID to update
            data: Dictionary of fields to update
            
        Returns:
            Updated Playbook instance or None if not found
        """
        logger.info(f"Repository: Updating playbook {playbook_id} for user {user.id}")
        
        playbook = self.get_by_id(user, playbook_id)
        if not playbook:
            logger.warning(f"Repository: Cannot update playbook {playbook_id} - not found")
            return None
        
        # Update fields
        for field, value in data.items():
            if hasattr(playbook, field):
                setattr(playbook, field, value)
        
        # Validate and save
        playbook.full_clean()
        playbook.save()
        
        logger.info(f"Repository: Playbook {playbook_id} updated successfully")
        return playbook
    
    def delete_playbook(self, user: User, playbook_id: int) -> bool:
        """Delete a playbook.
        
        Args:
            user: The user deleting the playbook
            playbook_id: The playbook ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        logger.info(f"Repository: Deleting playbook {playbook_id} for user {user.id}")
        
        playbook = self.get_by_id(user, playbook_id)
        if not playbook:
            logger.warning(f"Repository: Cannot delete playbook {playbook_id} - not found")
            return False
        
        playbook.delete()
        logger.info(f"Repository: Playbook {playbook_id} deleted successfully")
        return True
    
    def get_playbook_count(self, user: User) -> int:
        """Get the total number of playbooks for a user.
        
        Args:
            user: The user to count playbooks for
            
        Returns:
            Number of playbooks
        """
        count = Playbook.objects.filter(created_by=user).count()
        logger.debug(f"Repository: User {user.id} has {count} playbooks")
        return count


class WorkflowRepository:
    """Repository pattern for Workflow data access operations."""
    
    def create(self, playbook, name, description, created_by, status='draft'):
        """Create a new workflow.
        
        Args:
            playbook: Playbook instance
            name: Workflow name
            description: Workflow description  
            created_by: User instance
            status: Workflow status (default: 'draft')
            
        Returns:
            Created Workflow instance
        """
        logger.info(f"Repository: Creating workflow '{name}' for playbook {playbook.id}")
        
        workflow = Workflow.objects.create(
            playbook=playbook,
            name=name,
            description=description,
            status=status,
            created_by=created_by
        )
        
        logger.info(f"Repository: Created workflow {workflow.id}")
        return workflow
    
    def get_by_id(self, workflow_id):
        """Get workflow by ID.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Workflow instance or None
        """
        try:
            workflow = Workflow.objects.get(id=workflow_id)
            logger.debug(f"Repository: Found workflow {workflow_id}")
            return workflow
        except Workflow.DoesNotExist:
            logger.warning(f"Repository: Workflow {workflow_id} not found")
            return None
    
    def list_by_playbook(self, playbook):
        """List all workflows for a playbook.
        
        Args:
            playbook: Playbook instance
            
        Returns:
            QuerySet of workflows ordered by order field
        """
        workflows = Workflow.objects.filter(playbook=playbook).order_by('order', 'created_at')
        logger.debug(f"Repository: Found {workflows.count()} workflows for playbook {playbook.id}")
        return workflows
    
    def update(self, workflow, **kwargs):
        """Update workflow fields.
        
        Args:
            workflow: Workflow instance
            **kwargs: Fields to update
            
        Returns:
            Updated Workflow instance
        """
        logger.info(f"Repository: Updating workflow {workflow.id}")
        
        for field, value in kwargs.items():
            if hasattr(workflow, field):
                setattr(workflow, field, value)
        
        workflow.save()
        logger.info(f"Repository: Updated workflow {workflow.id}")
        return workflow
    
    def delete(self, workflow):
        """Delete a workflow.
        
        Args:
            workflow: Workflow instance
        """
        logger.info(f"Repository: Deleting workflow {workflow.id}")
        workflow.delete()
        logger.info(f"Repository: Deleted workflow {workflow.id}")
    
    def reorder(self, playbook, workflow_ids):
        """Reorder workflows within a playbook.
        
        Args:
            playbook: Playbook instance
            workflow_ids: List of workflow IDs in desired order
        """
        logger.info(f"Repository: Reordering workflows for playbook {playbook.id}")
        
        workflows = Workflow.objects.filter(playbook=playbook, id__in=workflow_ids)
        workflow_dict = {w.id: w for w in workflows}
        
        for index, workflow_id in enumerate(workflow_ids):
            if workflow_id in workflow_dict:
                workflow = workflow_dict[workflow_id]
                workflow.order = index
                workflow.save()
        
        logger.info(f"Repository: Reordered {len(workflow_ids)} workflows")
    
    def count_by_playbook(self, playbook):
        """Count workflows for a playbook.
        
        Args:
            playbook: Playbook instance
            
        Returns:
            Number of workflows
        """
        count = Workflow.objects.filter(playbook=playbook).count()
        logger.debug(f"Repository: Playbook {playbook.id} has {count} workflows")
        return count
