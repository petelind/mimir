"""Integration tests for Playbook VIEW Phase 2 - Action buttons."""

import pytest
import json
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from methodology.models import Playbook, Workflow

User = get_user_model()


@pytest.fixture
def owned_playbook():
    """Create owned playbook."""
    user = User.objects.create_user(username='maria', password='test123')
    pb = Playbook.objects.create(
        name='Product Discovery Framework',
        description='My methodology',
        category='product',
        status='active',
        source='owned',
        author=user
    )
    Workflow.objects.create(name='Research', playbook=pb)
    return {'user': user, 'playbook': pb}


@pytest.fixture
def downloaded_playbook():
    """Create downloaded playbook."""
    user = User.objects.create_user(username='bob', password='test123')
    pb = Playbook.objects.create(
        name='React Dev',
        description='Downloaded',
        category='development',
        status='active',
        source='downloaded',
        author=user
    )
    return {'user': user, 'playbook': pb}


@pytest.mark.django_db
class TestPlaybookViewPhase2:
    """Test Phase 2 - Action buttons."""
    
    def test_pb_view_14_owned_can_edit(self, owned_playbook):
        """PB-VIEW-14: Owned playbooks are editable."""
        client = Client()
        client.force_login(owned_playbook['user'])
        response = client.get(reverse('playbook_detail', kwargs={'pk': owned_playbook['playbook'].pk}))
        assert response.context['can_edit'] == True
    
    def test_pb_view_15_downloaded_not_editable(self, downloaded_playbook):
        """PB-VIEW-15: Downloaded playbooks are not editable."""
        client = Client()
        client.force_login(downloaded_playbook['user'])
        response = client.get(reverse('playbook_detail', kwargs={'pk': downloaded_playbook['playbook'].pk}))
        assert response.context['can_edit'] == False
    
    def test_pb_view_18_export_json(self, owned_playbook):
        """PB-VIEW-18: Export playbook to JSON."""
        client = Client()
        client.force_login(owned_playbook['user'])
        
        response = client.get(reverse('playbook_export', kwargs={'pk': owned_playbook['playbook'].pk}))
        
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json'
        assert 'product-discovery-framework' in response['Content-Disposition'].lower()
        
        data = json.loads(response.content)
        assert data['name'] == 'Product Discovery Framework'
    
    def test_pb_view_19_duplicate_playbook(self, owned_playbook):
        """PB-VIEW-19: Duplicate creates new playbook."""
        client = Client()
        client.force_login(owned_playbook['user'])
        
        response = client.post(
            reverse('playbook_duplicate', kwargs={'pk': owned_playbook['playbook'].pk}),
            {'new_name': 'Product Discovery Framework (Copy)'}
        )
        
        assert response.status_code == 302
        assert Playbook.objects.filter(name='Product Discovery Framework (Copy)').exists()
    
    def test_pb_view_20_toggle_status(self, owned_playbook):
        """PB-VIEW-20: Toggle status between active/disabled."""
        client = Client()
        client.force_login(owned_playbook['user'])
        pb = owned_playbook['playbook']
        
        assert pb.status == 'active'
        
        response = client.post(reverse('playbook_toggle_status', kwargs={'pk': pb.pk}))
        assert response.status_code == 302
        
        pb.refresh_from_db()
        assert pb.status == 'disabled'
        
        # Toggle back
        client.post(reverse('playbook_toggle_status', kwargs={'pk': pb.pk}))
        pb.refresh_from_db()
        assert pb.status == 'active'
