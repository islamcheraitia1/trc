from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import MaintenanceRequest
from .forms import MaintenanceRequestForm
from accounts.decorators import role_required

@login_required
@role_required(['employee', 'admin'])
def request_list_view(request):
    requests = MaintenanceRequest.objects.filter(requester=request.user)
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if status_filter:
        requests = requests.filter(status=status_filter)
    if priority_filter:
        requests = requests.filter(priority=priority_filter)
    if date_from:
        dt = datetime.strptime(date_from, '%Y-%m-%d')
        start = timezone.make_aware(datetime(dt.year, dt.month, dt.day))
        requests = requests.filter(created_at__gte=start)
    if date_to:
        dt = datetime.strptime(date_to, '%Y-%m-%d')
        end = timezone.make_aware(datetime(dt.year, dt.month, dt.day) + timedelta(days=1))
        requests = requests.filter(created_at__lt=end)

    return render(request, 'requests_app/request_list.html', {
        'requests': requests,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'date_from': date_from,
        'date_to': date_to,
    })

@login_required
@role_required(['employee', 'admin'])
def request_create_view(request):
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            req = form.save(commit=False)
            req.requester = request.user
            if req.request_category != 'deplacement':
                req.destination_location = ''
            req.save()
            messages.success(request, 'Request created successfully!')
            return redirect('request_detail', req.id)
    else:
        initial = {}
        if hasattr(request.user, 'profile'):
            initial['office_location'] = request.user.profile.office_location
        form = MaintenanceRequestForm(initial=initial)

    return render(request, 'requests_app/request_form.html', {'form': form, 'title': 'New Request'})

@login_required
@role_required(['employee', 'admin'])
def request_detail_view(request, pk):
    req = get_object_or_404(MaintenanceRequest, id=pk, requester=request.user)
    return render(request, 'requests_app/request_detail.html', {'request_obj': req})

@login_required
@role_required(['employee', 'admin'])
def request_edit_view(request, pk):
    req = get_object_or_404(MaintenanceRequest, id=pk, requester=request.user)

    if req.status != 'pending':
        messages.error(request, 'Only pending requests can be edited.')
        return redirect('request_detail', pk)

    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST, request.FILES, instance=req)
        if form.is_valid():
            updated = form.save(commit=False)
            if updated.request_category != 'deplacement':
                updated.destination_location = ''
            updated.save()
            messages.success(request, 'Request updated successfully!')
            return redirect('request_detail', pk)
    else:
        form = MaintenanceRequestForm(instance=req)

    return render(request, 'requests_app/request_form.html', {'form': form, 'title': 'Edit Request'})

@login_required
@role_required(['employee', 'admin'])
def request_delete_view(request, pk):
    req = get_object_or_404(MaintenanceRequest, id=pk, requester=request.user)

    if req.status != 'pending':
        messages.error(request, 'Only pending requests can be deleted.')
        return redirect('request_detail', pk)

    if request.method == 'POST':
        req.delete()
        messages.success(request, 'Request deleted successfully!')
        return redirect('request_list')

    return render(request, 'requests_app/request_confirm_delete.html', {'request_obj': req})
