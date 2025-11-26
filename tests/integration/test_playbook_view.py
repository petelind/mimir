"""Integration tests for Playbook VIEW operations."""

import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from methodology.models import Playbook, Workflow

User = get_user_model()


@pytest.mark.django_db
class TestPlaybookView:
    """Integration tests for playbook detail view - 24 scenarios."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='maria_test',
            email='maria@test.com',
            password='testpass123'
        )
        self.client.login(username='maria_test', password='testpass123')
        
        self.playbook = Playbook.objects.create(
            name='React Frontend Development',
            description='A comprehensive methodology',
            category='development',
            tags=['react', 'frontend'],
            status='active',
            version=2,
            author=self.user
        )
    
    def test_pb_view_01_open_playbook_detail_page(self):
        """PB-VIEW-01: Open playbook detail page."""
        response = self.client.get(reverse('playbook_detail', kwargs={'pk': self.playbook.id}))
        assert response.status_code == 200
