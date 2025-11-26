"""Feature Acceptance Tests for Quick Create Playbook (Step 1).

Tests all scenarios from docs/features/act-2-playbooks/playbooks-create.feature
related to Step 1 of the wizard.

Uses Django Test Client for fast, reliable testing.
NO mocking - real database operations.
"""
import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from methodology.models import Playbook, Visibility, Status, Category


@pytest.mark.django_db
class TestQuickCreatePlaybookStep1:
    """Test PB-CREATE-01 through PB-CREATE-08: Step 1 of playbook creation wizard."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test user and client."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
    
    def test_open_create_wizard_step1_get(self):
        """Test PB-CREATE-01: Open create playbook wizard Step 1."""
        response = self.client.get(reverse('playbook_create_step1'))
        
        # Check response
        assert response.status_code == 200
        assert 'playbooks/wizard/step1_basic.html' in [t.name for t in response.templates]
        
        # Check content
        content = response.content.decode('utf-8')
        assert 'data-testid="playbook-create-step1-form"' in content
        assert 'Step 1: Basic Information' in content
        assert 'data-testid="name-input"' in content
        assert 'data-testid="description-input"' in content
        assert 'data-testid="category-select"' in content
        assert 'data-testid="visibility-private"' in content
        assert 'data-testid="next-button"' in content
        assert 'data-testid="cancel-button"' in content
    
    def test_step1_validation_empty_name(self):
        """Test PB-CREATE-03: Name field required validation."""
        response = self.client.post(reverse('playbook_create_step1'), {
            'name': '',
            'description': 'Valid description with at least 10 characters.',
            'category': Category.DEVELOPMENT,
            'visibility': Visibility.PRIVATE,
        })
        
        # Should stay on Step 1 with errors
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'data-testid="name-error"' in content
        assert 'Name is required' in content or '3-100 characters' in content
    
    def test_step1_validation_name_too_short(self):
        """Test PB-CREATE-05: Name minimum length validation."""
        response = self.client.post(reverse('playbook_create_step1'), {
            'name': 'AB',  # Too short
            'description': 'Valid description with at least 10 characters.',
            'category': Category.DEVELOPMENT,
            'visibility': Visibility.PRIVATE,
        })
        
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'data-testid="name-error"' in content
        assert 'at least 3 characters' in content
    
    def test_step1_validation_name_too_long(self):
        """Test PB-CREATE-05: Name maximum length validation."""
        response = self.client.post(reverse('playbook_create_step1'), {
            'name': 'A' * 101,  # Too long
            'description': 'Valid description with at least 10 characters.',
            'category': Category.DEVELOPMENT,
            'visibility': Visibility.PRIVATE,
        })
        
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'data-testid="name-error"' in content
        assert 'not exceed 100 characters' in content
    
    def test_step1_validation_empty_description(self):
        """Test PB-CREATE-03: Description field required validation."""
        response = self.client.post(reverse('playbook_create_step1'), {
            'name': 'Valid Playbook Name',
            'description': '',
            'category': Category.DEVELOPMENT,
            'visibility': Visibility.PRIVATE,
        })
        
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'data-testid="description-error"' in content
        assert 'Description is required' in content or '10-500 characters' in content
    
    def test_step1_validation_description_too_short(self):
        """Test PB-CREATE-06: Description minimum length validation."""
        response = self.client.post(reverse('playbook_create_step1'), {
            'name': 'Valid Playbook Name',
            'description': 'Too short',  # 9 characters
            'category': Category.DEVELOPMENT,
            'visibility': Visibility.PRIVATE,
        })
        
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'data-testid="description-error"' in content
        assert 'at least 10 characters' in content
    
    def test_step1_validation_description_too_long(self):
        """Test PB-CREATE-06: Description maximum length validation."""
        response = self.client.post(reverse('playbook_create_step1'), {
            'name': 'Valid Playbook Name',
            'description': 'A' * 501,  # Too long
            'category': Category.DEVELOPMENT,
            'visibility': Visibility.PRIVATE,
        })
        
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'data-testid="description-error"' in content
        assert 'not exceed 500 characters' in content
    
    def test_step1_validation_empty_category(self):
        """Test PB-CREATE-03: Category field required validation."""
        response = self.client.post(reverse('playbook_create_step1'), {
            'name': 'Valid Playbook Name',
            'description': 'Valid description with at least 10 characters.',
            'category': '',
            'visibility': Visibility.PRIVATE,
        })
        
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'data-testid="category-error"' in content
        assert 'Please select a category' in content
    
    def test_step1_validation_duplicate_name(self):
        """Test PB-CREATE-04: Duplicate playbook name validation."""
        # Create existing playbook
        Playbook.objects.create(
            name='Existing Playbook',
            description='Existing description with enough characters.',
            category=Category.DEVELOPMENT,
            visibility=Visibility.PRIVATE,
            created_by=self.user
        )
        
        response = self.client.post(reverse('playbook_create_step1'), {
            'name': 'Existing Playbook',  # Duplicate name
            'description': 'Valid description with at least 10 characters.',
            'category': Category.DESIGN,
            'visibility': Visibility.PRIVATE,
        })
        
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'data-testid="name-error"' in content
        assert 'already exists' in content
    
    def test_step1_success_redirects_to_step2(self):
        """Test PB-CREATE-02: Valid Step 1 data redirects to Step 2."""
        response = self.client.post(reverse('playbook_create_step1'), {
            'name': 'Product Discovery Framework',
            'description': 'Comprehensive methodology for discovering and validating product opportunities.',
            'category': Category.PRODUCT,
            'visibility': Visibility.PRIVATE,
            'tags': ['product management', 'discovery'],
        })
        
        # Should redirect to Step 2
        assert response.status_code == 302
        assert reverse('playbook_create_step2') in response.url
        
        # Check session data is stored
        session_data = self.client.session.get('playbook_wizard_step1', {})
        assert session_data['name'] == 'Product Discovery Framework'
        assert session_data['category'] == Category.PRODUCT
    
    def test_step1_with_tags_validation(self):
        """Test PB-CREATE-08: Tags field validation and handling."""
        response = self.client.post(reverse('playbook_create_step1'), {
            'name': 'Test Playbook',
            'description': 'Valid description with at least 10 characters.',
            'category': Category.PRODUCT,
            'visibility': Visibility.PRIVATE,
            'tags': 'product management,discovery,validation',
        })
        
        # Should succeed with valid tags
        assert response.status_code == 302
        assert reverse('playbook_create_step2') in response.url
        
        # Check tags are stored correctly
        session_data = self.client.session.get('playbook_wizard_step1', {})
        assert 'product management' in session_data['tags']
        assert 'discovery' in session_data['tags']
        assert 'validation' in session_data['tags']
    
    def test_step1_visibility_options(self):
        """Test PB-CREATE-07: All visibility options are available."""
        response = self.client.get(reverse('playbook_create_step1'))
        content = response.content.decode('utf-8')
        
        # Check all visibility options are present
        assert 'data-testid="visibility-private"' in content
        assert 'data-testid="visibility-family"' in content
        assert 'data-testid="visibility-local_only"' in content
        
        # Check labels are correct
        assert 'Private (only me)' in content
        assert 'Family' in content
        assert 'Local only (not uploaded to Homebase)' in content
    
    def test_step1_cancel_confirmation_modal(self):
        """Test PB-CREATE-15: Cancel button shows confirmation modal."""
        response = self.client.get(reverse('playbook_create_step1'))
        content = response.content.decode('utf-8')
        
        # Check cancel button and modal
        assert 'data-testid="cancel-button"' in content
        assert 'data-bs-target="#cancelModal"' in content
        assert 'Discard changes?' in content
        assert 'data-testid="keep-editing-button"' in content
        assert 'data-testid="discard-changes-button"' in content
    
    def test_step1_form_has_test_ids(self):
        """Test all form elements have proper test IDs for E2E testing."""
        response = self.client.get(reverse('playbook_create_step1'))
        content = response.content.decode('utf-8')
        
        # Check all important elements have test IDs
        test_ids = [
            'data-testid="playbook-create-step1-form"',
            'data-testid="name-input"',
            'data-testid="description-input"',
            'data-testid="category-select"',
            'data-testid="tags-input"',
            'data-testid="visibility-private"',
            'data-testid="next-button"',
            'data-testid="cancel-button"',
        ]
        
        for test_id in test_ids:
            assert test_id in content, f"Missing test ID: {test_id}"
