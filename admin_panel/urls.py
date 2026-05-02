from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='admin_dashboard'),
    path('requests/', views.admin_request_list_view, name='admin_request_list'),
    path('requests/<int:pk>/', views.admin_request_detail_view, name='admin_request_detail'),
    path('calendar/', views.calendar_view, name='admin_calendar'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/<int:pk>/delete/', views.user_delete_view, name='user_delete'),
]
