"""URL configuration for playbook views."""

from django.urls import path
from methodology import playbook_views

urlpatterns = [
    path('', playbook_views.playbook_list, name='playbook_list'),
    
    # CREATE wizard (3 steps)
    path('create/', playbook_views.playbook_create, name='playbook_create'),
    path('create/step2/', playbook_views.playbook_create_step2, name='playbook_create_step2'),
    path('create/step3/', playbook_views.playbook_create_step3, name='playbook_create_step3'),
    
    # Legacy add endpoint (kept for backwards compatibility)
    path('add/', playbook_views.playbook_add, name='playbook_add'),
    
    # Detail, Edit, Delete
    path('<int:pk>/', playbook_views.playbook_detail, name='playbook_detail'),
    path('<int:pk>/edit/', playbook_views.playbook_edit, name='playbook_edit'),
    path('<int:pk>/delete/', playbook_views.playbook_delete, name='playbook_delete'),
    path('<int:pk>/delete/confirm/', playbook_views.playbook_delete_confirm, name='playbook_delete_confirm'),
]
