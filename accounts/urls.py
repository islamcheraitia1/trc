from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False), name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('admin-panel/users/', views.user_list_view, name='user_list'),
    path('admin-panel/users/<int:user_id>/toggle-role/', views.user_toggle_role, name='user_toggle_role'),
]
