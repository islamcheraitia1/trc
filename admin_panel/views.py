from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
import json
from requests_app.models import MaintenanceRequest
from requests_app.forms import AdminRequestForm
from accounts.decorators import role_required

@login_required
@role_required('admin')
def dashboard_view(request):
    total = MaintenanceRequest.objects.count()
    pending = MaintenanceRequest.objects.filter(status='pending').count()
    processing = MaintenanceRequest.objects.filter(status='processing').count()
    scheduled = MaintenanceRequest.objects.filter(status='scheduled').count()
    completed = MaintenanceRequest.objects.filter(status='completed').count()
    rejected = MaintenanceRequest.objects.filter(status='rejected').count()

    recent_requests = MaintenanceRequest.objects.select_related('requester').all()[:5]

    today = timezone.localtime(timezone.now()).date()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    daily_counts = []
    day_labels = []
    for day in last_7_days:
        count = MaintenanceRequest.objects.filter(created_at__date=day).count()
        daily_counts.append(count)
        day_labels.append(day.strftime('%a'))

    status_data = {
        'pending': pending,
        'processing': processing,
        'scheduled': scheduled,
        'completed': completed,
        'rejected': rejected,
    }

    context = {
        'stats': {
            'total': total,
            'pending': pending,
            'processing': processing,
            'scheduled': scheduled,
            'completed': completed,
            'rejected': rejected,
        },
        'recent_requests': recent_requests,
        'chart_labels': json.dumps(day_labels),
        'chart_data': json.dumps(daily_counts),
        'status_data': json.dumps(status_data),
    }
    return render(request, 'admin_panel/dashboard.html', context)

@login_required
@role_required('admin')
def admin_request_list_view(request):
    requests = MaintenanceRequest.objects.select_related('requester').all()
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    search = request.GET.get('search', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if status_filter:
        requests = requests.filter(status=status_filter)
    if priority_filter:
        requests = requests.filter(priority=priority_filter)
    if search:
        requests = requests.filter(
            Q(title__icontains=search) |
            Q(requester__username__icontains=search) |
            Q(office_location__icontains=search) |
            Q(destination_location__icontains=search) |
            Q(request_category__icontains=search) |
            Q(request_subcategory__icontains=search)
        )
    if date_from:
        dt = datetime.strptime(date_from, '%Y-%m-%d')
        start = timezone.make_aware(datetime(dt.year, dt.month, dt.day))
        requests = requests.filter(created_at__gte=start)
    if date_to:
        dt = datetime.strptime(date_to, '%Y-%m-%d')
        end = timezone.make_aware(datetime(dt.year, dt.month, dt.day) + timedelta(days=1))
        requests = requests.filter(created_at__lt=end)

    return render(request, 'admin_panel/request_list.html', {
        'requests': requests,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'search': search,
        'date_from': date_from,
        'date_to': date_to,
    })

@login_required
@role_required('admin')
def admin_request_detail_view(request, pk):
    req = get_object_or_404(MaintenanceRequest, id=pk)

    if request.method == 'POST' and 'delete' in request.POST:
        req.delete()
        messages.success(request, 'Request deleted successfully!')
        return redirect('admin_request_list')

    if request.method == 'POST' and 'update' in request.POST:
        form = AdminRequestForm(request.POST, request.FILES, instance=req)
        if form.is_valid():
            form.save()
            messages.success(request, 'Request updated successfully!')
            return redirect('admin_request_detail', pk)
    else:
        form = AdminRequestForm(instance=req)

    return render(request, 'admin_panel/request_detail.html', {'request_obj': req, 'form': form})

@login_required
@role_required('admin')
def calendar_view(request):
    scheduled_requests = MaintenanceRequest.objects.filter(
        status='scheduled',
        scheduled_date__isnull=False
    ).select_related('requester').order_by('scheduled_date')

    return render(request, 'admin_panel/calendar.html', {'requests': scheduled_requests})

@login_required
@role_required('admin')
def user_list_view(request):
    users = User.objects.select_related('profile').all().order_by('username')
    return render(request, 'admin_panel/user_list.html', {'users': users})

@login_required
@role_required('admin')
def user_delete_view(request, pk):
    user_to_delete = get_object_or_404(User, id=pk)
    
    if request.method == 'POST':
        if user_to_delete == request.user:
            messages.error(request, 'You cannot delete your own account.')
        else:
            user_to_delete.delete()
            messages.success(request, 'User deleted successfully.')
        
        return redirect('user_list')

    return redirect('user_list')
