"""Integration tests for Step 2 of the playbook creation wizard."""

import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from methodology.models import Playbook, Category, Visibility, Workflow


class TestQuickCreatePlaybookStep2(TestCase):
    """Integration tests for Step 2: Add Workflows."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
        self.client.login(username='testuser', password='testpass')
        
        # Set up Step 1 session data
        session = self.client.session
        session['playbook_wizard_step1'] = {
            'name': 'Test Playbook',
            'description': 'A test playbook for workflows',
            'category': Category.DEVELOPMENT,
            'visibility': Visibility.PRIVATE,
        }
        session.save()

    def test_step2_get_displays_correctly(self):
        """Test PB-CREATE-08: Step 2 displays correctly after Step 1."""
        response = self.client.get(reverse('playbook_create_step2'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Step 2: Add Workflows')
        self.assertContains(response, 'Test Playbook')
        self.assertContains(response, 'A test playbook for workflows')
        self.assertContains(response, 'data-testid="add-workflow-form"')
        self.assertContains(response, 'data-testid="skip-button"')

    def test_step2_requires_step1_data(self):
        """Test that Step 2 requires Step 1 data."""
        # Clear session
        session = self.client.session
        session.pop('playbook_wizard_step1', None)
        session.save()
        
        response = self.client.get(reverse('playbook_create_step2'))
        
        self.assertRedirects(response, reverse('playbook_create_step1'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Please complete Step 1 first', str(messages[0]))

    def test_step2_add_workflow_success(self):
        """Test PB-CREATE-10: Add first workflow successfully."""
        response = self.client.post(reverse('playbook_create_step2'), {
            'action': 'add_workflow',
            'workflow_name': 'Discovery Phase',
            'workflow_description': 'Initial research and validation activities.',
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Discovery Phase')
        self.assertContains(response, 'Initial research and validation activities.')
        self.assertContains(response, 'data-testid="workflow-temp_1"')
        
        # Check session has workflow
        session = self.client.session
        workflows = session.get('playbook_wizard_workflows', [])
        self.assertEqual(len(workflows), 1)
        self.assertEqual(workflows[0]['name'], 'Discovery Phase')
        self.assertEqual(workflows[0]['description'], 'Initial research and validation activities.')

    def test_step2_add_workflow_validation_errors(self):
        """Test workflow validation errors."""
        # Test empty name
        response = self.client.post(reverse('playbook_create_step2'), {
            'action': 'add_workflow',
            'workflow_name': '',
            'workflow_description': 'Valid description with enough characters.',
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-testid="workflow-name-error"')
        self.assertContains(response, 'Workflow name is required.')

    def test_step2_add_workflow_name_too_short(self):
        """Test workflow name minimum length validation."""
        response = self.client.post(reverse('playbook_create_step2'), {
            'action': 'add_workflow',
            'workflow_name': 'AB',  # Too short
            'workflow_description': 'Valid description with enough characters.',
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-testid="workflow-name-error"')
        self.assertContains(response, 'at least 3 characters')

    def test_step2_add_workflow_description_too_short(self):
        """Test workflow description minimum length validation."""
        response = self.client.post(reverse('playbook_create_step2'), {
            'action': 'add_workflow',
            'workflow_name': 'Valid Workflow Name',
            'workflow_description': 'Too short',  # Too short
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-testid="workflow-description-error"')
        self.assertContains(response, 'at least 10 characters')

    def test_step2_add_duplicate_workflow_name(self):
        """Test duplicate workflow name validation."""
        # Add first workflow
        self.client.post(reverse('playbook_create_step2'), {
            'action': 'add_workflow',
            'workflow_name': 'Discovery Phase',
            'workflow_description': 'First workflow description.',
        })
        
        # Try to add duplicate
        response = self.client.post(reverse('playbook_create_step2'), {
            'action': 'add_workflow',
            'workflow_name': 'Discovery Phase',  # Duplicate
            'workflow_description': 'Second workflow description.',
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-testid="workflow-name-error"')
        self.assertContains(response, 'already exists')

    def test_step2_remove_workflow(self):
        """Test removing a workflow."""
        # Add a workflow first
        self.client.post(reverse('playbook_create_step2'), {
            'action': 'add_workflow',
            'workflow_name': 'Test Workflow',
            'workflow_description': 'Test description.',
        })
        
        # Remove it
        response = self.client.post(reverse('playbook_create_step2'), {
            'action': 'remove_workflow',
            'workflow_id': 'temp_1',
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Workflow')
        
        # Check session is empty
        session = self.client.session
        workflows = session.get('playbook_wizard_workflows', [])
        self.assertEqual(len(workflows), 0)

    def test_step2_skip_workflows(self):
        """Test PB-CREATE-09: Skip adding workflows."""
        response = self.client.post(reverse('playbook_create_step2'), {
            'action': 'skip',
        })
        
        self.assertRedirects(response, reverse('playbook_create_step3'))
        
        # Check session data
        session = self.client.session
        step2_data = session.get('playbook_wizard_step2')
        self.assertTrue(step2_data['skip_workflows'])
        self.assertEqual(step2_data['workflows'], [])

    def test_step2_continue_with_workflows(self):
        """Test continuing to Step 3 with workflows."""
        # Add a workflow first
        self.client.post(reverse('playbook_create_step2'), {
            'action': 'add_workflow',
            'workflow_name': 'Test Workflow',
            'workflow_description': 'Test description.',
        })
        
        # Continue to Step 3
        response = self.client.post(reverse('playbook_create_step2'), {
            'action': 'continue',
        })
        
        self.assertRedirects(response, reverse('playbook_create_step3'))
        
        # Check session data
        session = self.client.session
        step2_data = session.get('playbook_wizard_step2')
        self.assertFalse(step2_data['skip_workflows'])
        self.assertEqual(len(step2_data['workflows']), 1)
        self.assertEqual(step2_data['workflows'][0]['name'], 'Test Workflow')

    def test_step2_continue_button_only_shows_with_workflows(self):
        """Test that Continue button only appears when workflows exist."""
        # Initially no continue button
        response = self.client.get(reverse('playbook_create_step2'))
        self.assertNotContains(response, 'data-testid="continue-button"')
        
        # Add workflow and check continue button appears
        self.client.post(reverse('playbook_create_step2'), {
            'action': 'add_workflow',
            'workflow_name': 'Test Workflow',
            'workflow_description': 'Test description.',
        })
        
        response = self.client.get(reverse('playbook_create_step2'))
        self.assertContains(response, 'data-testid="continue-button"')

    def test_step2_workflow_list_display(self):
        """Test that multiple workflows display correctly."""
        # Add multiple workflows
        workflows_data = [
            ('Discovery Phase', 'Research and validation'),
            ('Design Process', 'Wireframing and prototyping'),
            ('Development Sprint', 'Coding and testing'),
        ]
        
        for name, desc in workflows_data:
            self.client.post(reverse('playbook_create_step2'), {
                'action': 'add_workflow',
                'workflow_name': name,
                'workflow_description': desc,
            })
        
        response = self.client.get(reverse('playbook_create_step2'))
        
        # Check all workflows are displayed
        self.assertContains(response, 'Added Workflows (3)')
        for name, desc in workflows_data:
            self.assertContains(response, name)
            self.assertContains(response, desc)
        
        # Check workflow count
        session = self.client.session
        workflows = session.get('playbook_wizard_workflows', [])
        self.assertEqual(len(workflows), 3)

    def test_step2_form_has_test_ids(self):
        """Test that all form elements have test IDs."""
        response = self.client.get(reverse('playbook_create_step2'))
        
        # Check main elements have test IDs
        test_ids = [
            'add-workflow-form',
            'workflow-name-input',
            'workflow-description-input',
            'add-workflow-button',
            'skip-button',
            'workflow-name-field-group',
            'workflow-description-field-group',
        ]
        
        for test_id in test_ids:
            self.assertContains(response, f'data-testid="{test_id}"')

    def test_step2_breadcrumb_navigation(self):
        """Test breadcrumb navigation links."""
        response = self.client.get(reverse('playbook_create_step2'))
        
        self.assertContains(response, reverse('playbook_create_step1'))
        self.assertContains(response, 'data-testid="step1-link"')
        self.assertContains(response, 'Step 1: Basic Information')
        self.assertContains(response, 'Step 2: Add Workflows')
        self.assertContains(response, 'Step 3: Publishing Settings')

    def test_step2_workflow_examples_display(self):
        """Test that workflow examples are displayed in sidebar."""
        response = self.client.get(reverse('playbook_create_step2'))
        
        examples = [
            'Discovery Phase',
            'Design Process', 
            'Development Sprint',
        ]
        
        for example in examples:
            self.assertContains(response, example)

    def test_step2_skip_confirmation_modal(self):
        """Test skip confirmation modal elements."""
        response = self.client.get(reverse('playbook_create_step2'))
        
        self.assertContains(response, 'skipModal')
        self.assertContains(response, 'data-testid="confirm-skip-button"')
        self.assertContains(response, 'Skip adding workflows?')
        self.assertContains(response, 'You can add workflows later')
