"""Integration tests for Playbook EDIT operation."""

import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from methodology.models import Playbook

User = get_user_model()


@pytest.fixture
def test_user():
    """Create test user."""
    return User.objects.create_user(username='maria', password='test123')


@pytest.fixture
def other_user():
    """Create another user."""
    return User.objects.create_user(username='bob', password='test123')


@pytest.fixture
def owned_playbook(test_user):
    """Create owned playbook."""
    return Playbook.objects.create(
        name='Product Discovery Framework',
        description='Comprehensive methodology for discovering and validating products',
        category='product',
        tags=['product management', 'discovery', 'validation'],
        visibility='private',
        status='active',
        author=test_user,
        source='owned'
    )


@pytest.fixture
def downloaded_playbook(test_user):
    """Create downloaded playbook."""
    return Playbook.objects.create(
        name='Downloaded Framework',
        description='Framework from library',
        category='development',
        author=test_user,
        source='downloaded'
    )


@pytest.mark.django_db
class TestPlaybookEdit:
    """Test playbook edit operation."""
    
    def test_pb_edit_01_open_edit_form(self, test_user, owned_playbook):
        """PB-EDIT-01: Open edit form from playbook detail."""
        client = Client()
        client.force_login(test_user)
        
        response = client.get(reverse('playbook_edit', kwargs={'pk': owned_playbook.pk}))
        
        assert response.status_code == 200
        assert b'Edit Playbook' in response.content or b'Edit' in response.content
    
    def test_pb_edit_02_form_prepopulated(self, test_user, owned_playbook):
        """PB-EDIT-02: Form shows pre-populated data."""
        client = Client()
        client.force_login(test_user)
        
        response = client.get(reverse('playbook_edit', kwargs={'pk': owned_playbook.pk}))
        
        assert owned_playbook.name.encode() in response.content
        assert owned_playbook.description.encode() in response.content
    
    def test_pb_edit_03_edit_name(self, test_user, owned_playbook):
        """PB-EDIT-03: Edit playbook name."""
        client = Client()
        client.force_login(test_user)
        
        response = client.post(
            reverse('playbook_edit', kwargs={'pk': owned_playbook.pk}),
            {
                'name': 'Product Discovery Framework v2',
                'description': owned_playbook.description,
                'category': owned_playbook.category,
                'tags': 'product management, discovery',
                'visibility': owned_playbook.visibility,
                'status': owned_playbook.status
            },
            follow=True
        )
        
        assert response.status_code == 200
        owned_playbook.refresh_from_db()
        assert owned_playbook.name == 'Product Discovery Framework v2'
    
    def test_pb_edit_04_edit_description(self, test_user, owned_playbook):
        """PB-EDIT-04: Edit playbook description."""
        client = Client()
        client.force_login(test_user)
        
        new_desc = 'Updated comprehensive methodology for product discovery'
        
        response = client.post(
            reverse('playbook_edit', kwargs={'pk': owned_playbook.pk}),
            {
                'name': owned_playbook.name,
                'description': new_desc,
                'category': owned_playbook.category,
                'tags': 'test',
                'visibility': owned_playbook.visibility,
                'status': owned_playbook.status
            },
            follow=True
        )
        
        owned_playbook.refresh_from_db()
        assert owned_playbook.description == new_desc
    
    def test_pb_edit_05_change_category(self, test_user, owned_playbook):
        """PB-EDIT-05: Change playbook category."""
        client = Client()
        client.force_login(test_user)
        
        response = client.post(
            reverse('playbook_edit', kwargs={'pk': owned_playbook.pk}),
            {
                'name': owned_playbook.name,
                'description': owned_playbook.description,
                'category': 'research',
                'tags': 'test',
                'visibility': owned_playbook.visibility,
                'status': owned_playbook.status
            },
            follow=True
        )
        
        owned_playbook.refresh_from_db()
        assert owned_playbook.category == 'research'
    
    def test_pb_edit_06_add_tags(self, test_user, owned_playbook):
        """PB-EDIT-06: Add new tags."""
        client = Client()
        client.force_login(test_user)
        
        response = client.post(
            reverse('playbook_edit', kwargs={'pk': owned_playbook.pk}),
            {
                'name': owned_playbook.name,
                'description': owned_playbook.description,
                'category': owned_playbook.category,
                'tags': 'product, discovery, validation, lean startup, user research',
                'visibility': owned_playbook.visibility,
                'status': owned_playbook.status
            },
            follow=True
        )
        
        owned_playbook.refresh_from_db()
        assert len(owned_playbook.tags) == 5
        assert 'lean startup' in owned_playbook.tags
    
    def test_pb_edit_10_change_status_to_draft(self, test_user, owned_playbook):
        """PB-EDIT-10: Change status from Active to Draft."""
        client = Client()
        client.force_login(test_user)
        
        response = client.post(
            reverse('playbook_edit', kwargs={'pk': owned_playbook.pk}),
            {
                'name': owned_playbook.name,
                'description': owned_playbook.description,
                'category': owned_playbook.category,
                'tags': 'test',
                'visibility': owned_playbook.visibility,
                'status': 'draft'
            },
            follow=True
        )
        
        owned_playbook.refresh_from_db()
        assert owned_playbook.status == 'draft'
    
    def test_pb_edit_12_version_readonly(self, test_user, owned_playbook):
        """PB-EDIT-12: Version field is read-only."""
        client = Client()
        client.force_login(test_user)
        
        original_version = owned_playbook.version
        
        # Try to change version (should be ignored)
        response = client.post(
            reverse('playbook_edit', kwargs={'pk': owned_playbook.pk}),
            {
                'name': owned_playbook.name,
                'description': owned_playbook.description,
                'category': owned_playbook.category,
                'tags': 'test',
                'visibility': owned_playbook.visibility,
                'status': owned_playbook.status,
                'version': 999  # Should be ignored
            },
            follow=True
        )
        
        owned_playbook.refresh_from_db()
        assert owned_playbook.version == original_version
    
    def test_pb_edit_13_validate_required_name(self, test_user, owned_playbook):
        """PB-EDIT-13: Validate required name field."""
        client = Client()
        client.force_login(test_user)
        
        response = client.post(
            reverse('playbook_edit', kwargs={'pk': owned_playbook.pk}),
            {
                'name': '',
                'description': owned_playbook.description,
                'category': owned_playbook.category,
                'tags': 'test',
                'visibility': owned_playbook.visibility,
                'status': owned_playbook.status
            }
        )
        
        assert response.status_code == 200
        assert b'required' in response.content.lower() or b'error' in response.content.lower()
    
    def test_pb_edit_14_duplicate_name_validation(self, test_user, owned_playbook):
        """PB-EDIT-14: Duplicate name validation."""
        # Create another playbook
        Playbook.objects.create(
            name='Existing Framework',
            description='Test',
            category='product',
            author=test_user,
            source='owned'
        )
        
        client = Client()
        client.force_login(test_user)
        
        response = client.post(
            reverse('playbook_edit', kwargs={'pk': owned_playbook.pk}),
            {
                'name': 'Existing Framework',
                'description': owned_playbook.description,
                'category': owned_playbook.category,
                'tags': 'test',
                'visibility': owned_playbook.visibility,
                'status': owned_playbook.status
            }
        )
        
        assert response.status_code == 200
        assert b'already exists' in response.content.lower()
    
    def test_pb_edit_23_cannot_edit_downloaded(self, test_user, downloaded_playbook):
        """PB-EDIT-23: Cannot edit downloaded playbooks."""
        client = Client()
        client.force_login(test_user)
        
        response = client.get(reverse('playbook_edit', kwargs={'pk': downloaded_playbook.pk}))
        
        # Should redirect or show error
        assert response.status_code in [302, 403, 200]
        if response.status_code == 200:
            assert b'cannot edit' in response.content.lower() or b'own' in response.content.lower()
