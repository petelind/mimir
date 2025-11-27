import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from methodology.models import Playbook


@pytest.mark.django_db
class TestPlaybookDeleteBackend:
    """Core backend tests for playbook delete (Issue #31, PB-DELETE-05)."""

    def test_confirm_deletion_deletes_playbook_and_redirects_to_list(self, client):
        """Deleting an owned playbook should remove it and redirect to list page."""
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(user)

        playbook = Playbook.objects.create(
            name="Old Design Patterns",
            description="To be deleted",
            category="development",
            tags=[],
            visibility="private",
            status="disabled",
            version=1,
            source="owned",
            author=user,
        )

        delete_url = reverse("playbook_delete", kwargs={"pk": playbook.pk})
        response = client.post(delete_url, follow=True)

        # Should redirect to playbook list
        assert response.redirect_chain
        final_url, status_code = response.redirect_chain[-1]
        assert status_code == 302
        assert final_url == reverse("playbook_list")

        # Playbook should be gone from DB
        assert not Playbook.objects.filter(pk=playbook.pk).exists()

    def test_detail_returns_404_after_playbook_deleted(self, client):
        """After deletion, accessing playbook_detail should result in 404."""
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(user)

        playbook = Playbook.objects.create(
            name="To Delete Detail",
            description="Will be deleted",
            category="development",
            tags=[],
            visibility="private",
            status="disabled",
            version=1,
            source="owned",
            author=user,
        )

        delete_url = reverse("playbook_delete", kwargs={"pk": playbook.pk})
        client.post(delete_url, follow=True)

        detail_url = reverse("playbook_detail", kwargs={"pk": playbook.pk})
        response = client.get(detail_url)
        assert response.status_code == 404

    def test_delete_flow_does_not_expose_undo_option(self, client):
        """Delete success response should not contain any Undo link or text."""
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(user)

        playbook = Playbook.objects.create(
            name="No Recovery Playbook",
            description="Ensure no undo UI",
            category="development",
            tags=[],
            visibility="private",
            status="disabled",
            version=1,
            source="owned",
            author=user,
        )

        delete_url = reverse("playbook_delete", kwargs={"pk": playbook.pk})
        response = client.post(delete_url, follow=True)

        assert response.status_code == 200
        content = response.content.decode("utf-8")
        assert "Undo" not in content


@pytest.mark.django_db
class TestPlaybookDeleteDetailUI:
    """UI tests for delete control on playbook detail page (no modal yet)."""

    def test_detail_page_shows_delete_button_for_owned_playbook(self, client):
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(user)

        playbook = Playbook.objects.create(
            name="Deletable Playbook",
            description="To be deleted via detail page",
            category="development",
            tags=[],
            visibility="private",
            status="disabled",
            version=1,
            source="owned",
            author=user,
        )

        detail_url = reverse("playbook_detail", kwargs={"pk": playbook.pk})
        response = client.get(detail_url)

        assert response.status_code == 200
        content = response.content.decode("utf-8")

        # Delete control should be present and use playbook_delete_confirm via HTMX
        confirm_url = reverse("playbook_delete_confirm", kwargs={"pk": playbook.pk})
        assert confirm_url in content
        assert "hx-get" in content
        assert "Delete" in content

    def test_detail_page_hides_delete_for_downloaded_playbook(self, client):
        owner = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="SecurePass123",
        )
        other_user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(other_user)

        playbook = Playbook.objects.create(
            name="Downloaded Playbook",
            description="Downloaded from Homebase",
            category="development",
            tags=[],
            visibility="private",
            status="disabled",
            version=1,
            source="downloaded",
            author=owner,
        )

        detail_url = reverse("playbook_detail", kwargs={"pk": playbook.pk})
        response = client.get(detail_url, follow=True)

        # Non-owner of downloaded playbook should not see delete controls
        assert response.status_code == 200
        content = response.content.decode("utf-8")
        confirm_url = reverse("playbook_delete_confirm", kwargs={"pk": playbook.pk})
        assert confirm_url not in content
        delete_url = reverse("playbook_delete", kwargs={"pk": playbook.pk})
        assert delete_url not in content
        assert "Delete" not in content


@pytest.mark.django_db
class TestPlaybookDeleteModalEndpoint:
    """Tests for the delete confirmation modal endpoint (HTMX fragment)."""

    def test_delete_confirm_endpoint_renders_modal_for_owned_playbook(self, client):
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(user)

        playbook = Playbook.objects.create(
            name="Modal Target Playbook",
            description="To be deleted via modal",
            category="development",
            tags=[],
            visibility="private",
            status="disabled",
            version=1,
            source="owned",
            author=user,
        )

        confirm_url = reverse("playbook_delete_confirm", kwargs={"pk": playbook.pk})
        response = client.get(confirm_url)

        assert response.status_code == 200
        content = response.content.decode("utf-8")

        assert "Delete Playbook?" in content
        assert "Modal Target Playbook" in content
        assert 'data-testid="playbook-delete-modal"' in content
        assert 'data-testid="playbook-delete-confirm-button"' in content

    def test_delete_confirm_redirects_for_non_owned_or_downloaded_playbook(self, client):
        owner = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="SecurePass123",
        )
        other_user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(other_user)

        playbook = Playbook.objects.create(
            name="Downloaded Modal Target",
            description="Downloaded from Homebase",
            category="development",
            tags=[],
            visibility="private",
            status="disabled",
            version=1,
            source="downloaded",
            author=owner,
        )

        confirm_url = reverse("playbook_delete_confirm", kwargs={"pk": playbook.pk})
        response = client.get(confirm_url, follow=True)

        # Should not render modal for non-owned/downloaded playbook
        assert response.status_code == 200
        content = response.content.decode("utf-8")
        assert 'data-testid="playbook-delete-modal"' not in content

    def test_modal_shows_family_warning_for_shared_playbook(self, client):
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(user)

        playbook = Playbook.objects.create(
            name="Family Shared Playbook",
            description="Shared with family",
            category="development",
            tags=[],
            visibility="family",
            status="disabled",
            version=1,
            source="owned",
            author=user,
        )

        confirm_url = reverse("playbook_delete_confirm", kwargs={"pk": playbook.pk})
        response = client.get(confirm_url)

        assert response.status_code == 200
        content = response.content.decode("utf-8")
        assert "shared with your family" in content
        assert "will lose access after next sync" in content

    def test_modal_shows_active_warning_for_active_playbook(self, client):
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(user)

        playbook = Playbook.objects.create(
            name="Active Playbook",
            description="Currently active",
            category="development",
            tags=[],
            visibility="private",
            status="active",
            version=1,
            source="owned",
            author=user,
        )

        confirm_url = reverse("playbook_delete_confirm", kwargs={"pk": playbook.pk})
        response = client.get(confirm_url)

        assert response.status_code == 200
        content = response.content.decode("utf-8")
        assert "This playbook is currently Active" in content
        assert "Consider disabling it first" in content

    def test_modal_shows_generic_impact_statement_for_related_data(self, client):
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(user)

        playbook = Playbook.objects.create(
            name="Impact Target Playbook",
            description="Has related entities",
            category="development",
            tags=[],
            visibility="private",
            status="disabled",
            version=1,
            source="owned",
            author=user,
        )

        confirm_url = reverse("playbook_delete_confirm", kwargs={"pk": playbook.pk})
        response = client.get(confirm_url)

        assert response.status_code == 200
        content = response.content.decode("utf-8")
        assert "All workflows, activities, artifacts, roles, howtos and version history" in content

    def test_delete_via_list_removes_playbook_from_list(self, client):
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(user)

        playbook = Playbook.objects.create(
            name="List Delete Target",
            description="Should disappear from list after delete",
            category="development",
            tags=[],
            visibility="private",
            status="disabled",
            version=1,
            source="owned",
            author=user,
        )

        # Sanity check: playbook appears in the list before deletion
        list_url = reverse("playbook_list")
        response_before = client.get(list_url)
        assert response_before.status_code == 200
        content_before = response_before.content.decode("utf-8")
        assert "List Delete Target" in content_before

        # Perform delete
        delete_url = reverse("playbook_delete", kwargs={"pk": playbook.pk})
        client.post(delete_url, follow=True)

        # After deletion the playbook should no longer be rendered in the list
        response_after = client.get(list_url)
        assert response_after.status_code == 200
        content_after = response_after.content.decode("utf-8")
        assert "List Delete Target" not in content_after


@pytest.mark.django_db
class TestPlaybookDeleteListUI:
    """UI tests for delete control on playbook list page (simple POST, no modal)."""

    def test_list_page_shows_delete_button_for_owned_playbook(self, client):
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="SecurePass123",
        )
        client.force_login(user)

        playbook = Playbook.objects.create(
            name="List Deletable Playbook",
            description="To be deleted via list page",
            category="development",
            tags=[],
            visibility="private",
            status="disabled",
            version=1,
            source="owned",
            author=user,
        )

        list_url = reverse("playbook_list")
        response = client.get(list_url)

        assert response.status_code == 200
        content = response.content.decode("utf-8")

        delete_url = reverse("playbook_delete", kwargs={"pk": playbook.pk})
        assert delete_url in content
        assert "Delete" in content
