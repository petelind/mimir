"""
Thread-local storage for the current request.

This module provides a way to access the current request from anywhere
in the application, which is useful for logging and context propagation.
"""
import threading

_thread_locals = threading.local()


def set_current_request(request):
    """
    Store the current request in thread-local storage.
    
    :param request: Django request object
    :return: None
    """
    _thread_locals.request = request


def get_current_request():
    """
    Retrieve the current request from thread-local storage.
    
    :return: Django request object or None if not set
    """
    return getattr(_thread_locals, 'request', None)


def clear_current_request():
    """
    Clear the current request from thread-local storage.
    
    :return: None
    """
    if hasattr(_thread_locals, 'request'):
        del _thread_locals.request
