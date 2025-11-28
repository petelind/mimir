"""
Integration tests for request ID logging middleware.
"""
import pytest
import re
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestRequestIDLogging:
    """Tests for request ID middleware and logging integration."""
    
    def test_request_id_in_response_headers(self):
        """Request ID should be present in response headers."""
        client = Client()
        response = client.get(reverse('login'))
        
        assert 'X-Request-ID' in response
        request_id = response['X-Request-ID']
        
        # Should be a valid UUID format
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        assert re.match(uuid_pattern, request_id), f"Invalid UUID format: {request_id}"
    
    def test_custom_request_id_propagated(self):
        """Custom request ID from header should be propagated to response."""
        client = Client()
        custom_request_id = 'custom-tracking-id-12345'
        
        response = client.get(
            reverse('login'),
            HTTP_X_REQUEST_ID=custom_request_id
        )
        
        assert 'X-Request-ID' in response
        assert response['X-Request-ID'] == custom_request_id
    
    def test_request_id_available_in_view(self):
        """Request ID should be accessible from request object in views."""
        client = Client()
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        client.force_login(user)
        
        response = client.get(reverse('dashboard'))
        
        # Verify request ID in response
        assert 'X-Request-ID' in response
        request_id = response['X-Request-ID']
        assert request_id  # Not empty
    
    def test_multiple_requests_have_different_ids(self):
        """Each request should get a unique request ID."""
        client = Client()
        
        response1 = client.get(reverse('login'))
        response2 = client.get(reverse('login'))
        
        request_id_1 = response1['X-Request-ID']
        request_id_2 = response2['X-Request-ID']
        
        assert request_id_1 != request_id_2, "Request IDs should be unique per request"
