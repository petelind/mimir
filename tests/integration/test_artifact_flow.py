"""
Integration tests for Artifact FLOW operations.

Tests artifact producer/consumer relationships, flow visualization,
bulk operations, and validation.
"""

import pytest
import json
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from methodology.models import Playbook, Workflow, Activity, Artifact, ArtifactInput
from methodology.services.artifact_service import ArtifactService

User = get_user_model()


@pytest.mark.django_db
class TestProducerConsumer:
    """Test producer/consumer relationships (ART-FLOW-01 to ART-FLOW-06)."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test data for each test."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="maria_test", email="maria@test.com", password="testpass123"
        )
        self.client.login(username="maria_test", password="testpass123")

        # Create playbook and workflow
        self.playbook = Playbook.objects.create(
            name="React Frontend v1.2",
            description="Frontend development methodology",
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

        # Create activities in order
        self.design_activity = Activity.objects.create(
            workflow=self.workflow,
            name="Design Component API",
            guidance="Design the component API",
            order=1,
        )

        self.implement_activity = Activity.objects.create(
            workflow=self.workflow,
            name="Implement Component",
            guidance="Implement the component",
            order=2,
        )

        self.test_activity = Activity.objects.create(
            workflow=self.workflow,
            name="Test Component",
            guidance="Test the component",
            order=3,
        )

        self.document_activity = Activity.objects.create(
            workflow=self.workflow,
            name="Document Component",
            guidance="Document the component",
            order=4,
        )

    def test_art_flow_01_define_output(self):
        """ART-FLOW-01: Define artifact as output of activity."""
        # Create artifact with producer
        artifact = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.design_activity,
            name="Component API Specification",
            description="API contract",
            type="Document",
            is_required=True,
        )

        assert artifact.produced_by == self.design_activity
        assert artifact.name == "Component API Specification"
        assert artifact.playbook == self.playbook

        # Check artifact detail page shows producer
        url = reverse("artifact_detail", kwargs={"pk": artifact.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        assert b"Design Component API" in response.content
        assert b"producer-info" in response.content

    def test_art_flow_02_define_input(self):
        """ART-FLOW-02: Define artifact as input to downstream activity."""
        # Create artifact
        artifact = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.design_activity,
            name="Component API Specification",
            type="Document",
        )

        # Add as input to downstream activity
        artifact_input = ArtifactService.add_consumer(
            artifact, self.implement_activity, is_required=True
        )

        assert artifact_input.artifact == artifact
        assert artifact_input.activity == self.implement_activity
        assert artifact_input.is_required is True

        # Verify it appears in consumers list
        consumers = ArtifactService.get_artifact_consumers(artifact)
        assert consumers.count() == 1
        assert consumers.first().activity == self.implement_activity

    def test_art_flow_03_add_multiple_consumers(self):
        """ART-FLOW-03: Add multiple consumers for single artifact."""
        # Create artifact
        artifact = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.design_activity,
            name="Component API Specification",
            type="Document",
        )

        # Add multiple consumers
        ArtifactService.add_consumer(artifact, self.implement_activity, True)
        ArtifactService.add_consumer(artifact, self.test_activity, True)
        ArtifactService.add_consumer(artifact, self.document_activity, False)

        # Verify all consumers
        consumers = ArtifactService.get_artifact_consumers(artifact)
        assert consumers.count() == 3

        consumer_activities = [c.activity for c in consumers]
        assert self.implement_activity in consumer_activities
        assert self.test_activity in consumer_activities
        assert self.document_activity in consumer_activities

    def test_art_flow_04_view_artifact_flow(self):
        """ART-FLOW-04: View artifact flow through workflow."""
        # Create artifact with multiple consumers
        artifact = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.design_activity,
            name="Component API Specification",
            type="Document",
        )

        ArtifactService.add_consumer(artifact, self.implement_activity, True)
        ArtifactService.add_consumer(artifact, self.test_activity, True)
        ArtifactService.add_consumer(artifact, self.document_activity, False)

        # Get flow chain
        flow_chain = ArtifactService.get_flow_chain(artifact)

        assert flow_chain['artifact'] == artifact
        assert flow_chain['producer'] == self.design_activity
        assert len(flow_chain['consumers']) == 3
        
        # Verify consumer details
        consumer_map = {c['activity']: c['required'] for c in flow_chain['consumers']}
        assert consumer_map[self.implement_activity] is True
        assert consumer_map[self.test_activity] is True
        assert consumer_map[self.document_activity] is False

    def test_art_flow_05_view_workflow_flow_visualization(self):
        """ART-FLOW-05: View workflow with artifact flow visualization."""
        # Create artifacts with flow
        api_spec = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.design_activity,
            name="Component API Specification",
            type="Document",
        )

        component_code = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.implement_activity,
            name="Component Code",
            type="Code",
        )

        # Add consumers
        ArtifactService.add_consumer(api_spec, self.implement_activity, True)
        ArtifactService.add_consumer(component_code, self.test_activity, True)
        ArtifactService.add_consumer(api_spec, self.test_activity, True)

        # Generate flow data
        flow_data = ArtifactService.generate_flow_data(self.playbook)

        # Verify nodes and edges
        assert len(flow_data['nodes']) > 0
        assert len(flow_data['edges']) > 0

        # Verify flow diagram page
        url = reverse("artifact_flow_diagram", kwargs={"playbook_id": self.playbook.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        assert b"flow-diagram" in response.content

    def test_art_flow_06_prevent_circular_dependency(self):
        """ART-FLOW-06: Prevent circular artifact dependencies."""
        # Create artifact produced by implement activity
        artifact = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.implement_activity,
            name="Component Code",
            type="Code",
        )

        # Try to add as input to its own producer - should fail
        with pytest.raises(ValidationError) as exc_info:
            ArtifactService.add_consumer(artifact, self.implement_activity, True)

        assert "Circular dependency" in str(exc_info.value)


@pytest.mark.django_db
class TestValidation:
    """Test flow validation (ART-FLOW-07 to ART-FLOW-10)."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test data for each test."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="maria_test", email="maria@test.com", password="testpass123"
        )
        self.client.login(username="maria_test", password="testpass123")

        self.playbook = Playbook.objects.create(
            name="React Frontend v1.2",
            category="development",
            status="active",
            source="owned",
            author=self.user,
        )

        self.workflow = Workflow.objects.create(
            name="Component Development",
            playbook=self.playbook,
            order=1,
        )

        self.activity1 = Activity.objects.create(
            workflow=self.workflow, name="Design", order=1
        )

        self.activity2 = Activity.objects.create(
            workflow=self.workflow, name="Implement", order=2
        )

    def test_art_flow_07_temporal_ordering_warning(self):
        """ART-FLOW-07: Warn about temporal ordering issues."""
        # Create artifact produced by later activity (order 2)
        artifact = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.activity2,
            name="Component Code",
            type="Code",
        )

        # Validate flow to earlier activity (order 1) - should warn
        validation = ArtifactService.validate_flow(artifact, self.activity1)

        assert validation['valid'] is True
        assert len(validation['warnings']) > 0
        assert any('Temporal ordering' in w for w in validation['warnings'])

    def test_art_flow_08_allow_same_artifact_multiple_consumers(self):
        """ART-FLOW-08: Allow same artifact to multiple consumers."""
        artifact = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.activity1,
            name="API Spec",
            type="Document",
        )

        # Add same artifact to multiple consumers - should succeed
        input1 = ArtifactService.add_consumer(artifact, self.activity2, True)

        # Create another activity and add same artifact
        activity3 = Activity.objects.create(
            workflow=self.workflow, name="Test", order=3
        )
        input2 = ArtifactService.add_consumer(artifact, activity3, True)

        assert input1.artifact == input2.artifact
        assert artifact.get_consumer_count() == 2

    def test_art_flow_09_prevent_duplicate_input(self):
        """ART-FLOW-09: Prevent duplicate input."""
        artifact = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.activity1,
            name="API Spec",
            type="Document",
        )

        # Add as input once
        ArtifactService.add_consumer(artifact, self.activity2, True)

        # Try to add again - should fail
        with pytest.raises(ValidationError) as exc_info:
            ArtifactService.add_consumer(artifact, self.activity2, True)

        assert "already an input" in str(exc_info.value)

    def test_art_flow_10_validate_no_warnings_for_correct_order(self):
        """ART-FLOW-10: No warnings for correct temporal ordering."""
        # Create artifact produced by earlier activity (order 1)
        artifact = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.activity1,
            name="API Spec",
            type="Document",
        )

        # Validate flow to later activity (order 2) - no warnings
        validation = ArtifactService.validate_flow(artifact, self.activity2)

        assert validation['valid'] is True
        assert len(validation['warnings']) == 0


@pytest.mark.django_db
class TestActivityInputManagement:
    """Test activity input management (ART-FLOW-11 to ART-FLOW-19)."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test data for each test."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="maria_test", email="maria@test.com", password="testpass123"
        )
        self.client.login(username="maria_test", password="testpass123")

        self.playbook = Playbook.objects.create(
            name="React Frontend v1.2",
            category="development",
            status="active",
            source="owned",
            author=self.user,
        )

        self.workflow = Workflow.objects.create(
            name="Component Development",
            playbook=self.playbook,
            order=1,
        )

        self.design_activity = Activity.objects.create(
            workflow=self.workflow, name="Design", order=1
        )

        self.implement_activity = Activity.objects.create(
            workflow=self.workflow, name="Implement", order=2
        )

        # Create some artifacts
        self.api_spec = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.design_activity,
            name="API Spec",
            type="Document",
        )

        self.design_mockups = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.design_activity,
            name="Design Mockups",
            type="Diagram",
        )

    def test_art_flow_11_mark_input_as_required(self):
        """ART-FLOW-11: Mark artifact input as required."""
        artifact_input = ArtifactService.add_consumer(
            self.api_spec, self.implement_activity, is_required=True
        )

        assert artifact_input.is_required is True

        # Verify in activity inputs
        inputs = ArtifactService.get_activity_inputs(self.implement_activity)
        assert inputs.count() == 1
        assert inputs.first().is_required is True

    def test_art_flow_12_mark_input_as_optional(self):
        """ART-FLOW-12: Mark artifact input as optional."""
        artifact_input = ArtifactService.add_consumer(
            self.design_mockups, self.implement_activity, is_required=False
        )

        assert artifact_input.is_required is False

    def test_art_flow_13_view_inputs(self):
        """ART-FLOW-13: View activity's input artifacts."""
        # Add inputs
        ArtifactService.add_consumer(self.api_spec, self.implement_activity, True)
        ArtifactService.add_consumer(self.design_mockups, self.implement_activity, False)

        # View manage inputs page
        url = reverse(
            "activity_manage_inputs", kwargs={"activity_id": self.implement_activity.pk}
        )
        response = self.client.get(url)

        assert response.status_code == 200
        assert b"manage-inputs" in response.content
        assert b"API Spec" in response.content
        assert b"Design Mockups" in response.content

    def test_art_flow_14_change_required_to_optional(self):
        """ART-FLOW-14: Change artifact input from required to optional."""
        artifact_input = ArtifactService.add_consumer(
            self.api_spec, self.implement_activity, is_required=True
        )

        assert artifact_input.is_required is True

        # Toggle via endpoint
        url = reverse(
            "artifact_toggle_input_required", kwargs={"input_id": artifact_input.pk}
        )
        response = self.client.post(url)

        # Reload from database
        artifact_input.refresh_from_db()
        assert artifact_input.is_required is False

    def test_art_flow_15_remove_input(self):
        """ART-FLOW-15: Remove artifact as input from activity."""
        artifact_input = ArtifactService.add_consumer(
            self.design_mockups, self.implement_activity, False
        )

        # Remove input
        ArtifactService.remove_artifact_input(artifact_input.pk)

        # Verify removed
        assert not ArtifactInput.objects.filter(pk=artifact_input.pk).exists()

        # Verify not in inputs
        inputs = ArtifactService.get_activity_inputs(self.implement_activity)
        assert inputs.count() == 0

    def test_art_flow_16_view_available_artifacts(self):
        """ART-FLOW-16: View available artifacts for input."""
        # Add one artifact as input
        ArtifactService.add_consumer(self.api_spec, self.implement_activity, True)

        # Get available artifacts (should exclude api_spec and any produced by implement_activity)
        available = ArtifactService.get_available_inputs(self.implement_activity)

        # Should include design_mockups but not api_spec
        artifact_ids = [a.id for a in available]
        assert self.design_mockups.id in artifact_ids
        assert self.api_spec.id not in artifact_ids

    def test_art_flow_17_navigate_from_activity_to_input(self):
        """ART-FLOW-17: Navigate from activity to input artifact."""
        ArtifactService.add_consumer(self.api_spec, self.implement_activity, True)

        # View manage inputs page
        url = reverse(
            "activity_manage_inputs", kwargs={"activity_id": self.implement_activity.pk}
        )
        response = self.client.get(url)

        # Should have link to artifact detail
        artifact_url = reverse("artifact_detail", kwargs={"pk": self.api_spec.pk})
        assert artifact_url.encode() in response.content

    def test_art_flow_18_view_activity_outputs(self):
        """ART-FLOW-18: View activity outputs on activity detail page."""
        # api_spec is output of design_activity
        assert self.api_spec.produced_by == self.design_activity

        # Get artifacts for activity
        outputs = ArtifactService.get_artifacts_for_activity(self.design_activity)
        assert outputs.count() == 2
        assert self.api_spec in outputs
        assert self.design_mockups in outputs

    def test_art_flow_19_get_activity_inputs_list(self):
        """ART-FLOW-19: Get activity inputs list."""
        # Add inputs
        ArtifactService.add_consumer(self.api_spec, self.implement_activity, True)
        ArtifactService.add_consumer(self.design_mockups, self.implement_activity, False)

        # Get inputs
        inputs = ArtifactService.get_activity_inputs(self.implement_activity)
        assert inputs.count() == 2

        input_artifacts = [inp.artifact for inp in inputs]
        assert self.api_spec in input_artifacts
        assert self.design_mockups in input_artifacts


@pytest.mark.django_db
class TestBulkOperations:
    """Test bulk operations (ART-FLOW-20 to ART-FLOW-21)."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test data for each test."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="maria_test", email="maria@test.com", password="testpass123"
        )
        self.client.login(username="maria_test", password="testpass123")

        self.playbook = Playbook.objects.create(
            name="React Frontend v1.2",
            category="development",
            status="active",
            source="owned",
            author=self.user,
        )

        self.workflow = Workflow.objects.create(
            name="Component Development",
            playbook=self.playbook,
            order=1,
        )

        self.design_activity = Activity.objects.create(
            workflow=self.workflow, name="Design", order=1
        )

        self.test_activity = Activity.objects.create(
            workflow=self.workflow, name="Test", order=2
        )

        self.document_activity = Activity.objects.create(
            workflow=self.workflow, name="Document", order=3
        )

        # Create artifacts
        self.artifact1 = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.design_activity,
            name="Component Code",
            type="Code",
        )

        self.artifact2 = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.design_activity,
            name="API Spec",
            type="Document",
        )

        self.artifact3 = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.design_activity,
            name="Test Data",
            type="Data",
        )

    def test_art_flow_20_add_multiple_inputs(self):
        """ART-FLOW-20: Add multiple artifacts as inputs at once."""
        # Use bulk add endpoint
        url = reverse(
            "activity_bulk_add_inputs", kwargs={"activity_id": self.test_activity.pk}
        )

        data = {
            "artifact_ids": [self.artifact1.pk, self.artifact2.pk, self.artifact3.pk],
            "all_required": "true",
        }

        response = self.client.post(url, data)

        # Verify redirect
        assert response.status_code == 302

        # Verify all added
        inputs = ArtifactService.get_activity_inputs(self.test_activity)
        assert inputs.count() == 3

        # Verify all marked as required
        for inp in inputs:
            assert inp.is_required is True

    def test_art_flow_21_copy_inputs_from_another_activity(self):
        """ART-FLOW-21: Copy artifact inputs from another activity."""
        # Add inputs to test activity
        ArtifactService.add_consumer(self.artifact1, self.test_activity, True)
        ArtifactService.add_consumer(self.artifact2, self.test_activity, True)

        # Copy to document activity
        url = reverse(
            "activity_copy_inputs", kwargs={"activity_id": self.document_activity.pk}
        )

        data = {"source_activity_id": self.test_activity.pk}

        response = self.client.post(url, data)

        # Verify redirect
        assert response.status_code == 302

        # Verify inputs copied
        inputs = ArtifactService.get_activity_inputs(self.document_activity)
        assert inputs.count() == 2

        input_artifacts = [inp.artifact for inp in inputs]
        assert self.artifact1 in input_artifacts
        assert self.artifact2 in input_artifacts


@pytest.mark.django_db
class TestReporting:
    """Test reporting and visualization (ART-FLOW-22 to ART-FLOW-25)."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test data for each test."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="maria_test", email="maria@test.com", password="testpass123"
        )
        self.client.login(username="maria_test", password="testpass123")

        self.playbook = Playbook.objects.create(
            name="React Frontend v1.2",
            category="development",
            status="active",
            source="owned",
            author=self.user,
        )

        self.workflow = Workflow.objects.create(
            name="Component Development",
            playbook=self.playbook,
            order=1,
        )

        self.activity1 = Activity.objects.create(
            workflow=self.workflow, name="Design", order=1
        )

        self.activity2 = Activity.objects.create(
            workflow=self.workflow, name="Implement", order=2
        )

        self.activity3 = Activity.objects.create(
            workflow=self.workflow, name="Test", order=3
        )

    def test_art_flow_22_view_dependency_graph(self):
        """ART-FLOW-22: View playbook artifact dependency graph."""
        # Create artifacts with flows
        artifact1 = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.activity1,
            name="Design Doc",
            type="Document",
        )

        artifact2 = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.activity2,
            name="Component Code",
            type="Code",
        )

        ArtifactService.add_consumer(artifact1, self.activity2, True)
        ArtifactService.add_consumer(artifact2, self.activity3, True)

        # View flow diagram
        url = reverse("artifact_flow_diagram", kwargs={"playbook_id": self.playbook.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        assert b"Flow Diagram" in response.content

    def test_art_flow_23_generate_flow_data(self):
        """ART-FLOW-23: Generate flow data structure."""
        # Create artifacts with flows
        artifact = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.activity1,
            name="Design Doc",
            type="Document",
        )

        ArtifactService.add_consumer(artifact, self.activity2, True)
        ArtifactService.add_consumer(artifact, self.activity3, False)

        # Generate flow data
        flow_data = ArtifactService.generate_flow_data(self.playbook)

        # Verify structure
        assert 'nodes' in flow_data
        assert 'edges' in flow_data
        assert len(flow_data['nodes']) > 0
        assert len(flow_data['edges']) > 0

        # Verify nodes include activities and artifacts
        node_types = {node['type'] for node in flow_data['nodes']}
        assert 'activity' in node_types
        assert 'artifact' in node_types

        # Verify edges have correct structure
        for edge in flow_data['edges']:
            assert 'from' in edge
            assert 'to' in edge
            assert 'type' in edge

    def test_art_flow_24_identify_orphaned_artifacts(self):
        """ART-FLOW-24: Identify orphaned artifacts."""
        # Create artifact with no consumers
        orphaned = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.activity1,
            name="Old Design Doc",
            type="Document",
        )

        # Create artifact with consumers
        used = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.activity1,
            name="Active Doc",
            type="Document",
        )
        ArtifactService.add_consumer(used, self.activity2, True)

        # Check consumer counts
        assert orphaned.get_consumer_count() == 0
        assert used.get_consumer_count() == 1

    def test_art_flow_25_flow_chain_completeness(self):
        """ART-FLOW-25: Verify flow chain returns complete data."""
        # Create artifact with multiple consumers
        artifact = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.activity1,
            name="Design Doc",
            type="Document",
        )

        ArtifactService.add_consumer(artifact, self.activity2, True)
        ArtifactService.add_consumer(artifact, self.activity3, False)

        # Get flow chain
        flow_chain = ArtifactService.get_flow_chain(artifact)

        # Verify completeness
        assert 'artifact' in flow_chain
        assert 'producer' in flow_chain
        assert 'consumers' in flow_chain

        assert flow_chain['artifact'] == artifact
        assert flow_chain['producer'] == self.activity1
        assert len(flow_chain['consumers']) == 2

        # Verify consumer details
        for consumer in flow_chain['consumers']:
            assert 'activity' in consumer
            assert 'required' in consumer
            assert 'input_id' in consumer


@pytest.mark.django_db
class TestIntegration:
    """Test integration scenarios (ART-FLOW-26 to ART-FLOW-28)."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test data for each test."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="maria_test", email="maria@test.com", password="testpass123"
        )
        self.client.login(username="maria_test", password="testpass123")

        self.playbook = Playbook.objects.create(
            name="React Frontend v1.2",
            category="development",
            status="active",
            source="owned",
            author=self.user,
        )

        self.workflow = Workflow.objects.create(
            name="Component Development",
            playbook=self.playbook,
            order=1,
        )

        self.activity1 = Activity.objects.create(
            workflow=self.workflow, name="Design", order=1
        )

        self.activity2 = Activity.objects.create(
            workflow=self.workflow, name="Implement", order=2
        )

        self.activity3 = Activity.objects.create(
            workflow=self.workflow, name="Test", order=3
        )

    def test_art_flow_26_create_artifact_with_producer(self):
        """ART-FLOW-26: Create artifact with producer from activity detail page."""
        # This is already covered by create tests, verify service method works
        artifact = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.activity1,
            name="Design Output",
            type="Document",
        )

        assert artifact.produced_by == self.activity1
        assert artifact.playbook == self.playbook

    def test_art_flow_27_view_artifact_flow_from_detail(self):
        """ART-FLOW-27: View artifact flow from artifact detail page."""
        # Create artifact with consumers
        artifact = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.activity1,
            name="Component Code",
            type="Code",
        )

        ArtifactService.add_consumer(artifact, self.activity2, True)
        ArtifactService.add_consumer(artifact, self.activity3, False)

        # View artifact detail
        url = reverse("artifact_detail", kwargs={"pk": artifact.pk})
        response = self.client.get(url)

        assert response.status_code == 200
        assert b"Consumer Activities" in response.content
        assert b"Implement" in response.content
        assert b"Test" in response.content

    def test_art_flow_28_delete_artifact_with_consumers_shows_warning(self):
        """ART-FLOW-28: Delete artifact with consumers shows warning."""
        # Create artifact with multiple consumers
        artifact = ArtifactService.create_artifact(
            playbook=self.playbook,
            produced_by=self.activity1,
            name="Component Code",
            type="Code",
        )

        ArtifactService.add_consumer(artifact, self.activity2, True)
        ArtifactService.add_consumer(artifact, self.activity3, True)

        # Get delete modal
        url = reverse("artifact_delete", kwargs={"pk": artifact.pk})
        response = self.client.get(url)

        # Should show consumer count
        assert response.status_code == 200
        assert b"consumer" in response.content.lower()

        # Delete should cascade
        result = ArtifactService.delete_artifact(artifact.pk)
        assert result['deleted'] is True
        assert result['consumers_cleared'] == 2
