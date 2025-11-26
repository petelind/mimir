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

        # Quick action button must be present
        assert "+ New Playbook" in content
        assert 'data-testid="dashboard-quick-new-playbook"' in content

        # Link should go to playbook_create (FOB-PLAYBOOKS-CREATE_PLAYBOOK-1 entry point)
        create_url = reverse("playbook_create")
        assert create_url in content
