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
    Dashboard view with activity feed and recent playbooks (FOB-DASHBOARD-1).
    
    Displays user's personalized dashboard with:
    - My Playbooks section (5 most recent playbooks)
    - Recent Activity feed (10 most recent actions)
    - Quick Actions panel
    
    Template: dashboard.html
    Context:
        recent_playbooks: List of recent Playbook objects
        recent_activities: QuerySet of recent Activity objects
        activity_count: Number of recent activities
        playbook_count: Number of recent playbooks
    
    :param request: Django request object. Example: HttpRequest(method='GET', user=<User: maria>)
    :return: Rendered HTML response with dashboard data. Example: HttpResponse(status=200, content="<div>...</div>")
    :raises: None - handles all exceptions gracefully
    """
    logger.info(f"User {request.user.username} accessing dashboard")
    
    try:
        # Initialize activity service
        from methodology.services.activity_service import ActivityService
        activity_service = ActivityService()
        
        # Get dashboard data
        feed_data = activity_service.get_activity_feed_data(request.user)
        
        # Log dashboard view activity
        activity_service.log_activity(
            user=request.user,
            action_type='dashboard_viewed',
            description=f"{request.user.username} viewed dashboard"
        )
        
        logger.info(f"Dashboard loaded for {request.user.username}: {feed_data['playbook_count']} playbooks, {feed_data['activity_count']} activities")
        
        return render(request, 'dashboard.html', {
            'recent_playbooks': feed_data['recent_playbooks'],
            'recent_activities': feed_data['recent_activities'],
            'activity_count': feed_data['activity_count'],
            'playbook_count': feed_data['playbook_count'],
        })
        
    except Exception as e:
        logger.error(f"Error loading dashboard for {request.user.username}: {e}")
        # Return dashboard with empty data rather than error page
        return render(request, 'dashboard.html', {
            'recent_playbooks': [],
            'recent_activities': [],
            'activity_count': 0,
            'playbook_count': 0,
            'error_message': 'Unable to load some dashboard data'
        })
