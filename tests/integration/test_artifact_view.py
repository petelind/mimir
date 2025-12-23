"""
Integration tests for Artifact VIEW operation.

Tests artifact detail page display and navigation.
"""

import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from methodology.models import Playbook, Workflow, Activity, Artifact, ArtifactInput

User = get_user_model()


@pytest.mark.django_db
class TestArtifactView:
    """Integration tests for artifact view functionality."""

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

        self.consumer = Activity.objects.create(
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

    def test_art_view_01_open_artifact_detail_page(self):
        """ART-VIEW-01: Open artifact detail page."""
        url = reverse("artifact_detail", kwargs={"pk": self.artifact.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        assert b'data-testid="artifact-detail"' in response.content
        assert self.artifact.name.encode() in response.content

    def test_art_view_02_view_header_information(self):
        """ART-VIEW-02: View header information."""
        url = reverse("artifact_detail", kwargs={"pk": self.artifact.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        assert b'data-testid="artifact-name"' in response.content
        assert self.artifact.name.encode() in response.content
        assert b"Required" in response.content  # Badge for is_required
        assert self.artifact.type.encode() in response.content

    def test_art_view_03_view_description(self):
        """ART-VIEW-03: View description."""
        url = reverse("artifact_detail", kwargs={"pk": self.artifact.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        assert b'data-testid="artifact-description"' in response.content
        assert self.artifact.description.encode() in response.content

    def test_art_view_04_view_associated_activities(self):
        """ART-VIEW-04: View associated activities."""
        # Add artifact as input to consumer activity
        ArtifactInput.objects.create(
            artifact=self.artifact, activity=self.consumer, is_required=True
        )

        url = reverse("artifact_detail", kwargs={"pk": self.artifact.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        assert b'data-testid="consumers-list"' in response.content
        assert self.consumer.name.encode() in response.content

    def test_art_view_05_view_template_file(self):
        """ART-VIEW-05: View template file."""
        # Note: This test would require actual file upload setup
        # For now, we test the display when template_file is None
        url = reverse("artifact_detail", kwargs={"pk": self.artifact.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        # Template file section should not be present when no file
        assert b'data-testid="template-info"' not in response.content

    def test_art_view_06_navigate_to_edit(self):
        """ART-VIEW-06: Navigate to edit."""
        url = reverse("artifact_detail", kwargs={"pk": self.artifact.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        assert b'data-testid="edit-btn"' in response.content
        edit_url = reverse("artifact_edit", kwargs={"pk": self.artifact.pk})
        assert edit_url.encode() in response.content

    def test_art_view_07_navigate_to_delete(self):
        """ART-VIEW-07: Navigate to delete."""
        # Note: Delete functionality not implemented yet
        # This test is a placeholder
        url = reverse("artifact_detail", kwargs={"pk": self.artifact.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        # For now, we just verify the page loads

    def test_art_view_08_view_artifact_producer_activity(self):
        """ART-VIEW-08: View artifact producer activity."""
        url = reverse("artifact_detail", kwargs={"pk": self.artifact.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        assert b'data-testid="producer-info"' in response.content
        assert self.producer.name.encode() in response.content

        # Check link to producer activity
        producer_url = reverse(
            "activity_detail",
            kwargs={
                "playbook_pk": self.playbook.pk,
                "workflow_pk": self.workflow.pk,
                "activity_pk": self.producer.pk,
            },
        )
        assert producer_url.encode() in response.content

    def test_art_view_09_view_artifact_consumer_activities(self):
        """ART-VIEW-09: View artifact consumer activities."""
        # Add multiple consumers
        consumer2 = Activity.objects.create(
            workflow=self.workflow,
            name="Test Component",
            guidance="Write tests",
            order=3,
        )

        ArtifactInput.objects.create(
            artifact=self.artifact, activity=self.consumer, is_required=True
        )

        ArtifactInput.objects.create(
            artifact=self.artifact, activity=consumer2, is_required=False
        )

        url = reverse("artifact_detail", kwargs={"pk": self.artifact.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        assert b'data-testid="consumers-list"' in response.content
        assert self.consumer.name.encode() in response.content
        assert consumer2.name.encode() in response.content

        # Check badges for required/optional
        assert b"Required" in response.content
        assert b"Optional" in response.content

    def test_view_breadcrumbs(self):
        """Test breadcrumbs navigation."""
        url = reverse("artifact_detail", kwargs={"pk": self.artifact.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        assert b"breadcrumb" in response.content
        assert self.playbook.name.encode() in response.content

    def test_view_metadata_card(self):
        """Test metadata card displays correct information."""
        url = reverse("artifact_detail", kwargs={"pk": self.artifact.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        assert b"Metadata" in response.content
        assert self.artifact.type.encode() in response.content
        # Required badge should appear
        assert b"Yes" in response.content or b"Required" in response.content
