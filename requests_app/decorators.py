from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def employee_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'profile') or request.user.profile.role not in ['employee', 'admin']:
            messages.error(request, 'Access denied.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
