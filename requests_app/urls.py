from django.urls import path
from . import views

urlpatterns = [
    path('', views.request_list_view, name='request_list'),
    path('new/', views.request_create_view, name='request_create'),
    path('<int:pk>/', views.request_detail_view, name='request_detail'),
    path('<int:pk>/edit/', views.request_edit_view, name='request_edit'),
    path('<int:pk>/delete/', views.request_delete_view, name='request_delete'),
]
