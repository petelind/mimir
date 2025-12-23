"""
Service layer for Artifact operations.

Provides business logic for artifact CRUD operations, validation,
search/filter functionality, and deletion with dependency handling.
"""

import logging
import os
from django.db import IntegrityError
from django.db.models import Q
from django.core.exceptions import ValidationError
from methodology.models import Artifact, ArtifactInput

logger = logging.getLogger(__name__)


class ArtifactService:
    """Service class for artifact operations."""
    
    @staticmethod
    def create_artifact(activity, name, description='', artifact_type='Document',
                       is_required=False, template_file=None):
        """
        Create artifact with validation.
        
        :param activity: Parent activity instance. Example: Activity.objects.get(id=1)
        :param name: Artifact name as str (max 200 chars). Example: "Component Design Document"
        :param description: Artifact description as str. Example: "Detailed component architecture"
        :param artifact_type: Type as str from ARTIFACT_TYPES. Example: "Document"
        :param is_required: Required flag as bool. Example: True
        :param template_file: Uploaded file or None. Example: InMemoryUploadedFile(...)
        :returns: Created Artifact instance
        :raises ValidationError: If validation fails (empty name, invalid type, etc.)
        
        Example:
            >>> artifact = ArtifactService.create_artifact(
            ...     activity=activity,
            ...     name="API Specification",
            ...     artifact_type="Document",
            ...     is_required=True
            ... )
        """
        # Validate name
        if not name or not name.strip():
            logger.warning(f"Artifact creation failed: empty name for activity {activity.id}")
            raise ValidationError("Artifact name cannot be empty")
        
        if len(name) > 200:
            logger.warning(f"Artifact creation failed: name too long ({len(name)} chars)")
            raise ValidationError("Artifact name cannot exceed 200 characters")
        
        # Check for duplicate name in activity
        if Artifact.objects.filter(activity=activity, name=name).exists():
            logger.warning(f"Artifact creation failed: duplicate name '{name}' in activity {activity.id}")
            raise ValidationError(f"Artifact with name '{name}' already exists in this activity")
        
        # Validate artifact type
        valid_types = [choice[0] for choice in Artifact.ARTIFACT_TYPES]
        if artifact_type not in valid_types:
            logger.warning(f"Artifact creation failed: invalid type '{artifact_type}'")
            raise ValidationError(f"Invalid artifact type. Must be one of: {', '.join(valid_types)}")
        
        # Create artifact
        try:
            artifact = Artifact.objects.create(
                activity=activity,
                playbook=activity.workflow.playbook,
                name=name.strip(),
                description=description.strip() if description else '',
                type=artifact_type,
                is_required=is_required,
                template_file=template_file
            )
            
            file_info = f" with template file" if template_file else ""
            required_info = " (required)" if is_required else ""
            
            logger.info(f"Created artifact '{name}' of type '{artifact_type}' for activity {activity.id}{file_info}{required_info}")
            return artifact
            
        except IntegrityError as e:
            logger.error(f"Artifact creation failed: {str(e)}")
            raise ValidationError(f"Failed to create artifact: {str(e)}")
    
    @staticmethod
    def update_artifact(artifact, name=None, description=None, artifact_type=None,
                       is_required=None, template_file=None):
        """
        Update artifact with validation.
        
        :param artifact: Artifact instance to update
        :param name: New name as str or None. Example: "Updated API Specification"
        :param description: New description as str or None
        :param artifact_type: New type as str or None. Example: "Template"
        :param is_required: New required flag as bool or None
        :param template_file: New uploaded file or None
        :returns: Updated Artifact instance
        :raises ValidationError: If validation fails
        
        Example:
            >>> artifact = ArtifactService.update_artifact(
            ...     artifact=artifact,
            ...     name="Updated API Specification",
            ...     is_required=True
            ... )
        """
        changes = []
        
        # Update name if provided
        if name is not None:
            if not name or not name.strip():
                logger.warning(f"Artifact update failed: empty name for artifact {artifact.id}")
                raise ValidationError("Artifact name cannot be empty")
            
            if len(name) > 200:
                logger.warning(f"Artifact update failed: name too long ({len(name)} chars)")
                raise ValidationError("Artifact name cannot exceed 200 characters")
            
            # Check for duplicate name in activity (excluding current artifact)
            if Artifact.objects.filter(activity=artifact.activity, name=name).exclude(id=artifact.id).exists():
                logger.warning(f"Artifact update failed: duplicate name '{name}' in activity {artifact.activity.id}")
                raise ValidationError(f"Artifact with name '{name}' already exists in this activity")
            
            if artifact.name != name.strip():
                changes.append(f"name: '{artifact.name}' -> '{name.strip()}'")
                artifact.name = name.strip()
        
        # Update description if provided
        if description is not None:
            if artifact.description != description.strip():
                changes.append("description updated")
                artifact.description = description.strip() if description else ''
        
        # Update type if provided
        if artifact_type is not None:
            valid_types = [choice[0] for choice in Artifact.ARTIFACT_TYPES]
            if artifact_type not in valid_types:
                logger.warning(f"Artifact update failed: invalid type '{artifact_type}'")
                raise ValidationError(f"Invalid artifact type. Must be one of: {', '.join(valid_types)}")
            
            if artifact.type != artifact_type:
                changes.append(f"type: '{artifact.type}' -> '{artifact_type}'")
                artifact.type = artifact_type
        
        # Update required flag if provided
        if is_required is not None:
            if artifact.is_required != is_required:
                changes.append(f"required: {artifact.is_required} -> {is_required}")
                artifact.is_required = is_required
        
        # Update template file if provided
        if template_file is not None:
            # Delete old file if exists
            if artifact.template_file:
                old_path = artifact.template_file.path
                if os.path.exists(old_path):
                    os.remove(old_path)
                    logger.info(f"Deleted old template file: {old_path}")
            
            changes.append("template file updated")
            artifact.template_file = template_file
        
        # Save changes
        if changes:
            try:
                artifact.save()
                logger.info(f"Updated artifact {artifact.id}: {', '.join(changes)}")
            except IntegrityError as e:
                logger.error(f"Artifact update failed: {str(e)}")
                raise ValidationError(f"Failed to update artifact: {str(e)}")
        
        return artifact
    
    @staticmethod
    def delete_artifact(artifact):
        """
        Delete artifact and its template file.
        
        :param artifact: Artifact instance to delete
        :returns: Dict with deletion info
        :raises ValidationError: If artifact cannot be deleted
        
        Example:
            >>> result = ArtifactService.delete_artifact(artifact)
            >>> result
            {'deleted': True, 'template_deleted': True, 'consumers_cleared': 3}
        """
        artifact_id = artifact.id
        artifact_name = artifact.name
        template_deleted = False
        consumers_cleared = 0
        
        # Delete template file if exists
        if artifact.template_file:
            try:
                file_path = artifact.template_file.path
                if os.path.exists(file_path):
                    os.remove(file_path)
                    template_deleted = True
                    logger.info(f"Deleted template file for artifact {artifact_id}: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to delete template file for artifact {artifact_id}: {str(e)}")
        
        # Count consumers before deletion (cascade will clear them)
        consumers_cleared = artifact.consuming_activities.count()
        
        # Delete artifact (cascade will delete ArtifactInput relationships)
        try:
            artifact.delete()
            logger.info(f"Deleted artifact {artifact_id} '{artifact_name}' (consumers cleared: {consumers_cleared}, template deleted: {template_deleted})")
            
            return {
                'deleted': True,
                'template_deleted': template_deleted,
                'consumers_cleared': consumers_cleared
            }
        except Exception as e:
            logger.error(f"Failed to delete artifact {artifact_id}: {str(e)}")
            raise ValidationError(f"Failed to delete artifact: {str(e)}")
    
    @staticmethod
    def search_artifacts(playbook, search_query=None, type_filter=None,
                        required_filter=None, activity_filter=None):
        """
        Search and filter artifacts.
        
        :param playbook: Playbook instance
        :param search_query: Search term as str or None. Example: "API"
        :param type_filter: Type as str or None. Example: "Document"
        :param required_filter: Required flag as bool or None
        :param activity_filter: Activity ID as int or None
        :returns: QuerySet of Artifact instances
        
        Example:
            >>> ArtifactService.search_artifacts(playbook, search_query="API", type_filter="Document")
            <QuerySet [<Artifact: API Specification>]>
        """
        # Start with all artifacts in playbook
        queryset = Artifact.objects.filter(playbook=playbook)
        
        # Apply search query (search in name and description)
        if search_query:
            search_query = search_query.strip()
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )
            logger.info(f"Searching artifacts in playbook {playbook.id} with query '{search_query}'")
        
        # Apply type filter
        if type_filter:
            queryset = queryset.filter(type=type_filter)
            logger.info(f"Filtering artifacts in playbook {playbook.id} by type '{type_filter}'")
        
        # Apply required filter
        if required_filter is not None:
            queryset = queryset.filter(is_required=required_filter)
            logger.info(f"Filtering artifacts in playbook {playbook.id} by required={required_filter}")
        
        # Apply activity filter
        if activity_filter:
            queryset = queryset.filter(activity_id=activity_filter)
            logger.info(f"Filtering artifacts in playbook {playbook.id} by activity {activity_filter}")
        
        # Return with related objects for efficiency
        return queryset.select_related('activity', 'activity__workflow').prefetch_related('consuming_activities')
