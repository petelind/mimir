"""
Integration tests for Artifact CREATE operation.

Tests artifact creation form, validation, and success scenarios.
"""

import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from methodology.models import Playbook, Workflow, Activity, Artifact

User = get_user_model()


@pytest.mark.django_db
class TestArtifactCreate:
    """Integration tests for artifact create functionality."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test data for each test."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="maria_test", email="maria@test.com", password="testpass123"
        )
        self.client.login(username="maria_test", password="testpass123")

        # Create playbook, workflow, and activity
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

        self.activity = Activity.objects.create(
            workflow=self.workflow,
            name="Design Component",
            guidance="Create UI design",
            order=1,
        )

    def test_art_create_01_open_create_form(self):
        """ART-CREATE-01: Open create artifact form."""
        url = reverse("artifact_create", kwargs={"playbook_pk": self.playbook.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        assert b"Create Artifact" in response.content
        assert b'data-testid="artifact-form"' in response.content
        assert b'data-testid="name-input"' in response.content
        assert b'data-testid="description-input"' in response.content
        assert b'data-testid="save-btn"' in response.content

    def test_art_create_02_create_artifact_successfully(self):
        """ART-CREATE-02: Create artifact successfully."""
        url = reverse("artifact_create", kwargs={"playbook_pk": self.playbook.pk})

        data = {
            "name": "API Specification",
            "description": "REST API contract with endpoints",
            "type": "Document",
            "produced_by": self.activity.pk,
        }
        response = self.client.post(url, data)

        # Should redirect to playbook detail on success
        assert response.status_code == 302
        assert response.url == reverse(
            "playbook_detail", kwargs={"pk": self.playbook.pk}
        )

        # Verify artifact was created
        artifact = Artifact.objects.get(name="API Specification")
        assert artifact.playbook == self.playbook
        assert artifact.produced_by == self.activity
        assert artifact.description == "REST API contract with endpoints"
        assert artifact.type == "Document"
        assert artifact.is_required is False

    def test_art_create_03_validate_required_fields(self):
        """ART-CREATE-03: Validate required fields."""
        url = reverse("artifact_create", kwargs={"playbook_pk": self.playbook.pk})

        # Missing name
        data = {
            "name": "",
            "description": "Test",
            "type": "Document",
            "produced_by": self.activity.pk,
        }
        response = self.client.post(url, data)

        assert response.status_code == 200
        assert (
            b"Artifact name cannot be empty" in response.content
            or b"This field is required" in response.content
        )
        assert Artifact.objects.count() == 0

    def test_art_create_04_select_artifact_type(self):
        """ART-CREATE-04: Select artifact type."""
        url = reverse("artifact_create", kwargs={"playbook_pk": self.playbook.pk})

        # Create artifacts with different types
        types_to_test = ["Document", "Template", "Code", "Diagram", "Data", "Other"]

        for artifact_type in types_to_test:
            data = {
                "name": f"{artifact_type} Artifact",
                "description": f"Test {artifact_type}",
                "type": artifact_type,
                "produced_by": self.activity.pk,
            }
            response = self.client.post(url, data)

            assert response.status_code == 302
            artifact = Artifact.objects.get(name=f"{artifact_type} Artifact")
            assert artifact.type == artifact_type

    def test_art_create_05_associate_with_activity(self):
        """ART-CREATE-05: Associate with activity."""
        # Create another activity
        activity2 = Activity.objects.create(
            workflow=self.workflow,
            name="Implement Component",
            guidance="Write code",
            order=2,
        )

        url = reverse("artifact_create", kwargs={"playbook_pk": self.playbook.pk})

        data = {
            "name": "Component Code",
            "description": "React component implementation",
            "type": "Code",
            "produced_by": activity2.pk,
        }
        response = self.client.post(url, data)

        assert response.status_code == 302
        artifact = Artifact.objects.get(name="Component Code")
        assert artifact.produced_by == activity2

    def test_art_create_06_mark_as_required(self):
        """ART-CREATE-06: Mark as required."""
        url = reverse("artifact_create", kwargs={"playbook_pk": self.playbook.pk})

        data = {
            "name": "Required Spec",
            "description": "Critical document",
            "type": "Document",
            "produced_by": self.activity.pk,
            "is_required": "on",
        }
        response = self.client.post(url, data)

        assert response.status_code == 302
        artifact = Artifact.objects.get(name="Required Spec")
        assert artifact.is_required is True

    def test_art_create_07_add_template_file(self):
        """ART-CREATE-07: Add template file."""
        # Note: File upload testing requires more complex setup
        # For now, we'll test the form accepts the field
        url = reverse("artifact_create", kwargs={"playbook_pk": self.playbook.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        assert b'data-testid="template-input"' in response.content

    def test_art_create_08_cancel_creation(self):
        """ART-CREATE-08: Cancel creation."""
        url = reverse("artifact_create", kwargs={"playbook_pk": self.playbook.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        # Check cancel button exists with correct link
        playbook_url = reverse("playbook_detail", kwargs={"pk": self.playbook.pk})
        assert playbook_url.encode() in response.content
        assert b'data-testid="cancel-btn"' in response.content

    def test_duplicate_name_validation(self):
        """Test validation error for duplicate artifact name in playbook."""
        # Create existing artifact
        Artifact.objects.create(
            playbook=self.playbook,
            produced_by=self.activity,
            name="Design Document",
            type="Document",
        )

        url = reverse("artifact_create", kwargs={"playbook_pk": self.playbook.pk})

        data = {
            "name": "Design Document",  # Duplicate
            "description": "New description",
            "type": "Document",
            "produced_by": self.activity.pk,
        }
        response = self.client.post(url, data)

        # Should stay on form with error
        assert response.status_code == 200
        assert b"already exists" in response.content

        # Only original artifact should exist
        assert Artifact.objects.count() == 1
