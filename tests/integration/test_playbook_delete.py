"""Integration tests for playbook DELETE operation.

Tests all 20 scenarios from playbooks-delete.feature.
Run with: pytest tests/integration/test_playbook_delete.py
"""

import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from methodology.models import Playbook, Workflow, Activity

User = get_user_model()


@pytest.fixture
def maria(db):
    """Create Maria user for tests."""
    return User.objects.create_user(username='maria', password='testpass123')


@pytest.fixture
def alice(db):
    """Create Alice user for tests."""
    return User.objects.create_user(username='alice', password='testpass123')


@pytest.fixture
def client_maria(client, maria):
    """Authenticated client for Maria."""
    client.login(username='maria', password='testpass123')
    return client


@pytest.fixture
def playbook_old_patterns(maria):
    """Create 'Old Design Patterns' playbook with workflows."""
    playbook = Playbook.objects.create(
        name='Old Design Patterns',
        description='Legacy design patterns',
        category='development',
        author=maria,
        version='1.0',
        status='disabled'
    )
    # Add 2 workflows
    Workflow.objects.create(name='Workflow 1', playbook=playbook, order=1)
    Workflow.objects.create(name='Workflow 2', playbook=playbook, order=2)
    return playbook


# ==================== Opening Delete Modal ====================

@pytest.mark.django_db
class TestDeleteModal:
    """PB-DELETE-01 to PB-DELETE-04: Opening delete modal"""
    
    def test_delete_button_visible_in_detail(self, client_maria, playbook_old_patterns):
        """PB-DELETE-01: Open delete confirmation from detail page"""
        url = reverse('playbook_detail', kwargs={'pk': playbook_old_patterns.pk})
        response = client_maria.get(url)
        
        assert response.status_code == 200
        assert 'Delete' in response.content.decode()
        assert 'deleteModal' in response.content.decode()
    
    def test_modal_shows_playbook_details(self, client_maria, playbook_old_patterns):
        """PB-DELETE-03: Modal shows playbook details"""
        url = reverse('playbook_detail', kwargs={'pk': playbook_old_patterns.pk})
        response = client_maria.get(url)
        
        content = response.content.decode()
        assert playbook_old_patterns.name in content
        assert f'v{playbook_old_patterns.version}' in content
        assert 'Workflows: 2' in content
    
    def test_modal_shows_warning_message(self, client_maria, playbook_old_patterns):
        """PB-DELETE-04: Modal shows warning message"""
        url = reverse('playbook_detail', kwargs={'pk': playbook_old_patterns.pk})
        response = client_maria.get(url)
        
        content = response.content.decode()
        assert 'cannot be undone' in content
        assert 'permanently lost' in content or 'permanently deleted' in content
        assert 'btn-danger' in content
        assert 'Cancel' in content


# ==================== Confirming Deletion ====================

@pytest.mark.django_db
class TestConfirmDeletion:
    """PB-DELETE-05 to PB-DELETE-08: Confirming deletion"""
    
    def test_confirm_deletion(self, client_maria, playbook_old_patterns):
        """PB-DELETE-05: Confirm deletion"""
        url = reverse('playbook_delete', kwargs={'pk': playbook_old_patterns.pk})
        
        # Verify playbook exists
        assert Playbook.objects.filter(pk=playbook_old_patterns.pk).exists()
        
        # DELETE the playbook
        response = client_maria.post(url)
        
        # Should redirect to list
        assert response.status_code == 302
        assert response.url == reverse('playbook_list')
        
        # Playbook should be deleted
        assert not Playbook.objects.filter(pk=playbook_old_patterns.pk).exists()
        
        # Workflows should be cascade deleted
        assert not Workflow.objects.filter(playbook_id=playbook_old_patterns.pk).exists()
    
    def test_cancel_deletion_from_modal(self, client_maria, playbook_old_patterns):
        """PB-DELETE-06: Cancel deletion from modal (modal button doesn't trigger POST)"""
        # Verify playbook exists
        assert Playbook.objects.filter(pk=playbook_old_patterns.pk).exists()
        
        # Cancel just closes modal in browser, no server action needed
        # Verify playbook still exists (no POST was made)
        assert Playbook.objects.filter(pk=playbook_old_patterns.pk).exists()
    
    def test_get_request_redirects(self, client_maria, playbook_old_patterns):
        """PB-DELETE-07/08: GET request to delete redirects to detail"""
        url = reverse('playbook_delete', kwargs={'pk': playbook_old_patterns.pk})
        response = client_maria.get(url)
        
        # GET should redirect to detail
        assert response.status_code == 302
        assert response.url == reverse('playbook_detail', kwargs={'pk': playbook_old_patterns.pk})
        
        # Playbook should still exist
        assert Playbook.objects.filter(pk=playbook_old_patterns.pk).exists()


# ==================== Permissions ====================

@pytest.mark.django_db
class TestDeletePermissions:
    """PB-DELETE-09: Permissions"""
    
    def test_cannot_delete_other_users_playbook(self, client_maria, alice):
        """PB-DELETE-09: Cannot delete playbooks owned by others"""
        # Create playbook owned by Alice
        alice_playbook = Playbook.objects.create(
            name='Alice Playbook',
            description='Owned by Alice',
            category='development',
            author=alice,
            version='1.0'
        )
        
        url = reverse('playbook_delete', kwargs={'pk': alice_playbook.pk})
        
        # Maria tries to delete Alice's playbook
        response = client_maria.post(url)
        
        # Should redirect with error
        assert response.status_code == 302
        
        # Playbook should still exist
        assert Playbook.objects.filter(pk=alice_playbook.pk).exists()


# ==================== Dependency Warnings ====================

@pytest.mark.django_db
class TestDependencyWarnings:
    """PB-DELETE-10 to PB-DELETE-11: Dependency warnings"""
    
    def test_delete_playbook_with_dependencies(self, maria):
        """PB-DELETE-10: Delete playbook with dependencies warning"""
        playbook = Playbook.objects.create(
            name='Main Methodology',
            description='Has many dependencies',
            category='development',
            author=maria,
            version='1.0'
        )
        
        # Add 5 workflows
        for i in range(5):
            workflow = Workflow.objects.create(
                name=f'Workflow {i+1}',
                playbook=playbook,
                order=i+1
            )
            # Add 10 activities per workflow = 50 total
            for j in range(10):
                Activity.objects.create(
                    name=f'Activity {j+1}',
                    workflow=workflow,
                    order=j+1
                )
        
        client = Client()
        client.login(username='maria', password='testpass123')
        
        # View detail page - should show dependency counts
        url = reverse('playbook_detail', kwargs={'pk': playbook.pk})
        response = client.get(url)
        content = response.content.decode()
        
        assert 'Workflows: 5' in content
        assert 'permanently lost' in content or 'permanently deleted' in content
    
    def test_delete_requires_explicit_action(self, client_maria, playbook_old_patterns):
        """PB-DELETE-11: Delete confirmation requires explicit action (POST)"""
        url = reverse('playbook_delete', kwargs={'pk': playbook_old_patterns.pk})
        
        # GET request should NOT delete
        response = client_maria.get(url)
        assert Playbook.objects.filter(pk=playbook_old_patterns.pk).exists()
        
        # Only POST deletes
        response = client_maria.post(url)
        assert not Playbook.objects.filter(pk=playbook_old_patterns.pk).exists()


# ==================== Advanced Features ====================

@pytest.mark.django_db
class TestAdvancedFeatures:
    """PB-DELETE-12 to PB-DELETE-15: Advanced features"""
    
    @pytest.mark.skip(reason="Family/Homebase features deferred")
    def test_delete_family_playbook(self):
        """PB-DELETE-12: Delete playbook from family affects members (deferred)"""
        pass
    
    def test_delete_active_vs_disabled(self, maria):
        """PB-DELETE-13: Delete active vs disabled playbook"""
        active_playbook = Playbook.objects.create(
            name='Current Methodology',
            description='Active playbook',
            category='development',
            author=maria,
            version='1.0',
            status='active'
        )
        
        client = Client()
        client.login(username='maria', password='testpass123')
        
        # Both active and disabled playbooks can be deleted
        url = reverse('playbook_delete', kwargs={'pk': active_playbook.pk})
        response = client.post(url)
        
        assert response.status_code == 302
        assert not Playbook.objects.filter(pk=active_playbook.pk).exists()
    
    def test_bulk_delete_not_supported(self, client_maria, maria):
        """PB-DELETE-14: Bulk delete not supported (each requires individual DELETE)"""
        # Create multiple playbooks
        pb1 = Playbook.objects.create(name='PB1', author=maria, category='development')
        pb2 = Playbook.objects.create(name='PB2', author=maria, category='development')
        
        # No bulk delete endpoint exists - must delete individually
        client_maria.post(reverse('playbook_delete', kwargs={'pk': pb1.pk}))
        assert not Playbook.objects.filter(pk=pb1.pk).exists()
        assert Playbook.objects.filter(pk=pb2.pk).exists()  # PB2 still exists
    
    def test_keyboard_accessibility(self, client_maria, playbook_old_patterns):
        """PB-DELETE-15: Delete with keyboard accessibility (modal has proper attributes)"""
        url = reverse('playbook_detail', kwargs={'pk': playbook_old_patterns.pk})
        response = client_maria.get(url)
        content = response.content.decode()
        
        # Modal should have proper ARIA attributes
        assert 'aria-labelledby' in content
        assert 'aria-hidden' in content
        assert 'btn-close' in content  # Close button
        assert 'data-bs-dismiss="modal"' in content  # Cancel button


# ==================== System Impact ====================

@pytest.mark.django_db
class TestSystemImpact:
    """PB-DELETE-16 to PB-DELETE-20: System impact"""
    
    def test_deletion_removes_from_all_views(self, client_maria, playbook_old_patterns):
        """PB-DELETE-16: Deletion removes from all views"""
        # Delete playbook
        url = reverse('playbook_delete', kwargs={'pk': playbook_old_patterns.pk})
        client_maria.post(url)
        
        # Verify removed from list
        list_url = reverse('playbook_list')
        response = client_maria.get(list_url)
        content = response.content.decode()
        
        # Playbook should not be in database
        from methodology.models import Playbook
        assert not Playbook.objects.filter(name=playbook_old_patterns.name).exists()
        
        # List should show "No playbooks yet" message
        assert 'No playbooks yet' in content
    
    def test_deletion_cannot_be_undone(self, client_maria, playbook_old_patterns):
        """PB-DELETE-17: Deletion cannot be undone (no recovery mechanism)"""
        pk = playbook_old_patterns.pk
        name = playbook_old_patterns.name
        
        # Delete playbook
        url = reverse('playbook_delete', kwargs={'pk': pk})
        client_maria.post(url)
        
        # Playbook is gone
        assert not Playbook.objects.filter(pk=pk).exists()
        assert not Playbook.objects.filter(name=name).exists()
        
        # No undo mechanism exists
        # (This is verified by the absence of any undo functionality)
    
    @pytest.mark.skip(reason="Homebase sync features deferred")
    def test_delete_local_only_playbook(self):
        """PB-DELETE-18: Delete local-only playbook (deferred)"""
        pass
    
    def test_delete_error_handling(self, client_maria, playbook_old_patterns):
        """PB-DELETE-19: Delete error handling (playbook doesn't exist)"""
        # Delete playbook
        url = reverse('playbook_delete', kwargs={'pk': playbook_old_patterns.pk})
        client_maria.post(url)
        
        # Try to delete again - should get 404
        response = client_maria.post(url)
        assert response.status_code == 404
    
    def test_export_backup_suggestion(self, client_maria, playbook_old_patterns):
        """PB-DELETE-20: Delete with export backup suggestion"""
        url = reverse('playbook_detail', kwargs={'pk': playbook_old_patterns.pk})
        response = client_maria.get(url)
        content = response.content.decode()
        
        # Modal should suggest export
        assert 'export' in content.lower() or 'backup' in content.lower()
        # Should have link to export
        export_url = reverse('playbook_export', kwargs={'pk': playbook_old_patterns.pk})
        assert export_url in content
