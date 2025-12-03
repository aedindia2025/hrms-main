from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.http import require_POST

from entry.models import CompOffEntry
from master.models import Employee, Site
from .models import HRCompOffApproval


# ==================== HR Approval ====================
@permission_required('approval.view_hrcompoffapproval', raise_exception=True)
def hr_comp_off_approval(request):
    """Approval -> HR Comp-Off Approval list with filters & pagination."""
    per_page = request.GET.get('per_page', '').strip() or '10'
    search_query = request.GET.get('q', '').strip()
    page_number = request.GET.get('page')

    from_date = request.GET.get('from_date', '').strip()
    to_date = request.GET.get('to_date', '').strip()
    site_id = request.GET.get('site', '').strip()
    employee_id = request.GET.get('employee', '').strip()
    status = request.GET.get('status', '').strip()

    try:
        per_page_value = max(int(per_page), 1)
    except ValueError:
        per_page_value = 10

    comp_off_entries = CompOffEntry.objects.select_related('employee', 'site')

    if search_query:
        comp_off_entries = comp_off_entries.filter(
            Q(employee__staff_name__icontains=search_query)
            | Q(employee__staff_id__icontains=search_query)
            | Q(site__name__icontains=search_query)
            | Q(head_approval_by__icontains=search_query)
        )

    if from_date:
        comp_off_entries = comp_off_entries.filter(work_date__gte=from_date)
    if to_date:
        comp_off_entries = comp_off_entries.filter(work_date__lte=to_date)
    if site_id:
        comp_off_entries = comp_off_entries.filter(site_id=site_id)
    if employee_id:
        comp_off_entries = comp_off_entries.filter(employee_id=employee_id)
    if status:
        comp_off_entries = comp_off_entries.filter(head_approval_status=status)

    comp_off_entries = comp_off_entries.order_by('-work_date', 'employee__staff_name')

    paginator = Paginator(comp_off_entries, per_page_value)
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop('page', None)
    base_querystring = query_params.urlencode()
    page_query_base = f'{base_querystring}&' if base_querystring else ''

    # Get HR approvals for the entries
    entry_ids = [entry.id for entry in page_obj]
    hr_approvals = {
        approval.comp_off_entry_id: approval
        for approval in HRCompOffApproval.objects.filter(
            comp_off_entry_id__in=entry_ids
        ).select_related('hr_approval_by')
    }

    context = {
        'comp_off_entries': page_obj,
        'hr_approvals': hr_approvals,
        'page_obj': page_obj,
        'search_query': search_query,
        'per_page': str(per_page_value),
        'per_page_value': per_page_value,
        'base_querystring': base_querystring,
        'page_query_base': page_query_base,
        'total_entries': paginator.count,
        'from_date': from_date,
        'to_date': to_date,
        'filter_site_id': site_id,
        'filter_employee_id': employee_id,
        'filter_status': status,
        'sites': Site.objects.order_by('name'),
        'employees': Employee.objects.order_by('staff_name'),
        'approval_choices': HRCompOffApproval.APPROVAL_CHOICES,
    }
    return render(request, 'approval/hr_approval/list.html', context)

@permission_required('approval.approve_hrcompoffapproval', raise_exception=True)
@require_POST
def hr_comp_off_approval_update(request, pk):
    """
    Update HR approval status using the HRCompOffApproval model.
    Also updates the CompOffEntry for backward compatibility.
    """
    comp_off_entry = get_object_or_404(CompOffEntry, pk=pk)
    
    # Get or create HR approval record
    hr_approval, created = HRCompOffApproval.objects.get_or_create(
        comp_off_entry=comp_off_entry
    )

    new_status = request.POST.get('status', '').strip()
    note = request.POST.get('note', '').strip()

    valid_statuses = {choice[0] for choice in HRCompOffApproval.APPROVAL_CHOICES}
    if new_status not in valid_statuses:
        messages.error(request, 'Invalid approval status.')
    else:
        # Update HR approval model
        hr_approval.hr_approval_status = new_status
        hr_approval.hr_approval_by = request.user
        hr_approval.hr_approval_note = note
        hr_approval.hr_approval_date = timezone.now()
        hr_approval.save()
        
        # Also update CompOffEntry for backward compatibility
        comp_off_entry.head_approval_status = new_status
        comp_off_entry.head_approval_by = (
            request.user.get_full_name() or request.user.get_username()
        )
        comp_off_entry.head_approval_note = note
        comp_off_entry.save()
        
        messages.success(request, 'HR approval status updated successfully.')

    # Redirect back to the referring page if available, otherwise to the list view
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('approval:hr_comp_off_approval')


# ==================== Daily Attendance ====================
@permission_required('master.view_employee', raise_exception=True)
def daily_attendance_print(request):
    """Approval -> Daily Attendance -> Print view."""
    return render(request, 'approval/dailyAttendance_approval/print.html')


# ==================== Leave ====================
@permission_required('approval.view_leaveapproval', raise_exception=True)
def leave_approval_list(request):
    """Approval -> Leave Approval list."""
    return render(request, 'approval/leave_approval/list.html')


# ==================== Permission ====================
@permission_required('approval.view_permissionapproval', raise_exception=True)
def permission_approval_list(request):
    """Approval -> Permission Approval list."""
    return render(request, 'approval/permission_approval/list.html')


# ==================== TADA ====================
@permission_required('approval.view_tadaapproval', raise_exception=True)
def tada_approval_list(request):
    """Approval -> TADA Approval list."""
    return render(request, 'approval/tada_approval/list.html')

@permission_required('approval.view_tadaapproval', raise_exception=True)
def tada_head_approval_list(request):
    """Approval -> TADA Head Approval list."""
    return render(request, 'approval/tadaHead_approval/list.html')

@permission_required('approval.view_tadaapproval', raise_exception=True)
def tada_hr_approval_list(request):
    """Approval -> TADA HR Approval list."""
    return render(request, 'approval/tadaHr_approval/list.html')

@permission_required('approval.view_tadaapproval', raise_exception=True)
def tada_hr_print(request):
    """Approval -> TADA HR Print page."""
    return render(request, 'approval/tadaHr_approval/print.html')


# ==================== Travel HR ====================
@permission_required('approval.view_travelapproval', raise_exception=True)
def travel_hr_approval_list(request):
    """Approval -> Travel HR Approval list."""
    return render(request, 'approval/travelHr_approval/list.html')
