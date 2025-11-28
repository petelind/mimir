"""
Custom logging filters for adding contextual information to log records.
"""
import logging
from django.utils.deprecation import MiddlewareMixin


class RequestIDFilter(logging.Filter):
    """
    Logging filter that adds request ID to log records.
    
    This filter extracts the request ID from thread-local storage
    (set by RequestIDMiddleware) and adds it to each log record.
    
    If no request ID is available (e.g., background tasks, startup),
    it uses 'NO_REQUEST' as a placeholder.
    
    Usage:
        Add this filter to LOGGING configuration in settings.py:
        
        'filters': {
            'request_id': {
                '()': 'mimir.logging_filters.RequestIDFilter',
            },
        }
    """
    
    def filter(self, record):
        """
        Add request_id attribute to log record.
        
        :param record: LogRecord instance to be filtered
        :return: True (always pass the record)
        
        Side effects:
            Adds 'request_id' attribute to record
        """
        # Try to get request ID from thread-local storage
        from mimir.request_local import get_current_request
        
        request = get_current_request()
        
        if request and hasattr(request, 'request_id'):
            record.request_id = request.request_id
        else:
            # No active request (e.g., management commands, background tasks)
            record.request_id = 'NO_REQUEST'
        
        return True
