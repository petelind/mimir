"""
Integration tests for Playbook VIEW operation - Phase 1.

Tests PB-VIEW scenarios: 01-05, 21-24
"""

import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from methodology.models import Playbook, Workflow

User = get_user_model()


@pytest.fixture
def setup_playbook_data():
    """Create test data for playbook view tests."""
    user = User.objects.create_user(username='maria', password='testpass123')
    
    playbook = Playbook.objects.create(
        name='React Frontend Development',
        description='Comprehensive methodology for React development',
        category='development',
        tags=['react', 'frontend'],
        status='active',
        version=1,
        source='downloaded',
        author=user
    )
    
    # Create 3 workflows
    Workflow.objects.create(name='Component Design', playbook=playbook)
    Workflow.objects.create(name='State Management', playbook=playbook)
    Workflow.objects.create(name='Testing Strategy', playbook=playbook)
    
    return {'user': user, 'playbook': playbook}


@pytest.mark.django_db
class TestPlaybookViewPhase1:
    """Test Playbook VIEW Phase 1."""
    
    def test_pb_view_01_open_detail_page(self, setup_playbook_data):
        """PB-VIEW-01: Open playbook detail page."""
        client = Client()
        user = setup_playbook_data['user']
        playbook = setup_playbook_data['playbook']
        
        client.force_login(user)
        response = client.get(reverse('playbook_detail', kwargs={'pk': playbook.pk}))
        
        assert response.status_code == 200
        assert 'playbook' in response.context
    
    def test_pb_view_02_header_information(self, setup_playbook_data):
        """PB-VIEW-02: View header with version, status, author."""
        client = Client()
        user = setup_playbook_data['user']
        playbook = setup_playbook_data['playbook']
        
        client.force_login(user)
        response = client.get(reverse('playbook_detail', kwargs={'pk': playbook.pk}))
        
        content = response.content.decode('utf-8')
        assert 'React Frontend Development' in content
        assert 'v1' in content.lower() or 'version' in content.lower()
        assert 'active' in content.lower()
    
    def test_pb_view_03_overview_tab_default(self, setup_playbook_data):
        """PB-VIEW-03: Overview tab shows description and Quick Stats."""
        client = Client()
        user = setup_playbook_data['user']
        playbook = setup_playbook_data['playbook']
        
        client.force_login(user)
        response = client.get(reverse('playbook_detail', kwargs={'pk': playbook.pk}))
        
        content = response.content.decode('utf-8')
        assert 'Comprehensive methodology' in content
        assert 'workflows' in content.lower()
    
    def test_pb_view_04_metadata_section(self, setup_playbook_data):
        """PB-VIEW-04: Metadata shows category, tags, source."""
        client = Client()
        user = setup_playbook_data['user']
        playbook = setup_playbook_data['playbook']
        
        client.force_login(user)
        response = client.get(reverse('playbook_detail', kwargs={'pk': playbook.pk}))
        
        content = response.content.decode('utf-8')
        assert 'development' in content.lower()
        assert 'react' in content.lower()
    
    def test_pb_view_05_workflows_list(self, setup_playbook_data):
        """PB-VIEW-05: Workflows section shows all workflows."""
        client = Client()
        user = setup_playbook_data['user']
        playbook = setup_playbook_data['playbook']
        
        client.force_login(user)
        response = client.get(reverse('playbook_detail', kwargs={'pk': playbook.pk}))
        
        content = response.content.decode('utf-8')
        assert 'Component Design' in content
        assert 'State Management' in content
        assert 'Testing Strategy' in content
    
    def test_pb_view_21_back_to_list(self, setup_playbook_data):
        """PB-VIEW-21: Back button links to playbooks list."""
        client = Client()
        user = setup_playbook_data['user']
        playbook = setup_playbook_data['playbook']
        
        client.force_login(user)
        response = client.get(reverse('playbook_detail', kwargs={'pk': playbook.pk}))
        
        content = response.content.decode('utf-8')
        playbook_list_url = reverse('playbook_list')
        assert playbook_list_url in content
    
    def test_pb_view_22_breadcrumb_navigation(self, setup_playbook_data):
        """PB-VIEW-22: Breadcrumbs show path and are clickable."""
        client = Client()
        user = setup_playbook_data['user']
        playbook = setup_playbook_data['playbook']
        
        client.force_login(user)
        response = client.get(reverse('playbook_detail', kwargs={'pk': playbook.pk}))
        
        content = response.content.decode('utf-8')
        assert 'breadcrumb' in content.lower()
        assert 'Playbooks' in content
    
    def test_pb_view_23_phases_optional(self, setup_playbook_data):
        """PB-VIEW-23: Phases count shows 0 when not implemented."""
        client = Client()
        user = setup_playbook_data['user']
        playbook = setup_playbook_data['playbook']
        
        client.force_login(user)
        response = client.get(reverse('playbook_detail', kwargs={'pk': playbook.pk}))
        
        stats = response.context['playbook'].get_quick_stats()
        assert stats['phases'] == 0
    
    def test_pb_view_24_status_badge_colors(self, setup_playbook_data):
        """PB-VIEW-24: Status badges use correct Bootstrap colors."""
        client = Client()
        user = setup_playbook_data['user']
        
        # Active = success (green)
        pb_active = Playbook.objects.create(
            name='Active', description='Test', category='product',
            status='active', author=user
        )
        client.force_login(user)
        response = client.get(reverse('playbook_detail', kwargs={'pk': pb_active.pk}))
        content = response.content.decode('utf-8')
        assert 'success' in content.lower() or 'bg-success' in content.lower()
        
        # Draft = warning (yellow)
        pb_draft = Playbook.objects.create(
            name='Draft', description='Test', category='product',
            status='draft', author=user
        )
        response = client.get(reverse('playbook_detail', kwargs={'pk': pb_draft.pk}))
        content = response.content.decode('utf-8')
        assert 'warning' in content.lower() or 'bg-warning' in content.lower()
