"""
Integration tests for Artifact EDIT operation.

Tests artifact edit form, validation, and update scenarios.
"""

import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from methodology.models import Playbook, Workflow, Activity, Artifact

User = get_user_model()


@pytest.mark.django_db
class TestArtifactEdit:
    """Integration tests for artifact edit functionality."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test data for each test."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="maria_test", email="maria@test.com", password="testpass123"
        )
        self.client.login(username="maria_test", password="testpass123")

        # Create playbook, workflow, and activities
        self.playbook = Playbook.objects.create(
            name="React Frontend Development",
            description="A comprehensive methodology",
            category="development",
            status="active",
            source="owned",
            author=self.user,
        )

        self.workflow = Workflow.objects.create(
            name="Component Development",
            description="Develop React components",
            playbook=self.playbook,
            order=1,
        )

        self.producer = Activity.objects.create(
            workflow=self.workflow,
            name="Design Component",
            guidance="Create UI design",
            order=1,
        )

        self.producer2 = Activity.objects.create(
            workflow=self.workflow,
            name="Implement Component",
            guidance="Write code",
            order=2,
        )

        # Create artifact
        self.artifact = Artifact.objects.create(
            playbook=self.playbook,
            produced_by=self.producer,
            name="API Specification",
            description="REST API contract with endpoints",
            type="Document",
            is_required=True,
        )

    def test_art_edit_01_open_edit_form(self):
        """ART-EDIT-01: Open edit form."""
        url = reverse("artifact_edit", kwargs={"pk": self.artifact.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        assert b"Edit Artifact" in response.content
        assert b'data-testid="artifact-form"' in response.content
        assert b'data-testid="name-input"' in response.content
        assert b'data-testid="save-btn"' in response.content

        # Verify form is pre-populated
        assert self.artifact.name.encode() in response.content
        assert self.artifact.description.encode() in response.content

    def test_art_edit_02_edit_name(self):
        """ART-EDIT-02: Edit name."""
        url = reverse("artifact_edit", kwargs={"pk": self.artifact.pk})

        data = {
            "name": "Updated API Specification",
            "description": self.artifact.description,
            "type": self.artifact.type,
            "produced_by": self.producer.pk,
        }
        response = self.client.post(url, data)

        # Should redirect to detail on success
        assert response.status_code == 302
        assert response.url == reverse(
            "artifact_detail", kwargs={"pk": self.artifact.pk}
        )

        # Verify artifact was updated
        self.artifact.refresh_from_db()
        assert self.artifact.name == "Updated API Specification"

    def test_art_edit_03_edit_description(self):
        """ART-EDIT-03: Edit description."""
        url = reverse("artifact_edit", kwargs={"pk": self.artifact.pk})

        data = {
            "name": self.artifact.name,
            "description": "Updated comprehensive REST API documentation",
            "type": self.artifact.type,
            "produced_by": self.producer.pk,
        }
        response = self.client.post(url, data)

        assert response.status_code == 302

        # Verify description was updated
        self.artifact.refresh_from_db()
        assert (
            self.artifact.description == "Updated comprehensive REST API documentation"
        )

    def test_art_edit_04_change_type(self):
        """ART-EDIT-04: Change type."""
        url = reverse("artifact_edit", kwargs={"pk": self.artifact.pk})

        data = {
            "name": self.artifact.name,
            "description": self.artifact.description,
            "type": "Template",
            "produced_by": self.producer.pk,
        }
        response = self.client.post(url, data)

        assert response.status_code == 302

        # Verify type was changed
        self.artifact.refresh_from_db()
        assert self.artifact.type == "Template"

    def test_art_edit_05_toggle_required_status(self):
        """ART-EDIT-05: Toggle required status."""
        url = reverse("artifact_edit", kwargs={"pk": self.artifact.pk})

        # Initially required=True, toggle to False
        data = {
            "name": self.artifact.name,
            "description": self.artifact.description,
            "type": self.artifact.type,
            "produced_by": self.producer.pk,
            # is_required not included = False (unchecked)
        }
        response = self.client.post(url, data)

        assert response.status_code == 302

        # Verify required was toggled
        self.artifact.refresh_from_db()
        assert self.artifact.is_required is False

        # Toggle back to True
        data["is_required"] = "on"
        response = self.client.post(url, data)

        self.artifact.refresh_from_db()
        assert self.artifact.is_required is True

    def test_art_edit_06_change_activity_association(self):
        """ART-EDIT-06: Change activity association."""
        url = reverse("artifact_edit", kwargs={"pk": self.artifact.pk})

        data = {
            "name": self.artifact.name,
            "description": self.artifact.description,
            "type": self.artifact.type,
            "produced_by": self.producer2.pk,  # Change to different activity
        }
        response = self.client.post(url, data)

        assert response.status_code == 302

        # Verify producer was changed
        self.artifact.refresh_from_db()
        assert self.artifact.produced_by == self.producer2

    def test_art_edit_07_update_template_file(self):
        """ART-EDIT-07: Update template file."""
        # Note: File upload testing requires more complex setup
        # For now, we'll test the form accepts the field
        url = reverse("artifact_edit", kwargs={"pk": self.artifact.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        assert b'data-testid="template-input"' in response.content

    def test_art_edit_08_cancel_edit(self):
        """ART-EDIT-08: Cancel edit."""
        url = reverse("artifact_edit", kwargs={"pk": self.artifact.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        # Check cancel button exists with correct link
        detail_url = reverse("artifact_detail", kwargs={"pk": self.artifact.pk})
        assert detail_url.encode() in response.content
        assert b'data-testid="cancel-btn"' in response.content

    def test_validate_required_name(self):
        """Test validation error when name is missing."""
        url = reverse("artifact_edit", kwargs={"pk": self.artifact.pk})

        data = {
            "name": "",  # Empty name
            "description": self.artifact.description,
            "type": self.artifact.type,
            "produced_by": self.producer.pk,
        }
        response = self.client.post(url, data)

        # Should stay on form with error
        assert response.status_code == 200
        assert (
            b"Artifact name cannot be empty" in response.content
            or b"This field is required" in response.content
        )

        # Artifact should not be modified
        self.artifact.refresh_from_db()
        assert self.artifact.name == "API Specification"

    def test_duplicate_name_validation(self):
        """Test validation error for duplicate artifact name."""
        # Create another artifact
        Artifact.objects.create(
            playbook=self.playbook,
            produced_by=self.producer,
            name="Design Document",
            type="Document",
        )

        url = reverse("artifact_edit", kwargs={"pk": self.artifact.pk})

        data = {
            "name": "Design Document",  # Duplicate
            "description": self.artifact.description,
            "type": self.artifact.type,
            "produced_by": self.producer.pk,
        }
        response = self.client.post(url, data)

        # Should stay on form with error
        assert response.status_code == 200
        assert b"already exists" in response.content

        # Artifact should not be modified
        self.artifact.refresh_from_db()
        assert self.artifact.name == "API Specification"

    def test_breadcrumbs_in_edit(self):
        """Test breadcrumbs navigation in edit form."""
        url = reverse("artifact_edit", kwargs={"pk": self.artifact.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        assert b"breadcrumb" in response.content
        assert self.playbook.name.encode() in response.content
        assert self.artifact.name.encode() in response.content
