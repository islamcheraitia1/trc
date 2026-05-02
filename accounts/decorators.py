from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles):
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if not hasattr(request.user, 'profile'):
                messages.error(request, 'User profile not found.')
                return redirect('login')
            if request.user.profile.role not in allowed_roles:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('request_list')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
