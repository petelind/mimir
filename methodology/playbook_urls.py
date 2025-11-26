"""URL configuration for playbook views."""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.playbook_list, name='playbook_list'),
    path('add/', views.playbook_add, name='playbook_add'),
    path('create/step1/', views.playbook_create_step1, name='playbook_create_step1'),
    path('create/step2/', views.playbook_create_step2, name='playbook_create_step2'),
    path('create/step3/', views.playbook_create_step3, name='playbook_create_step3'),
    path('<str:playbook_id>/', views.playbook_detail, name='playbook_detail'),
    path('<str:playbook_id>/edit/', views.playbook_edit, name='playbook_edit'),
]
