"""
Unit tests for PlaybookService.

Tests all CRUD operations, validation, duplication, and status management.
NO MOCKING - uses real database via pytest-django.
"""
import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from methodology.models import Playbook
from methodology.services.playbook_service import PlaybookService

User = get_user_model()


@pytest.fixture
def maria(db):
    """Create test user maria."""
    return User.objects.create_user(username='maria', email='maria@test.com')


@pytest.fixture
def draft_playbook(db, maria):
    """Create a draft playbook."""
    return Playbook.objects.create(
        name='Test Playbook',
        description='Test Description',
        category='development',
        status='draft',
        version=Decimal('0.1'),
        author=maria
    )


@pytest.fixture
def released_playbook(db, maria):
    """Create a released playbook."""
    return Playbook.objects.create(
        name='Released Playbook',
        description='Released Description',
        category='development',
        status='released',
        version=Decimal('1.0'),
        author=maria
    )


@pytest.mark.django_db
class TestPlaybookServiceCreate:
    """Tests for PlaybookService.create_playbook."""
    
    def test_create_playbook_success(self, maria):
        """Test creating a playbook with valid data."""
        playbook = PlaybookService.create_playbook(
            author=maria,
            name='React Development',
            description='Modern React patterns',
            category='frontend'
        )
        
        assert playbook.id is not None
        assert playbook.name == 'React Development'
        assert playbook.description == 'Modern React patterns'
        assert playbook.category == 'frontend'
        assert playbook.status == 'draft'
        assert playbook.version == Decimal('0.1')
        assert playbook.author == maria
    
    def test_create_playbook_duplicate_name_raises_error(self, maria, draft_playbook):
        """Test creating playbook with duplicate name raises ValidationError."""
        with pytest.raises(ValidationError):
            PlaybookService.create_playbook(
                author=maria,
                name='Test Playbook',  # Same as draft_playbook
                description='Different',
                category='development'
            )
    
    def test_create_playbook_empty_name_raises_error(self, maria):
        """Test creating playbook with empty name raises ValidationError."""
        with pytest.raises(ValidationError):
            PlaybookService.create_playbook(
                author=maria,
                name='',
                description='Test',
                category='development'
            )


@pytest.mark.django_db
class TestPlaybookServiceGet:
    """Tests for PlaybookService.get_playbook."""
    
    def test_get_playbook_success(self, draft_playbook):
        """Test retrieving an existing playbook."""
        playbook = PlaybookService.get_playbook(draft_playbook.id)
        
        assert playbook.id == draft_playbook.id
        assert playbook.name == draft_playbook.name
    
    def test_get_playbook_not_found_raises_error(self):
        """Test retrieving non-existent playbook raises error."""
        with pytest.raises(Playbook.DoesNotExist):
            PlaybookService.get_playbook(99999)


@pytest.mark.django_db
class TestPlaybookServiceList:
    """Tests for PlaybookService.list_playbooks."""
    
    def test_list_all_playbooks(self, maria, draft_playbook, released_playbook):
        """Test listing all playbooks."""
        playbooks = PlaybookService.list_playbooks()
        
        assert len(playbooks) >= 2
        assert draft_playbook in playbooks
        assert released_playbook in playbooks
    
    def test_list_draft_playbooks_only(self, maria, draft_playbook, released_playbook):
        """Test listing only draft playbooks."""
        playbooks = PlaybookService.list_playbooks(status='draft')
        
        assert draft_playbook in playbooks
        assert released_playbook not in playbooks
    
    def test_list_released_playbooks_only(self, maria, draft_playbook, released_playbook):
        """Test listing only released playbooks."""
        playbooks = PlaybookService.list_playbooks(status='released')
        
        assert released_playbook in playbooks
        assert draft_playbook not in playbooks


@pytest.mark.django_db
class TestPlaybookServiceUpdate:
    """Tests for PlaybookService.update_playbook."""
    
    def test_update_draft_playbook_success(self, draft_playbook):
        """Test updating a draft playbook."""
        PlaybookService.update_playbook(
            draft_playbook,
            name='Updated Name',
            description='Updated Description'
        )
        
        draft_playbook.refresh_from_db()
        assert draft_playbook.name == 'Updated Name'
        assert draft_playbook.description == 'Updated Description'
        assert draft_playbook.version == Decimal('0.2')  # Auto-incremented
    
    def test_update_released_playbook_raises_permission_error(self, released_playbook):
        """Test updating a released playbook raises PermissionError."""
        with pytest.raises(PermissionError):
            PlaybookService.update_playbook(
                released_playbook,
                name='Should Fail'
            )
    
    def test_update_version_auto_increments(self, draft_playbook):
        """Test that version auto-increments on update."""
        old_version = draft_playbook.version
        
        PlaybookService.update_playbook(draft_playbook, description='Changed')
        
        draft_playbook.refresh_from_db()
        assert draft_playbook.version == old_version + Decimal('0.1')


@pytest.mark.django_db
class TestPlaybookServiceDelete:
    """Tests for PlaybookService.delete_playbook."""
    
    def test_delete_draft_playbook_success(self, draft_playbook):
        """Test deleting a draft playbook."""
        playbook_id = draft_playbook.id
        
        PlaybookService.delete_playbook(draft_playbook)
        
        assert not Playbook.objects.filter(id=playbook_id).exists()
    
    def test_delete_released_playbook_raises_permission_error(self, released_playbook):
        """Test deleting a released playbook raises PermissionError."""
        with pytest.raises(PermissionError):
            PlaybookService.delete_playbook(released_playbook)


@pytest.mark.django_db
class TestPlaybookServiceDuplicate:
    """Tests for PlaybookService.duplicate_playbook."""
    
    def test_duplicate_playbook_success(self, maria, draft_playbook):
        """Test duplicating a playbook."""
        duplicate = PlaybookService.duplicate_playbook(
            draft_playbook,
            new_author=maria,
            new_name='Duplicated Playbook'
        )
        
        assert duplicate.id != draft_playbook.id
        assert duplicate.name == 'Duplicated Playbook'
        assert duplicate.description == draft_playbook.description
        assert duplicate.category == draft_playbook.category
        assert duplicate.status == 'draft'
        assert duplicate.version == Decimal('0.1')
        assert duplicate.author == maria


@pytest.mark.django_db
class TestPlaybookServiceRelease:
    """Tests for PlaybookService.release_playbook."""
    
    def test_release_draft_playbook_success(self, maria, draft_playbook):
        """Test releasing a draft playbook."""
        PlaybookService.release_playbook(draft_playbook.id, maria)
        
        draft_playbook.refresh_from_db()
        assert draft_playbook.status == 'released'
        assert draft_playbook.version == Decimal('1.0')
    
    def test_release_already_released_playbook_raises_error(self, maria, released_playbook):
        """Test releasing an already released playbook raises ValidationError."""
        with pytest.raises(ValidationError):
            PlaybookService.release_playbook(released_playbook.id, maria)
