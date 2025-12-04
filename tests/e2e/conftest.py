import pytest
from django.contrib.auth.models import User

from methodology.models import Playbook, Workflow, Activity


@pytest.fixture
def nav06_sample_data(transactional_db, django_db_blocker):
    """Create sample data for NAV-06 global search E2E scenario.

    Runs in a synchronous DB context before Playwright starts interacting
    with the page to avoid Sync/async conflicts.
    """
    with django_db_blocker.unblock():
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )

        playbook = Playbook.objects.create(
            name="Component Development Playbook",
            description="Playbook for components",
            category="development",
            author=user,
        )
        workflow = Workflow.objects.create(
            playbook=playbook,
            name="Component Workflow",
            description="Workflow for components",
            order=1,
        )
        Activity.objects.create(
            workflow=workflow,
            name="Create Component",
            guidance="Do component work",
            order=1,
        )

    return {
        "username": "maria",
        "password": "SecurePass123",
        "playbook_name": "Component Development Playbook",
        "workflow_name": "Component Workflow",
        "activity_name": "Create Component",
    }
