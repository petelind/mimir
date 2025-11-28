"""
Middleware for request tracking and logging.
"""
import logging
import uuid
from django.utils.deprecation import MiddlewareMixin
from mimir.request_local import set_current_request, clear_current_request

logger = logging.getLogger(__name__)


class RequestIDMiddleware(MiddlewareMixin):
    """
    Middleware that generates or extracts a unique request ID for each request.
    
    The request ID is:
    - Generated as a UUID if not provided
    - Extracted from X-Request-ID header if present (for upstream propagation)
    - Stored in request.request_id for downstream use
    - Added to response headers as X-Request-ID
    
    This enables end-to-end request tracing across the application.
    
    Usage:
        Add 'mimir.middleware.RequestIDMiddleware' to MIDDLEWARE in settings.py
        Access via request.request_id in views
        All log messages will automatically include request_id
    """
    
    def process_request(self, request):
        """
        Extract or generate request ID and attach it to the request.
        
        :param request: Django request object
        :return: None
        
        Side effects:
            - Sets request.request_id attribute
            - Stores request in thread-local storage
            - Logs request initiation with request ID
        """
        # Check if request ID provided by upstream system (e.g., load balancer, API gateway)
        request_id = request.headers.get('X-Request-ID')
        
        if not request_id:
            # Generate new UUID for this request
            request_id = str(uuid.uuid4())
        
        # Attach to request for use throughout the request lifecycle
        request.request_id = request_id
        
        # Store in thread-local storage for logging filter access
        set_current_request(request)
        
        # Log request initiation
        logger.info(
            f"[REQUEST_START] {request.method} {request.path} - User: {getattr(request.user, 'username', 'anonymous')}"
        )
    
    def process_response(self, request, response):
        """
        Add request ID to response headers and clean up thread-local storage.
        
        :param request: Django request object
        :param response: Django response object
        :return: Modified response with X-Request-ID header
        """
        # Add request ID to response headers
        if hasattr(request, 'request_id'):
            response['X-Request-ID'] = request.request_id
            
            # Log request completion
            logger.info(
                f"[REQUEST_END] {request.method} {request.path} - Status: {response.status_code}"
            )
        
        # Clean up thread-local storage
        clear_current_request()
        
        return response
    
    def process_exception(self, request, exception):
        """
        Clean up thread-local storage on exception.
        
        :param request: Django request object
        :param exception: Exception that occurred
        :return: None
        """
        # Log exception with request ID
        if hasattr(request, 'request_id'):
            logger.error(
                f"[REQUEST_ERROR] {request.method} {request.path} - Exception: {exception.__class__.__name__}",
                exc_info=True
            )
        
        # Clean up thread-local storage
        clear_current_request()
        
        # Let Django handle the exception normally
        return None
