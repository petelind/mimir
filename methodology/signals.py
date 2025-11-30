"""
Signals for auto-incrementing playbook version on related object changes.

When workflows or activities are added/modified/deleted in a draft playbook,
the playbook version is automatically incremented (0.1 → 0.2 → 0.3, etc.).

Released playbooks cannot be modified directly and require PIP workflow.
"""

import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender='methodology.Workflow')
def increment_playbook_version_on_workflow_change(sender, instance, created, **kwargs):
    """
    Increment playbook version when workflow is created or updated.
    
    Only increments for draft playbooks. Released playbooks are read-only.
    
    :param instance: Workflow instance that was saved
    :param created: Boolean indicating if workflow was newly created
    """
    playbook = instance.playbook
    
    # Only auto-increment for draft playbooks
    if playbook and playbook.is_draft:
        playbook.increment_version()
        playbook.save()
        
        action = "created" if created else "updated"
        logger.info(
            f"Workflow '{instance.name}' {action} in draft playbook '{playbook.name}' "
            f"- version incremented to {playbook.version}"
        )


@receiver(post_delete, sender='methodology.Workflow')
def increment_playbook_version_on_workflow_delete(sender, instance, **kwargs):
    """
    Increment playbook version when workflow is deleted.
    
    Only increments for draft playbooks. Released playbooks are read-only.
    
    :param instance: Workflow instance that was deleted
    """
    playbook = instance.playbook
    
    # Only auto-increment for draft playbooks
    if playbook and playbook.is_draft:
        playbook.increment_version()
        playbook.save()
        
        logger.info(
            f"Workflow '{instance.name}' deleted from draft playbook '{playbook.name}' "
            f"- version incremented to {playbook.version}"
        )


@receiver(post_save, sender='methodology.Activity')
def increment_playbook_version_on_activity_change(sender, instance, created, **kwargs):
    """
    Increment playbook version when activity is created or updated.
    
    Only increments for draft playbooks. Released playbooks are read-only.
    
    :param instance: Activity instance that was saved
    :param created: Boolean indicating if activity was newly created
    """
    workflow = instance.workflow
    playbook = workflow.playbook if workflow else None
    
    # Only auto-increment for draft playbooks
    if playbook and playbook.is_draft:
        playbook.increment_version()
        playbook.save()
        
        action = "created" if created else "updated"
        logger.info(
            f"Activity '{instance.name}' {action} in workflow '{workflow.name}' "
            f"of draft playbook '{playbook.name}' - version incremented to {playbook.version}"
        )


@receiver(post_delete, sender='methodology.Activity')
def increment_playbook_version_on_activity_delete(sender, instance, **kwargs):
    """
    Increment playbook version when activity is deleted.
    
    Only increments for draft playbooks. Released playbooks are read-only.
    
    :param instance: Activity instance that was deleted
    """
    workflow = instance.workflow
    playbook = workflow.playbook if workflow else None
    
    # Only auto-increment for draft playbooks
    if playbook and playbook.is_draft:
        playbook.increment_version()
        playbook.save()
        
        logger.info(
            f"Activity '{instance.name}' deleted from workflow '{workflow.name}' "
            f"of draft playbook '{playbook.name}' - version incremented to {playbook.version}"
        )
