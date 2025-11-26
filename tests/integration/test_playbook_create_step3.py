"""Integration tests for Step 3 of the playbook creation wizard."""

import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from methodology.models import Playbook, Category, Visibility, Status, Workflow


class TestQuickCreatePlaybookStep3(TestCase):
    """Integration tests for Step 3: Publishing Settings."""

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
            'description': 'A test playbook for Step 3',
            'category': Category.DEVELOPMENT,
            'visibility': Visibility.PRIVATE,
            'tags': ['testing', 'playbook'],
        }
        session.save()

    def test_step3_get_displays_correctly(self):
        """Test PB-CREATE-12: Step 3 displays correctly after Step 2."""
        # Set up Step 2 data
        session = self.client.session
        session['playbook_wizard_step2'] = {
            'skip_workflows': True,
            'workflows': [],
        }
        session.save()
        
        response = self.client.get(reverse('playbook_create_step3'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Step 3: Publishing Settings')
        self.assertContains(response, 'Test Playbook')
        self.assertContains(response, 'A test playbook for Step 3')
        self.assertContains(response, 'data-testid="publishing-form"')
        self.assertContains(response, 'data-testid="summary-name"')

    def test_step3_requires_step1_data(self):
        """Test that Step 3 requires Step 1 data."""
        # Clear session
        session = self.client.session
        session.pop('playbook_wizard_step1', None)
        session.save()
        
        response = self.client.get(reverse('playbook_create_step3'))
        
        self.assertRedirects(response, reverse('playbook_create_step1'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Please complete Step 1 first', str(messages[0]))

    def test_step3_displays_summary_without_workflows(self):
        """Test PB-CREATE-13: Summary displays correctly when workflows skipped."""
        # Set up Step 2 data with skipped workflows
        session = self.client.session
        session['playbook_wizard_step2'] = {
            'skip_workflows': True,
            'workflows': [],
        }
        session.save()
        
        response = self.client.get(reverse('playbook_create_step3'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-testid="summary-workflows"')
        self.assertContains(response, 'None added yet')
        self.assertNotContains(response, 'workflows added')

    def test_step3_displays_summary_with_workflows(self):
        """Test PB-CREATE-14: Summary displays correctly with workflows."""
        # Set up Step 2 data with workflows
        session = self.client.session
        session['playbook_wizard_step2'] = {
            'skip_workflows': False,
            'workflows': [
                {'id': 'temp_1', 'name': 'Discovery Phase', 'description': 'Research phase'},
                {'id': 'temp_2', 'name': 'Design Process', 'description': 'Design phase'},
            ],
        }
        session.save()
        
        response = self.client.get(reverse('playbook_create_step3'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-testid="summary-workflows"')
        self.assertContains(response, '2 workflows added')
        self.assertNotContains(response, 'None added yet')

    def test_step3_displays_summary_with_single_workflow(self):
        """Test PB-CREATE-15: Summary displays correctly with single workflow."""
        # Set up Step 2 data with single workflow
        session = self.client.session
        session['playbook_wizard_step2'] = {
            'skip_workflows': False,
            'workflows': [
                {'id': 'temp_1', 'name': 'Discovery Phase', 'description': 'Research phase'},
            ],
        }
        session.save()
        
        response = self.client.get(reverse('playbook_create_step3'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-testid="summary-workflows"')
        self.assertContains(response, '1 workflow added')
        self.assertNotContains(response, 'None added yet')

    def test_step3_create_playbook_draft_success(self):
        """Test PB-CREATE-16: Create playbook with draft status."""
        # Set up Step 2 data
        session = self.client.session
        session['playbook_wizard_step2'] = {
            'skip_workflows': True,
            'workflows': [],
        }
        session.save()
        
        response = self.client.post(reverse('playbook_create_step3'), {
            'status': Status.DRAFT,
        })
        
        self.assertRedirects(response, reverse('playbook_detail', kwargs={'playbook_id': 1}))
        
        # Check playbook was created
        playbook = Playbook.objects.get(id=1)
        self.assertEqual(playbook.name, 'Test Playbook')
        self.assertEqual(playbook.description, 'A test playbook for Step 3')
        self.assertEqual(playbook.category, Category.DEVELOPMENT)
        self.assertEqual(playbook.visibility, Visibility.PRIVATE)
        self.assertEqual(playbook.status, Status.DRAFT)
        self.assertEqual(playbook.created_by, self.user)
        
        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('created successfully', str(messages[0]))

    def test_step3_create_playbook_published_success(self):
        """Test PB-CREATE-17: Create playbook with active status."""
        # Set up Step 2 data
        session = self.client.session
        session['playbook_wizard_step2'] = {
            'skip_workflows': True,
            'workflows': [],
        }
        session.save()
        
        response = self.client.post(reverse('playbook_create_step3'), {
            'status': Status.ACTIVE,
        })
        
        self.assertRedirects(response, reverse('playbook_detail', kwargs={'playbook_id': 1}))
        
        # Check playbook was created with active status
        playbook = Playbook.objects.get(id=1)
        self.assertEqual(playbook.status, Status.ACTIVE)

    def test_step3_create_playbook_with_workflows(self):
        """Test PB-CREATE-18: Create playbook with workflows."""
        # Set up Step 2 data with workflows
        session = self.client.session
        session['playbook_wizard_step2'] = {
            'skip_workflows': False,
            'workflows': [
                {'id': 'temp_1', 'name': 'Discovery Phase', 'description': 'Research and validation'},
                {'id': 'temp_2', 'name': 'Design Process', 'description': 'Design and prototyping'},
            ],
        }
        session.save()
        
        response = self.client.post(reverse('playbook_create_step3'), {
            'status': Status.DRAFT,
        })
        
        self.assertRedirects(response, reverse('playbook_detail', kwargs={'playbook_id': 1}))
        
        # Check playbook was created
        playbook = Playbook.objects.get(id=1)
        self.assertEqual(playbook.name, 'Test Playbook')
        
        # Check workflows were created
        workflows = Workflow.objects.filter(playbook=playbook).order_by('order')
        self.assertEqual(len(workflows), 2)
        self.assertEqual(workflows[0].name, 'Discovery Phase')
        self.assertEqual(workflows[0].description, 'Research and validation')
        self.assertEqual(workflows[0].order, 1)
        self.assertEqual(workflows[1].name, 'Design Process')
        self.assertEqual(workflows[1].description, 'Design and prototyping')
        self.assertEqual(workflows[1].order, 2)

    def test_step3_session_cleanup_after_creation(self):
        """Test PB-CREATE-19: Session data cleaned up after creation."""
        # Set up Step 2 data
        session = self.client.session
        session['playbook_wizard_step2'] = {
            'skip_workflows': True,
            'workflows': [],
        }
        session.save()
        
        # Verify session data exists before
        self.assertIn('playbook_wizard_step1', session)
        self.assertIn('playbook_wizard_step2', session)
        
        response = self.client.post(reverse('playbook_create_step3'), {
            'status': Status.DRAFT,
        })
        
        # Check session data was cleaned up
        session = self.client.session
        self.assertNotIn('playbook_wizard_step1', session)
        self.assertNotIn('playbook_wizard_step2', session)

    def test_step3_default_status_to_draft(self):
        """Test PB-CREATE-20: Default status is draft when not specified."""
        # Set up Step 2 data
        session = self.client.session
        session['playbook_wizard_step2'] = {
            'skip_workflows': True,
            'workflows': [],
        }
        session.save()
        
        response = self.client.post(reverse('playbook_create_step3'), {})
        
        self.assertRedirects(response, reverse('playbook_detail', kwargs={'playbook_id': 1}))
        
        # Check playbook was created with draft status
        playbook = Playbook.objects.get(id=1)
        self.assertEqual(playbook.status, Status.DRAFT)

    def test_step3_breadcrumb_navigation(self):
        """Test breadcrumb navigation links."""
        # Set up Step 2 data
        session = self.client.session
        session['playbook_wizard_step2'] = {
            'skip_workflows': True,
            'workflows': [],
        }
        session.save()
        
        response = self.client.get(reverse('playbook_create_step3'))
        
        self.assertContains(response, reverse('playbook_create_step1'))
        self.assertContains(response, reverse('playbook_create_step2'))
        self.assertContains(response, 'data-testid="step1-link"')
        self.assertContains(response, 'data-testid="step2-link"')
        self.assertContains(response, 'Step 1: Basic Information')
        self.assertContains(response, 'Step 2: Add Workflows')
        self.assertContains(response, 'Step 3: Publishing Settings')

    def test_step3_form_has_test_ids(self):
        """Test that all form elements have test IDs."""
        # Set up Step 2 data
        session = self.client.session
        session['playbook_wizard_step2'] = {
            'skip_workflows': True,
            'workflows': [],
        }
        session.save()
        
        response = self.client.get(reverse('playbook_create_step3'))
        
        # Check main elements have test IDs
        test_ids = [
            'publishing-form',
            'summary-name',
            'summary-description',
            'summary-category',
            'summary-tags',
            'summary-visibility',
            'summary-workflows',
        ]
        
        for test_id in test_ids:
            self.assertContains(response, f'data-testid="{test_id}"')

    def test_step3_status_choices_display(self):
        """Test that status choices are displayed correctly."""
        # Set up Step 2 data
        session = self.client.session
        session['playbook_wizard_step2'] = {
            'skip_workflows': True,
            'workflows': [],
        }
        session.save()
        
        response = self.client.get(reverse('playbook_create_step3'))
        
        # Check status choices are displayed
        for choice in Status.choices:
            self.assertContains(response, f'value="{choice[0]}"')
            self.assertContains(response, choice[1])

    def test_step3_tags_display_in_summary(self):
        """Test that tags are displayed correctly in summary."""
        # Set up Step 1 data with tags
        session = self.client.session
        session['playbook_wizard_step1'] = {
            'name': 'Test Playbook',
            'description': 'A test playbook for Step 3',
            'category': Category.DEVELOPMENT,
            'visibility': Visibility.PRIVATE,
            'tags': ['testing', 'playbook', 'development'],
        }
        session['playbook_wizard_step2'] = {
            'skip_workflows': True,
            'workflows': [],
        }
        session.save()
        
        response = self.client.get(reverse('playbook_create_step3'))
        
        self.assertContains(response, 'data-testid="summary-tags"')
        self.assertContains(response, 'testing')
        self.assertContains(response, 'playbook')
        self.assertContains(response, 'development')
        self.assertContains(response, 'badge bg-secondary')

    def test_step3_no_tags_display_in_summary(self):
        """Test summary when no tags are provided."""
        # Set up Step 1 data without tags
        session = self.client.session
        session['playbook_wizard_step1'] = {
            'name': 'Test Playbook',
            'description': 'A test playbook for Step 3',
            'category': Category.DEVELOPMENT,
            'visibility': Visibility.PRIVATE,
            'tags': [],
        }
        session['playbook_wizard_step2'] = {
            'skip_workflows': True,
            'workflows': [],
        }
        session.save()
        
        response = self.client.get(reverse('playbook_create_step3'))
        
        self.assertContains(response, 'data-testid="summary-tags"')
        self.assertContains(response, 'None')
        self.assertNotContains(response, 'badge bg-secondary')

    def test_step3_description_truncation(self):
        """Test that long descriptions are truncated in summary."""
        # Set up Step 1 data with long description
        long_description = 'A' * 150  # 150 characters
        session = self.client.session
        session['playbook_wizard_step1'] = {
            'name': 'Test Playbook',
            'description': long_description,
            'category': Category.DEVELOPMENT,
            'visibility': Visibility.PRIVATE,
            'tags': [],
        }
        session['playbook_wizard_step2'] = {
            'skip_workflows': True,
            'workflows': [],
        }
        session.save()
        
        response = self.client.get(reverse('playbook_create_step3'))
        
        self.assertContains(response, 'data-testid="summary-description"')
        self.assertContains(response, '...')  # Should show truncation
        self.assertNotContains(response, long_description)  # Should not show full description

    def test_step3_workflow_creation_error_handling(self):
        """Test that workflow creation errors don't break playbook creation."""
        # Set up Step 2 data with invalid workflow (missing required fields)
        session = self.client.session
        session['playbook_wizard_step2'] = {
            'skip_workflows': False,
            'workflows': [
                {'id': 'temp_1', 'name': '', 'description': ''},  # Invalid workflow
                {'id': 'temp_2', 'name': 'Valid Workflow', 'description': 'Valid description'},
            ],
        }
        session.save()
        
        response = self.client.post(reverse('playbook_create_step3'), {
            'status': Status.DRAFT,
        })
        
        # Playbook should still be created successfully
        self.assertRedirects(response, reverse('playbook_detail', kwargs={'playbook_id': 1}))
        
        # Check playbook was created
        playbook = Playbook.objects.get(id=1)
        self.assertEqual(playbook.name, 'Test Playbook')
        
        # Only valid workflow should be created
        workflows = Workflow.objects.filter(playbook=playbook)
        self.assertEqual(len(workflows), 1)
        self.assertEqual(workflows[0].name, 'Valid Workflow')
