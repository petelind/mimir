"""End-to-end test for the complete playbook creation wizard."""

import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from methodology.models import Playbook, Category, Visibility, Status, Workflow


class TestPlaybookWizardE2E(TestCase):
    """End-to-end tests for the complete playbook creation wizard."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
        self.client.login(username='testuser', password='testpass')

    def test_complete_wizard_flow_with_workflows(self):
        """Test complete wizard flow from Step 1 to Step 3 with workflows."""
        # Step 1: Basic Information
        response = self.client.post(reverse('playbook_create_step1'), {
            'name': 'Complete Test Playbook',
            'description': 'A comprehensive playbook for testing the complete wizard flow',
            'category': Category.DEVELOPMENT,
            'visibility': Visibility.PRIVATE,
            'tags': 'testing,complete,wizard',
            'action': 'next',
        })
        
        # Should redirect to Step 2
        self.assertRedirects(response, reverse('playbook_create_step2'))
        
        # Verify Step 1 data is in session
        session = self.client.session
        step1_data = session.get('playbook_wizard_step1')
        self.assertIsNotNone(step1_data)
        self.assertEqual(step1_data['name'], 'Complete Test Playbook')
        
        # Step 2: Add Workflows
        # Add first workflow
        response = self.client.post(reverse('playbook_create_step2'), {
            'action': 'add_workflow',
            'workflow_name': 'Discovery Phase',
            'workflow_description': 'Initial research and validation activities',
        })
        
        # Should stay on Step 2 after adding workflow
        self.assertEqual(response.status_code, 200)
        
        # Add second workflow
        response = self.client.post(reverse('playbook_create_step2'), {
            'action': 'add_workflow',
            'workflow_name': 'Design Process',
            'workflow_description': 'Design and prototyping activities',
        })
        
        # Should stay on Step 2 after adding workflow
        self.assertEqual(response.status_code, 200)
        
        # Continue to Step 3
        response = self.client.post(reverse('playbook_create_step2'), {
            'action': 'continue',
        })
        
        # Should redirect to Step 3
        self.assertRedirects(response, reverse('playbook_create_step3'))
        
        # Verify Step 2 data is in session
        session = self.client.session
        step2_data = session.get('playbook_wizard_step2')
        self.assertIsNotNone(step2_data)
        self.assertFalse(step2_data['skip_workflows'])
        self.assertEqual(len(step2_data['workflows']), 2)
        
        # Step 3: Publishing Settings
        response = self.client.post(reverse('playbook_create_step3'), {
            'status': Status.ACTIVE,
        })
        
        # Should redirect to playbook detail
        self.assertRedirects(response, reverse('playbook_detail', kwargs={'playbook_id': 1}))
        
        # Verify playbook was created
        playbook = Playbook.objects.get(id=1)
        self.assertEqual(playbook.name, 'Complete Test Playbook')
        self.assertEqual(playbook.description, 'A comprehensive playbook for testing the complete wizard flow')
        self.assertEqual(playbook.category, Category.DEVELOPMENT)
        self.assertEqual(playbook.visibility, Visibility.PRIVATE)
        self.assertEqual(playbook.status, Status.ACTIVE)
        self.assertEqual(playbook.created_by, self.user)
        # Tags are stored as a list in the JSONField
        self.assertEqual(playbook.tags, ['testing', 'complete', 'wizard'])
        
        # Verify workflows were created
        workflows = Workflow.objects.filter(playbook=playbook).order_by('order')
        self.assertEqual(len(workflows), 2)
        self.assertEqual(workflows[0].name, 'Discovery Phase')
        self.assertEqual(workflows[0].description, 'Initial research and validation activities')
        self.assertEqual(workflows[1].name, 'Design Process')
        self.assertEqual(workflows[1].description, 'Design and prototyping activities')
        
        # Verify session was cleaned up
        session = self.client.session
        self.assertNotIn('playbook_wizard_step1', session)
        self.assertNotIn('playbook_wizard_step2', session)
        self.assertNotIn('playbook_wizard_workflows', session)
        
        # Verify success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('created successfully', str(messages[0]))

    def test_complete_wizard_flow_without_workflows(self):
        """Test complete wizard flow skipping workflows."""
        # Step 1: Basic Information
        response = self.client.post(reverse('playbook_create_step1'), {
            'name': 'Simple Test Playbook',
            'description': 'A simple playbook without workflows',
            'category': Category.DESIGN,
            'visibility': Visibility.FAMILY,
            'tags': 'simple,design',
            'action': 'next',
        })
        
        # Should redirect to Step 2
        self.assertRedirects(response, reverse('playbook_create_step2'))
        
        # Step 2: Skip Workflows
        response = self.client.post(reverse('playbook_create_step2'), {
            'action': 'skip',
        })
        
        # Should redirect to Step 3
        self.assertRedirects(response, reverse('playbook_create_step3'))
        
        # Verify Step 2 data is in session
        session = self.client.session
        step2_data = session.get('playbook_wizard_step2')
        self.assertIsNotNone(step2_data)
        self.assertTrue(step2_data['skip_workflows'])
        
        # Step 3: Publishing Settings (default to draft)
        response = self.client.post(reverse('playbook_create_step3'), {})
        
        # Should redirect to playbook detail
        self.assertRedirects(response, reverse('playbook_detail', kwargs={'playbook_id': 1}))
        
        # Verify playbook was created
        playbook = Playbook.objects.get(id=1)
        self.assertEqual(playbook.name, 'Simple Test Playbook')
        self.assertEqual(playbook.category, Category.DESIGN)
        self.assertEqual(playbook.visibility, Visibility.FAMILY)
        self.assertEqual(playbook.status, Status.DRAFT)  # Default status
        # Tags are stored as a list in the JSONField
        self.assertEqual(playbook.tags, ['simple', 'design'])
        
        # Verify no workflows were created
        workflows = Workflow.objects.filter(playbook=playbook)
        self.assertEqual(len(workflows), 0)

    def test_wizard_navigation_flow(self):
        """Test wizard navigation between steps."""
        # Start Step 1
        response = self.client.get(reverse('playbook_create_step1'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Step 1: Basic Information')
        
        # Submit Step 1
        response = self.client.post(reverse('playbook_create_step1'), {
            'name': 'Navigation Test',
            'description': 'Testing navigation',
            'category': Category.RESEARCH,
            'visibility': Visibility.LOCAL_ONLY,
            'action': 'next',
        })
        self.assertRedirects(response, reverse('playbook_create_step2'))
        
        # Check Step 2 breadcrumbs
        response = self.client.get(reverse('playbook_create_step2'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Step 1: Basic Information')
        self.assertContains(response, 'Step 2: Add Workflows')
        self.assertContains(response, 'Step 3: Publishing Settings')
        self.assertContains(response, reverse('playbook_create_step1'))
        # Step 2 is not a link since it's the current page
        
        # Skip to Step 3
        response = self.client.post(reverse('playbook_create_step2'), {
            'action': 'skip',
        })
        self.assertRedirects(response, reverse('playbook_create_step3'))
        
        # Check Step 3 breadcrumbs
        response = self.client.get(reverse('playbook_create_step3'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Step 1: Basic Information')
        self.assertContains(response, 'Step 2: Add Workflows')
        self.assertContains(response, 'Step 3: Publishing Settings')
        self.assertContains(response, reverse('playbook_create_step1'))
        self.assertContains(response, reverse('playbook_create_step2'))
        # Step 3 is not a link since it's the current page

    def test_wizard_session_persistence(self):
        """Test that wizard data persists across requests."""
        # Submit Step 1 with specific data
        response = self.client.post(reverse('playbook_create_step1'), {
            'name': 'Persistence Test',
            'description': 'Testing session persistence',
            'category': Category.DEVELOPMENT,
            'visibility': Visibility.PRIVATE,
            'tags': 'persistence,session',
            'action': 'next',
        })
        
        # Navigate to Step 2
        response = self.client.get(reverse('playbook_create_step2'))
        self.assertEqual(response.status_code, 200)
        
        # Step 2 should show Step 1 data
        self.assertContains(response, 'Persistence Test')
        self.assertContains(response, 'Testing session persistence')
        
        # Navigate back to Step 2 again (simulate refresh)
        response = self.client.get(reverse('playbook_create_step2'))
        self.assertEqual(response.status_code, 200)
        
        # Data should still be there
        self.assertContains(response, 'Persistence Test')
        
        # Skip to Step 3
        response = self.client.post(reverse('playbook_create_step2'), {
            'action': 'skip',
        })
        
        # Step 3 should show all previous data
        response = self.client.get(reverse('playbook_create_step3'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Persistence Test')
        self.assertContains(response, 'Testing session persistence')
        self.assertContains(response, 'Development')
        self.assertContains(response, 'Private')
        self.assertContains(response, 'persistence')
        self.assertContains(response, 'session')

    def test_wizard_error_handling(self):
        """Test wizard error handling and recovery."""
        # Submit Step 1 with invalid data
        response = self.client.post(reverse('playbook_create_step1'), {
            'name': '',  # Empty name
            'description': 'Too short',
            'category': Category.DEVELOPMENT,
            'visibility': Visibility.PRIVATE,
            'action': 'next',
        })
        
        # Should stay on Step 1 with errors
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name-error')
        self.assertContains(response, 'description-error')
        
        # Submit Step 1 with valid data
        response = self.client.post(reverse('playbook_create_step1'), {
            'name': 'Error Recovery Test',
            'description': 'A playbook to test error recovery',
            'category': Category.DEVELOPMENT,
            'visibility': Visibility.PRIVATE,
            'action': 'next',
        })
        
        # Should proceed to Step 2
        self.assertRedirects(response, reverse('playbook_create_step2'))
        
        # Add invalid workflow
        response = self.client.post(reverse('playbook_create_step2'), {
            'action': 'add_workflow',
            'workflow_name': 'Ab',  # Too short
            'workflow_description': 'Too short',
        })
        
        # Should stay on Step 2 with errors
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'workflow-name-error')
        self.assertContains(response, 'workflow-description-error')
        
        # Add valid workflow
        response = self.client.post(reverse('playbook_create_step2'), {
            'action': 'add_workflow',
            'workflow_name': 'Valid Workflow',
            'workflow_description': 'A valid workflow description for testing',
        })
        
        # Should stay on Step 2 (workflow added)
        self.assertEqual(response.status_code, 200)
        
        # Continue to Step 3
        response = self.client.post(reverse('playbook_create_step2'), {
            'action': 'continue',
        })
        
        # Should proceed to Step 3
        self.assertRedirects(response, reverse('playbook_create_step3'))
        
        # Complete the wizard
        response = self.client.post(reverse('playbook_create_step3'), {
            'status': Status.DRAFT,
        })
        
        # Should successfully create playbook
        self.assertRedirects(response, reverse('playbook_detail', kwargs={'playbook_id': 1}))
        
        # Verify playbook was created despite errors
        playbook = Playbook.objects.get(id=1)
        self.assertEqual(playbook.name, 'Error Recovery Test')
        
        # Verify valid workflow was created
        workflows = Workflow.objects.filter(playbook=playbook)
        self.assertEqual(len(workflows), 1)
        self.assertEqual(workflows[0].name, 'Valid Workflow')
