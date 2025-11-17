"""URL configuration for playbook views."""

from django.urls import path
from . import playbook_views

urlpatterns = [
    path('', playbook_views.playbook_list, name='playbook_list'),
    path('add/', playbook_views.playbook_add, name='playbook_add'),
    path('<str:playbook_id>/', playbook_views.playbook_detail, name='playbook_detail'),
    path('<str:playbook_id>/edit/', playbook_views.playbook_edit, name='playbook_edit'),
]
