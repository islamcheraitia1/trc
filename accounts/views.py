from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import activate
from django.conf import settings
from .forms import RegisterForm, ProfileForm
from .models import UserProfile
from .decorators import role_required

def set_language(request):
    if request.method == 'POST':
        language = request.POST.get('language', 'en')
        if language in ['en', 'fr']:
            request.session['django_language'] = language
            activate(language)
    return redirect(request.POST.get('next', '/'))

def login_view(request):
    if request.user.is_authenticated:
        return redirect('request_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        from django.contrib.auth import authenticate
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful!')
            if hasattr(user, 'profile') and user.profile.is_admin:
                return redirect('admin_dashboard')
            return redirect('request_list')
        messages.error(request, 'Invalid credentials')

    return render(request, 'accounts/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('request_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('request_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('login')

@login_required
def profile_view(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, user=request.user)

    return render(request, 'accounts/profile.html', {'form': form})

@login_required
@role_required('admin')
def user_list_view(request):
    users = User.objects.select_related('profile').all()
    return render(request, 'admin_panel/user_list.html', {'users': users})

@login_required
@role_required('admin')
def user_toggle_role(request, user_id):
    if request.method == 'POST':
        target_user = User.objects.get(id=user_id)
        if target_user == request.user:
            messages.error(request, 'You cannot change your own role.')
        else:
            profile = target_user.profile
            profile.role = 'employee' if profile.role == 'admin' else 'admin'
            profile.save()
            messages.success(request, f"Role updated for {target_user.username}")
    return redirect('user_list')
