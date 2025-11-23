"""Views for the methodology app."""
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

logger = logging.getLogger(__name__)


def index(request):
    """
    Home page - methodology explorer landing page. Public access allowed.
    
    :param request: Django request object. Example: HttpRequest(method='GET', user=<User: admin>)
    :return: Rendered HTML response. Example: HttpResponse(status=200, content="<div>...</div>")
    """
    return render(request, 'methodology/index.html')


@login_required
def dashboard(request):
    """
    Dashboard stub page (FOB-DASHBOARD-1).
    
    Placeholder view for dashboard. Full implementation tracked separately
    in navigation.feature issues #17-22.
    
    Template: dashboard.html
    Context: None
    
    :param request: Django request object
    :return: Rendered dashboard stub template
    """
    logger.info(f"User {request.user.username} accessed dashboard stub")
    return render(request, 'dashboard.html')
