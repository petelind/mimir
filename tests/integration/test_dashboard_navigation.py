import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestDashboardNavigation:
    """Integration tests for dashboard navigation and quick actions (NAV-01..NAV-03)."""

    def test_dashboard_has_quick_create_playbook_action(self):
        """NAV-03: Dashboard shows [+ New Playbook] quick action linking to playbook create wizard."""
        client = Client()
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(user)

        response = client.get(reverse("dashboard"))

        assert response.status_code == 200
        content = response.content.decode("utf-8")

        # Quick action button must be present in header
        assert "New Playbook" in content
        assert 'data-testid="dashboard-quick-new-playbook-header"' in content

        # Tooltip should explain the action
        assert 'data-bs-toggle="tooltip"' in content
        assert 'title="Create a new playbook"' in content

        # Icon should follow UI conventions (playbook icon)
        assert "fa-book-sparkles" in content

        # Link should go to playbook_create (FOB-PLAYBOOKS-CREATE_PLAYBOOK-1 entry point)
        create_url = reverse("playbook_create")
        assert create_url in content
        
        # Verify disabled buttons are present in header
        assert 'data-testid="quick-action-import-playbook-header"' in content
        assert 'data-testid="quick-action-sync-homebase-header"' in content
        assert "Import Playbook" in content
        assert "Sync with Homebase" in content
        
        # Verify Settings button is present
        assert 'data-testid="dashboard-settings-button"' in content
        
        # Verify Dashboard button is NOT present on dashboard
        assert 'Dashboard</button>' not in content or content.count('Dashboard</button>') == 0
