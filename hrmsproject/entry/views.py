 # entry/views.py
import json
from decimal import Decimal, InvalidOperation
from datetime import datetime, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Q

from master.models import Employee, Site, ExpenseType, SubExpense
from .models import CompOffEntry, SiteEntry, PermissionEntry, LeaveEntry, TADAEntry, TADAEntrySubItem

# ------------------------
# ENTRY -> COMP OFF
# ------------------------
@permission_required('entry.add_compoffentry', raise_exception=True)
def comp_off_create(request):
    employees = Employee.objects.order_by('staff_name')
    sites = Site.objects.order_by('name')

    values = {
        'work_date': '',
        'site': '',
        'employee': '',
        'in_time': '',
        'out_time': '',
        'day_status': '',
    }
    errors = {}

    if request.method == 'POST':
        values['work_date'] = request.POST.get('work_date', '').strip()
        values['site'] = request.POST.get('site', '').strip()
        values['employee'] = request.POST.get('employee', '').strip()
        values['in_time'] = request.POST.get('in_time', '').strip()
        values['out_time'] = request.POST.get('out_time', '').strip()
        values['day_status'] = request.POST.get('day_status', '').strip()

        work_date_obj = None
        in_time_obj = None
        out_time_obj = None

        if not values['work_date']:
            errors['work_date'] = 'Work date is required.'
        else:
            try:
                work_date_obj = datetime.strptime(values['work_date'], '%Y-%m-%d').date()
            except ValueError:
                errors['work_date'] = 'Invalid date format.'

        if not values['employee']:
            errors['employee'] = 'Employee selection is required.'
        elif not Employee.objects.filter(pk=values['employee']).exists():
            errors['employee'] = 'Selected employee does not exist.'

        if not values['site']:
            errors['site'] = 'Site selection is required.'
        elif not Site.objects.filter(pk=values['site']).exists():
            errors['site'] = 'Selected site does not exist.'

        if not values['in_time']:
            errors['in_time'] = 'In time is required.'
        else:
            try:
                in_time_obj = datetime.strptime(values['in_time'], '%H:%M').time()
            except ValueError:
                errors['in_time'] = 'Invalid time format.'

        if not values['out_time']:
            errors['out_time'] = 'Out time is required.'
        else:
            try:
                out_time_obj = datetime.strptime(values['out_time'], '%H:%M').time()
            except ValueError:
                errors['out_time'] = 'Invalid time format.'

        if not values['day_status']:
            errors['day_status'] = 'Day status is required.'
        elif values['day_status'] not in dict(CompOffEntry.DAY_STATUS_CHOICES):
            errors['day_status'] = 'Invalid day status.'

        if not errors:
            CompOffEntry.objects.create(
                work_date=work_date_obj,
                employee_id=values['employee'],
                site_id=values['site'],
                in_time=in_time_obj,
                out_time=out_time_obj,
                day_status=values['day_status'],
            )
            messages.success(request, 'Comp-Off entry created successfully.')
            return redirect('entry:comp_off_list')

    context = {
        'employees': employees,
        'sites': sites,
        'values': values,
        'errors': errors,
        'day_status_choices': CompOffEntry.DAY_STATUS_CHOICES,
    }
    return render(request, 'entry/comp_entry/create.html', context)


@permission_required('entry.view_compoffentry', raise_exception=True)
def comp_off_list(request):
    per_page = request.GET.get('per_page', '').strip() or '10'
    search_query = request.GET.get('q', '').strip()
    page_number = request.GET.get('page')

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

    comp_off_entries = comp_off_entries.order_by('-work_date', 'employee__staff_name')
    paginator = Paginator(comp_off_entries, per_page_value)
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop('page', None)
    base_querystring = query_params.urlencode()
    page_query_base = f'{base_querystring}&' if base_querystring else ''

    context = {
        'comp_off_entries': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'per_page': str(per_page_value),
        'per_page_value': per_page_value,
        'base_querystring': base_querystring,
        'page_query_base': page_query_base,
        'total_entries': paginator.count,
    }
    return render(request, 'entry/comp_entry/list.html', context)


@permission_required('entry.change_compoffentry', raise_exception=True)
def comp_off_edit(request, pk):
    comp_off_entry = get_object_or_404(CompOffEntry, pk=pk)
    employees = Employee.objects.order_by('staff_name')
    sites = Site.objects.order_by('name')

    values = {
        'work_date': comp_off_entry.work_date.strftime('%Y-%m-%d') if comp_off_entry.work_date else '',
        'site': str(comp_off_entry.site_id) if comp_off_entry.site_id else '',
        'employee': str(comp_off_entry.employee_id) if comp_off_entry.employee_id else '',
        'in_time': comp_off_entry.in_time.strftime('%H:%M') if comp_off_entry.in_time else '',
        'out_time': comp_off_entry.out_time.strftime('%H:%M') if comp_off_entry.out_time else '',
        'day_status': comp_off_entry.day_status or '',
    }
    errors = {}

    if request.method == 'POST':
        values['work_date'] = request.POST.get('work_date', '').strip()
        values['site'] = request.POST.get('site', '').strip()
        values['employee'] = request.POST.get('employee', '').strip()
        values['in_time'] = request.POST.get('in_time', '').strip()
        values['out_time'] = request.POST.get('out_time', '').strip()
        values['day_status'] = request.POST.get('day_status', '').strip()

        work_date_obj = None
        in_time_obj = None
        out_time_obj = None

        if not values['work_date']:
            errors['work_date'] = 'Work date is required.'
        else:
            try:
                work_date_obj = datetime.strptime(values['work_date'], '%Y-%m-%d').date()
            except ValueError:
                errors['work_date'] = 'Invalid date format.'

        if not values['employee']:
            errors['employee'] = 'Employee selection is required.'
        elif not Employee.objects.filter(pk=values['employee']).exists():
            errors['employee'] = 'Selected employee does not exist.'

        if not values['site']:
            errors['site'] = 'Site selection is required.'
        elif not Site.objects.filter(pk=values['site']).exists():
            errors['site'] = 'Selected site does not exist.'

        if not values['in_time']:
            errors['in_time'] = 'In time is required.'
        else:
            try:
                in_time_obj = datetime.strptime(values['in_time'], '%H:%M').time()
            except ValueError:
                errors['in_time'] = 'Invalid time format.'

        if not values['out_time']:
            errors['out_time'] = 'Out time is required.'
        else:
            try:
                out_time_obj = datetime.strptime(values['out_time'], '%H:%M').time()
            except ValueError:
                errors['out_time'] = 'Invalid time format.'

        if not values['day_status']:
            errors['day_status'] = 'Day status is required.'
        elif values['day_status'] not in dict(CompOffEntry.DAY_STATUS_CHOICES):
            errors['day_status'] = 'Invalid day status.'

        if not errors:
            comp_off_entry.work_date = work_date_obj
            comp_off_entry.employee_id = values['employee']
            comp_off_entry.site_id = values['site']
            comp_off_entry.in_time = in_time_obj
            comp_off_entry.out_time = out_time_obj
            comp_off_entry.day_status = values['day_status']
            comp_off_entry.save()
            messages.success(request, 'Comp-Off entry updated successfully.')
            return redirect('entry:comp_off_list')

    context = {
        'comp_off_entry': comp_off_entry,
        'employees': employees,
        'sites': sites,
        'values': values,
        'errors': errors,
        'day_status_choices': CompOffEntry.DAY_STATUS_CHOICES,
    }
    return render(request, 'entry/comp_entry/edit.html', context)


@permission_required('entry.delete_compoffentry', raise_exception=True)
def comp_off_delete(request, pk):
    comp_off_entry = get_object_or_404(CompOffEntry, pk=pk)
    if request.method == 'POST':
        comp_off_entry.delete()
        messages.success(request, 'Comp-Off entry deleted successfully.')
        return redirect('entry:comp_off_list')
    
    context = {
        'comp_off_entry': comp_off_entry,
    }
    return render(request, 'entry/comp_entry/confirm_delete.html', context)


# ------------------------
# ENTRY -> LEAVE
# ------------------------
@permission_required('entry.add_leaveentry', raise_exception=True)
def leave_entry_create(request):
    employees = Employee.objects.order_by('staff_name')
    sites = Site.objects.order_by('name')

    values = {
        'from_date': '',
        'to_date': '',
        'site': '',
        'employee': '',
        'leave_type': '',
        'leave_duration_type': LeaveEntry.DURATION_FULL_DAY,
        'reason': '',
    }
    errors = {}
    selected_employee = None
    calculated_days = 0

    if request.method == 'POST':
        values['from_date'] = request.POST.get('from_date', '').strip()
        values['to_date'] = request.POST.get('to_date', '').strip()
        values['site'] = request.POST.get('site', '').strip()
        values['employee'] = request.POST.get('employee', '').strip()
        values['leave_type'] = request.POST.get('leave_type', '').strip()
        values['leave_duration_type'] = request.POST.get('leave_duration_type', LeaveEntry.DURATION_FULL_DAY).strip()
        values['reason'] = request.POST.get('reason', '').strip()

        from_date_obj = None
        to_date_obj = None

        if not values['from_date']:
            errors['from_date'] = 'From date is required.'
        else:
            try:
                from_date_obj = datetime.strptime(values['from_date'], '%Y-%m-%d').date()
            except ValueError:
                errors['from_date'] = 'Invalid date format.'

        if not values['to_date']:
            errors['to_date'] = 'To date is required.'
        else:
            try:
                to_date_obj = datetime.strptime(values['to_date'], '%Y-%m-%d').date()
            except ValueError:
                errors['to_date'] = 'Invalid date format.'

        if from_date_obj and to_date_obj and to_date_obj < from_date_obj:
            errors['to_date'] = 'To date cannot be before from date.'

        if not values['employee']:
            errors['employee'] = 'Employee selection is required.'
        elif not Employee.objects.filter(pk=values['employee']).exists():
            errors['employee'] = 'Selected employee does not exist.'
        else:
            selected_employee = Employee.objects.get(pk=values['employee'])

        if not values['site']:
            errors['site'] = 'Site selection is required.'
        elif not Site.objects.filter(pk=values['site']).exists():
            errors['site'] = 'Selected site does not exist.'

        if not values['leave_type']:
            errors['leave_type'] = 'Leave type is required.'
        elif values['leave_type'] not in dict(LeaveEntry.LEAVE_TYPE_CHOICES):
            errors['leave_type'] = 'Invalid leave type selected.'

        if not values['reason']:
            errors['reason'] = 'Reason is required.'

        if not values['leave_duration_type']:
            values['leave_duration_type'] = LeaveEntry.DURATION_FULL_DAY

        # Calculate leave days
        if from_date_obj and to_date_obj and not errors:
            days_diff = (to_date_obj - from_date_obj).days + 1
            if values['leave_duration_type'] == LeaveEntry.DURATION_FULL_DAY:
                calculated_days = days_diff
            elif values['leave_duration_type'] in [LeaveEntry.DURATION_FORENOON, LeaveEntry.DURATION_AFTERNOON]:
                if days_diff == 1:
                    calculated_days = 0.50
                else:
                    calculated_days = (days_diff - 1) + 0.50
            else:
                calculated_days = days_diff

        if not errors:
            LeaveEntry.objects.create(
                from_date=from_date_obj,
                to_date=to_date_obj,
                employee_id=values['employee'],
                site_id=values['site'],
                leave_type=values['leave_type'],
                leave_duration_type=values['leave_duration_type'],
                reason=values['reason'],
            )
            messages.success(request, 'Leave entry created successfully.')
            return redirect('entry:leave_entry_list')

    context = {
        'employees': employees,
        'sites': sites,
        'values': values,
        'errors': errors,
        'selected_employee': selected_employee,
        'calculated_days': calculated_days,
        'leave_type_choices': LeaveEntry.LEAVE_TYPE_CHOICES,
        'duration_type_choices': LeaveEntry.DURATION_CHOICES,
    }
    return render(request, 'entry/leave_entry/create.html', context)


@permission_required('entry.view_leaveentry', raise_exception=True)
def leave_entry_list(request):
    per_page = request.GET.get('per_page', '').strip() or '10'
    search_query = request.GET.get('q', '').strip()
    page_number = request.GET.get('page')
    filter_site = request.GET.get('site', '').strip()
    filter_employee = request.GET.get('employee', '').strip()
    filter_from_date = request.GET.get('from_date', '').strip()
    filter_to_date = request.GET.get('to_date', '').strip()

    try:
        per_page_value = max(int(per_page), 1)
    except ValueError:
        per_page_value = 10

    # Fetch employees and sites for filter dropdowns
    employees = Employee.objects.order_by('staff_name')
    sites = Site.objects.order_by('name')

    leave_entries = LeaveEntry.objects.select_related('employee', 'site')
    
    # Apply filters
    if filter_site:
        leave_entries = leave_entries.filter(site_id=filter_site)
    if filter_employee:
        leave_entries = leave_entries.filter(employee_id=filter_employee)
    if filter_from_date:
        try:
            from_date_obj = datetime.strptime(filter_from_date, '%Y-%m-%d').date()
            leave_entries = leave_entries.filter(from_date__gte=from_date_obj)
        except ValueError:
            pass
    if filter_to_date:
        try:
            to_date_obj = datetime.strptime(filter_to_date, '%Y-%m-%d').date()
            leave_entries = leave_entries.filter(to_date__lte=to_date_obj)
        except ValueError:
            pass
    
    if search_query:
        leave_entries = leave_entries.filter(
            Q(employee__staff_name__icontains=search_query)
            | Q(employee__staff_id__icontains=search_query)
            | Q(site__name__icontains=search_query)
            | Q(reason__icontains=search_query)
        )

    leave_entries = leave_entries.order_by('-from_date', 'employee__staff_name')
    paginator = Paginator(leave_entries, per_page_value)
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop('page', None)
    base_querystring = query_params.urlencode()
    page_query_base = f'{base_querystring}&' if base_querystring else ''

    context = {
        'leave_entries': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'per_page': str(per_page_value),
        'per_page_value': per_page_value,
        'base_querystring': base_querystring,
        'page_query_base': page_query_base,
        'total_entries': paginator.count,
        'employees': employees,
        'sites': sites,
        'filter_site': filter_site,
        'filter_employee': filter_employee,
        'filter_from_date': filter_from_date,
        'filter_to_date': filter_to_date,
    }
    return render(request, 'entry/leave_entry/list.html', context)


@permission_required('entry.change_leaveentry', raise_exception=True)
def leave_entry_edit(request, pk):
    leave_entry = get_object_or_404(LeaveEntry, pk=pk)
    employees = Employee.objects.order_by('staff_name')
    sites = Site.objects.order_by('name')

    values = {
        'from_date': leave_entry.from_date.strftime('%Y-%m-%d') if leave_entry.from_date else '',
        'to_date': leave_entry.to_date.strftime('%Y-%m-%d') if leave_entry.to_date else '',
        'site': str(leave_entry.site_id) if leave_entry.site_id else '',
        'employee': str(leave_entry.employee_id) if leave_entry.employee_id else '',
        'leave_type': leave_entry.leave_type or '',
        'leave_duration_type': leave_entry.leave_duration_type or LeaveEntry.DURATION_FULL_DAY,
        'reason': leave_entry.reason or '',
    }
    errors = {}
    selected_employee = None
    calculated_days = leave_entry.leave_days

    if request.method == 'POST':
        values['from_date'] = request.POST.get('from_date', '').strip()
        values['to_date'] = request.POST.get('to_date', '').strip()
        values['site'] = request.POST.get('site', '').strip()
        values['employee'] = request.POST.get('employee', '').strip()
        values['leave_type'] = request.POST.get('leave_type', '').strip()
        values['leave_duration_type'] = request.POST.get('leave_duration_type', LeaveEntry.DURATION_FULL_DAY).strip()
        values['reason'] = request.POST.get('reason', '').strip()

        from_date_obj = None
        to_date_obj = None

        if not values['from_date']:
            errors['from_date'] = 'From date is required.'
        else:
            try:
                from_date_obj = datetime.strptime(values['from_date'], '%Y-%m-%d').date()
            except ValueError:
                errors['from_date'] = 'Invalid date format.'

        if not values['to_date']:
            errors['to_date'] = 'To date is required.'
        else:
            try:
                to_date_obj = datetime.strptime(values['to_date'], '%Y-%m-%d').date()
            except ValueError:
                errors['to_date'] = 'Invalid date format.'

        if from_date_obj and to_date_obj and to_date_obj < from_date_obj:
            errors['to_date'] = 'To date cannot be before from date.'

        if not values['employee']:
            errors['employee'] = 'Employee selection is required.'
        elif not Employee.objects.filter(pk=values['employee']).exists():
            errors['employee'] = 'Selected employee does not exist.'
        else:
            selected_employee = Employee.objects.get(pk=values['employee'])

        if not values['site']:
            errors['site'] = 'Site selection is required.'
        elif not Site.objects.filter(pk=values['site']).exists():
            errors['site'] = 'Selected site does not exist.'

        if not values['leave_type']:
            errors['leave_type'] = 'Leave type is required.'
        elif values['leave_type'] not in dict(LeaveEntry.LEAVE_TYPE_CHOICES):
            errors['leave_type'] = 'Invalid leave type selected.'

        if not values['reason']:
            errors['reason'] = 'Reason is required.'

        if not values['leave_duration_type']:
            values['leave_duration_type'] = LeaveEntry.DURATION_FULL_DAY

        # Calculate leave days
        if from_date_obj and to_date_obj and not errors:
            days_diff = (to_date_obj - from_date_obj).days + 1
            if values['leave_duration_type'] == LeaveEntry.DURATION_FULL_DAY:
                calculated_days = days_diff
            elif values['leave_duration_type'] in [LeaveEntry.DURATION_FORENOON, LeaveEntry.DURATION_AFTERNOON]:
                if days_diff == 1:
                    calculated_days = 0.50
                else:
                    calculated_days = (days_diff - 1) + 0.50
            else:
                calculated_days = days_diff

        if not errors:
            leave_entry.from_date = from_date_obj
            leave_entry.to_date = to_date_obj
            leave_entry.employee_id = values['employee']
            leave_entry.site_id = values['site']
            leave_entry.leave_type = values['leave_type']
            leave_entry.leave_duration_type = values['leave_duration_type']
            leave_entry.reason = values['reason']
            leave_entry.save()  # This will recalculate leave_days
            messages.success(request, 'Leave entry updated successfully.')
            return redirect('entry:leave_entry_list')
    else:
        selected_employee = leave_entry.employee

    context = {
        'leave_entry': leave_entry,
        'employees': employees,
        'sites': sites,
        'values': values,
        'errors': errors,
        'selected_employee': selected_employee,
        'calculated_days': calculated_days,
        'leave_type_choices': LeaveEntry.LEAVE_TYPE_CHOICES,
        'duration_type_choices': LeaveEntry.DURATION_CHOICES,
    }
    return render(request, 'entry/leave_entry/edit.html', context)


@permission_required('entry.delete_leaveentry', raise_exception=True)
def leave_entry_delete(request, pk):
    leave_entry = get_object_or_404(LeaveEntry, pk=pk)
    if request.method == 'POST':
        leave_entry.delete()
        messages.success(request, 'Leave entry deleted successfully.')
        return redirect('entry:leave_entry_list')
    
    context = {
        'leave_entry': leave_entry,
    }
    return render(request, 'entry/leave_entry/confirm_delete.html', context)


@permission_required('entry.view_leaveentry', raise_exception=True)
def leave_entry_print(request):
    return render(request, 'entry/leave_entry/print.html')


# ------------------------
# ENTRY -> MANUAL
# ------------------------
@permission_required('entry.add_manualentry', raise_exception=True)
def manual_entry_create(request):
    return render(request, 'entry/manual_entry/create.html')

@permission_required('entry.view_manualentry', raise_exception=True)
def manual_entry_list(request):
    return render(request, 'entry/manual_entry/list.html')

@permission_required('entry.view_manualentry', raise_exception=True)
def manual_entry_print(request):
    return render(request, 'entry/manual_entry/print.html')


# ------------------------
# ENTRY -> PERMISSION
# ------------------------
@permission_required('entry.add_permissionentry', raise_exception=True)
def permission_entry_create(request):
    employees = Employee.objects.order_by('staff_name')
    sites = Site.objects.order_by('name')

    values = {
        'permission_date': '',
        'site': '',
        'employee': '',
        'permission_start_time': '',
        'permission_end_time': '',
        'reason': '',
    }
    errors = {}
    selected_employee = None

    if request.method == 'POST':
        values['permission_date'] = request.POST.get('permission_date', '').strip()
        values['site'] = request.POST.get('site', '').strip()
        values['employee'] = request.POST.get('employee', '').strip()
        values['permission_start_time'] = request.POST.get('permission_start_time', '').strip()
        values['permission_end_time'] = request.POST.get('permission_end_time', '').strip()
        values['reason'] = request.POST.get('reason', '').strip()

        permission_date_obj = None
        start_time_obj = None
        end_time_obj = None

        if not values['permission_date']:
            errors['permission_date'] = 'Permission date is required.'
        else:
            try:
                permission_date_obj = datetime.strptime(values['permission_date'], '%Y-%m-%d').date()
            except ValueError:
                errors['permission_date'] = 'Invalid date format.'

        if not values['employee']:
            errors['employee'] = 'Employee selection is required.'
        elif not Employee.objects.filter(pk=values['employee']).exists():
            errors['employee'] = 'Selected employee does not exist.'
        else:
            selected_employee = Employee.objects.get(pk=values['employee'])

        if not values['site']:
            errors['site'] = 'Site selection is required.'
        elif not Site.objects.filter(pk=values['site']).exists():
            errors['site'] = 'Selected site does not exist.'

        if values['permission_start_time']:
            try:
                start_time_obj = datetime.strptime(values['permission_start_time'], '%H:%M').time()
            except ValueError:
                errors['permission_start_time'] = 'Invalid time format.'

        if values['permission_end_time']:
            try:
                end_time_obj = datetime.strptime(values['permission_end_time'], '%H:%M').time()
            except ValueError:
                errors['permission_end_time'] = 'Invalid time format.'

        if start_time_obj and end_time_obj:
            start_dt = datetime.combine(permission_date_obj or datetime.now().date(), start_time_obj)
            end_dt = datetime.combine(permission_date_obj or datetime.now().date(), end_time_obj)
            if end_dt <= start_dt:
                end_dt += timedelta(days=1)
            diff = end_dt - start_dt
            per_hr_count = diff.total_seconds() / 3600
        else:
            per_hr_count = 0

        if not errors:
            PermissionEntry.objects.create(
                permission_date=permission_date_obj,
                employee_id=values['employee'],
                site_id=values['site'],
                permission_start_time=start_time_obj,
                permission_end_time=end_time_obj,
                per_hr_count=per_hr_count,
                reason=values['reason'],
            )
            messages.success(request, 'Permission entry created successfully.')
            return redirect('entry:permission_entry_list')

    context = {
        'employees': employees,
        'sites': sites,
        'values': values,
        'errors': errors,
        'selected_employee': selected_employee,
    }
    return render(request, 'entry/permission_entry/create.html', context)


@permission_required('entry.view_permissionentry', raise_exception=True)
def permission_entry_list(request):
    per_page = request.GET.get('per_page', '').strip() or '10'
    search_query = request.GET.get('q', '').strip()
    page_number = request.GET.get('page')
    filter_site = request.GET.get('site', '').strip()
    filter_employee = request.GET.get('employee', '').strip()
    filter_from_date = request.GET.get('from_date', '').strip()
    filter_to_date = request.GET.get('to_date', '').strip()
    filter_status = request.GET.get('status', '').strip()

    try:
        per_page_value = max(int(per_page), 1)
    except ValueError:
        per_page_value = 10

    # Fetch employees and sites for filter dropdowns
    employees = Employee.objects.order_by('staff_name')
    sites = Site.objects.order_by('name')

    permission_entries = PermissionEntry.objects.select_related('employee', 'site')
    
    # Apply filters
    if filter_site:
        permission_entries = permission_entries.filter(site_id=filter_site)
    if filter_employee:
        permission_entries = permission_entries.filter(employee_id=filter_employee)
    if filter_from_date:
        try:
            from_date_obj = datetime.strptime(filter_from_date, '%Y-%m-%d').date()
            permission_entries = permission_entries.filter(permission_date__gte=from_date_obj)
        except ValueError:
            pass
    if filter_to_date:
        try:
            to_date_obj = datetime.strptime(filter_to_date, '%Y-%m-%d').date()
            permission_entries = permission_entries.filter(permission_date__lte=to_date_obj)
        except ValueError:
            pass
    if filter_status:
        permission_entries = permission_entries.filter(status=filter_status)
    
    if search_query:
        permission_entries = permission_entries.filter(
            Q(employee__staff_name__icontains=search_query)
            | Q(employee__staff_id__icontains=search_query)
            | Q(site__name__icontains=search_query)
            | Q(reason__icontains=search_query)
        )

    permission_entries = permission_entries.order_by('-permission_date', 'employee__staff_name')
    paginator = Paginator(permission_entries, per_page_value)
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop('page', None)
    base_querystring = query_params.urlencode()
    page_query_base = f'{base_querystring}&' if base_querystring else ''

    context = {
        'permission_entries': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'per_page': str(per_page_value),
        'per_page_value': per_page_value,
        'base_querystring': base_querystring,
        'page_query_base': page_query_base,
        'total_entries': paginator.count,
        'status_choices': PermissionEntry.STATUS_CHOICES,
        'employees': employees,
        'sites': sites,
        'filter_site': filter_site,
        'filter_employee': filter_employee,
        'filter_from_date': filter_from_date,
        'filter_to_date': filter_to_date,
        'filter_status': filter_status,
    }
    return render(request, 'entry/permission_entry/list.html', context)


@permission_required('entry.change_permissionentry', raise_exception=True)
def permission_entry_edit(request, pk):
    permission_entry = get_object_or_404(PermissionEntry, pk=pk)
    employees = Employee.objects.order_by('staff_name')
    sites = Site.objects.order_by('name')

    values = {
        'permission_date': permission_entry.permission_date.strftime('%Y-%m-%d') if permission_entry.permission_date else '',
        'site': str(permission_entry.site_id) if permission_entry.site_id else '',
        'employee': str(permission_entry.employee_id) if permission_entry.employee_id else '',
        'permission_start_time': permission_entry.permission_start_time.strftime('%H:%M') if permission_entry.permission_start_time else '',
        'permission_end_time': permission_entry.permission_end_time.strftime('%H:%M') if permission_entry.permission_end_time else '',
        'reason': permission_entry.reason or '',
    }
    errors = {}
    selected_employee = None

    if request.method == 'POST':
        values['permission_date'] = request.POST.get('permission_date', '').strip()
        values['site'] = request.POST.get('site', '').strip()
        values['employee'] = request.POST.get('employee', '').strip()
        values['permission_start_time'] = request.POST.get('permission_start_time', '').strip()
        values['permission_end_time'] = request.POST.get('permission_end_time', '').strip()
        values['reason'] = request.POST.get('reason', '').strip()

        permission_date_obj = None
        start_time_obj = None
        end_time_obj = None

        if not values['permission_date']:
            errors['permission_date'] = 'Permission date is required.'
        else:
            try:
                permission_date_obj = datetime.strptime(values['permission_date'], '%Y-%m-%d').date()
            except ValueError:
                errors['permission_date'] = 'Invalid date format.'

        if not values['employee']:
            errors['employee'] = 'Employee selection is required.'
        elif not Employee.objects.filter(pk=values['employee']).exists():
            errors['employee'] = 'Selected employee does not exist.'
        else:
            selected_employee = Employee.objects.get(pk=values['employee'])

        if not values['site']:
            errors['site'] = 'Site selection is required.'
        elif not Site.objects.filter(pk=values['site']).exists():
            errors['site'] = 'Selected site does not exist.'

        if values['permission_start_time']:
            try:
                start_time_obj = datetime.strptime(values['permission_start_time'], '%H:%M').time()
            except ValueError:
                errors['permission_start_time'] = 'Invalid time format.'

        if values['permission_end_time']:
            try:
                end_time_obj = datetime.strptime(values['permission_end_time'], '%H:%M').time()
            except ValueError:
                errors['permission_end_time'] = 'Invalid time format.'

        if start_time_obj and end_time_obj:
            start_dt = datetime.combine(permission_date_obj or datetime.now().date(), start_time_obj)
            end_dt = datetime.combine(permission_date_obj or datetime.now().date(), end_time_obj)
            if end_dt <= start_dt:
                end_dt += timedelta(days=1)
            diff = end_dt - start_dt
            per_hr_count = diff.total_seconds() / 3600
        else:
            per_hr_count = 0

        if not errors:
            permission_entry.permission_date = permission_date_obj
            permission_entry.employee_id = values['employee']
            permission_entry.site_id = values['site']
            permission_entry.permission_start_time = start_time_obj
            permission_entry.permission_end_time = end_time_obj
            permission_entry.per_hr_count = per_hr_count
            permission_entry.reason = values['reason']
            permission_entry.save()
            messages.success(request, 'Permission entry updated successfully.')
            return redirect('entry:permission_entry_list')
    else:
        selected_employee = permission_entry.employee

    context = {
        'permission_entry': permission_entry,
        'employees': employees,
        'sites': sites,
        'values': values,
        'errors': errors,
        'selected_employee': selected_employee,
    }
    return render(request, 'entry/permission_entry/edit.html', context)


@permission_required('entry.delete_permissionentry', raise_exception=True)
def permission_entry_delete(request, pk):
    permission_entry = get_object_or_404(PermissionEntry, pk=pk)
    if request.method == 'POST':
        permission_entry.delete()
        messages.success(request, 'Permission entry deleted successfully.')
        return redirect('entry:permission_entry_list')
    
    context = {
        'permission_entry': permission_entry,
    }
    return render(request, 'entry/permission_entry/confirm_delete.html', context)


@permission_required('entry.view_permissionentry', raise_exception=True)
def permission_entry_print(request):
    return render(request, 'entry/permission_entry/print.html')


# ------------------------
# ENTRY -> SITE
# ------------------------
@permission_required('entry.view_siteentry', raise_exception=True)
def site_entry_list(request):
    per_page = request.GET.get('per_page', '').strip() or '10'
    search_query = request.GET.get('q', '').strip()
    page_number = request.GET.get('page')

    try:
        per_page_value = max(int(per_page), 1)
    except ValueError:
        per_page_value = 10

    site_entries = SiteEntry.objects.all()
    if search_query:
        site_entries = site_entries.filter(
            Q(employee_name__icontains=search_query)
            | Q(from_site__icontains=search_query)
            | Q(to_site__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    site_entries = site_entries.order_by('-transfer_date', 'employee_name')
    paginator = Paginator(site_entries, per_page_value)
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop('page', None)
    base_querystring = query_params.urlencode()
    page_query_base = f'{base_querystring}&' if base_querystring else ''

    context = {
        'site_entries': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'per_page': str(per_page_value),
        'per_page_value': per_page_value,
        'base_querystring': base_querystring,
        'page_query_base': page_query_base,
        'total_entries': paginator.count,
    }
    return render(request, 'entry/site_entry/list.html', context)


@permission_required('entry.add_siteentry', raise_exception=True)
def site_entry_create(request):
    employees = Employee.objects.order_by('staff_name')
    sites = Site.objects.order_by('name')
    
    values = {
        'transfer_date': '',
        'employee_name': '',
        'from_site': '',
        'to_site': '',
        'description': '',
        'transfer_type': '',
    }
    errors = {}

    if request.method == 'POST':
        values['transfer_date'] = request.POST.get('transfer_date', '').strip()
        values['employee_name'] = request.POST.get('employee_name', '').strip()
        values['from_site'] = request.POST.get('from_site', '').strip()
        values['to_site'] = request.POST.get('to_site', '').strip()
        values['description'] = request.POST.get('description', '').strip()
        values['transfer_type'] = request.POST.get('transfer_type', '').strip()

        if not values['transfer_date']:
            errors['transfer_date'] = 'Transfer date is required.'

        if not values['employee_name']:
            errors['employee_name'] = 'Employee name is required.'

        if not values['from_site']:
            errors['from_site'] = 'From site is required.'

        if not values['to_site']:
            errors['to_site'] = 'To site is required.'

        if values['from_site'] == values['to_site']:
            errors['to_site'] = 'To site must be different from from site.'

        if values['transfer_type'] and values['transfer_type'] not in dict(SiteEntry.TRANSFER_TYPE_CHOICES):
            errors['transfer_type'] = 'Invalid transfer type selected.'

        if not errors:
            SiteEntry.objects.create(
                transfer_date=values['transfer_date'],
                employee_name=values['employee_name'],
                from_site=values['from_site'],
                to_site=values['to_site'],
                description=values['description'],
                transfer_type=values['transfer_type'] if values['transfer_type'] else '',
            )
            messages.success(request, 'Site transfer entry created successfully.')
            return redirect('entry:site_entry_list')

    context = {
        'employees': employees,
        'sites': sites,
        'values': values,
        'errors': errors,
        'transfer_type_choices': SiteEntry.TRANSFER_TYPE_CHOICES,
    }
    return render(request, 'entry/site_entry/create.html', context)


@permission_required('entry.change_siteentry', raise_exception=True)
def site_entry_edit(request, pk):
    site_entry = get_object_or_404(SiteEntry, pk=pk)
    employees = Employee.objects.order_by('staff_name')
    sites = Site.objects.order_by('name')
    
    values = {
        'transfer_date': site_entry.transfer_date.strftime('%Y-%m-%d') if site_entry.transfer_date else '',
        'employee_name': site_entry.employee_name,
        'from_site': site_entry.from_site,
        'to_site': site_entry.to_site,
        'description': site_entry.description or '',
        'transfer_type': site_entry.transfer_type or '',
    }
    errors = {}

    if request.method == 'POST':
        values['transfer_date'] = request.POST.get('transfer_date', '').strip()
        values['employee_name'] = request.POST.get('employee_name', '').strip()
        values['from_site'] = request.POST.get('from_site', '').strip()
        values['to_site'] = request.POST.get('to_site', '').strip()
        values['description'] = request.POST.get('description', '').strip()
        values['transfer_type'] = request.POST.get('transfer_type', '').strip()

        if not values['transfer_date']:
            errors['transfer_date'] = 'Transfer date is required.'

        if not values['employee_name']:
            errors['employee_name'] = 'Employee name is required.'

        if not values['from_site']:
            errors['from_site'] = 'From site is required.'

        if not values['to_site']:
            errors['to_site'] = 'To site is required.'

        if values['from_site'] == values['to_site']:
            errors['to_site'] = 'To site must be different from from site.'

        if values['transfer_type'] and values['transfer_type'] not in dict(SiteEntry.TRANSFER_TYPE_CHOICES):
            errors['transfer_type'] = 'Invalid transfer type selected.'

        if not errors:
            site_entry.transfer_date = values['transfer_date']
            site_entry.employee_name = values['employee_name']
            site_entry.from_site = values['from_site']
            site_entry.to_site = values['to_site']
            site_entry.description = values['description']
            site_entry.transfer_type = values['transfer_type'] or None
            site_entry.save()
            messages.success(request, 'Site transfer entry updated successfully.')
            return redirect('entry:site_entry_list')

    context = {
        'site_entry': site_entry,
        'employees': employees,
        'sites': sites,
        'values': values,
        'errors': errors,
        'transfer_type_choices': SiteEntry.TRANSFER_TYPE_CHOICES,
    }
    return render(request, 'entry/site_entry/edit.html', context)


@permission_required('entry.delete_siteentry', raise_exception=True)
def site_entry_delete(request, pk):
    site_entry = get_object_or_404(SiteEntry, pk=pk)
    if request.method == 'POST':
        site_entry.delete()
        messages.success(request, 'Site transfer entry deleted successfully.')
        return redirect('entry:site_entry_list')
    
    context = {
        'site_entry': site_entry,
    }
    return render(request, 'entry/site_entry/confirm_delete.html', context)


# ------------------------
# ENTRY -> TADA
# ------------------------
@permission_required('entry.view_tadaentry', raise_exception=True)
def tada_entry_list(request):
    per_page = request.GET.get('per_page', '').strip() or '10'
    search_query = request.GET.get('q', '').strip()
    page_number = request.GET.get('page')
    filter_site = request.GET.get('site', '').strip()
    filter_employee = request.GET.get('employee', '').strip()
    filter_from_date = request.GET.get('from_date', '').strip()
    filter_to_date = request.GET.get('to_date', '').strip()

    try:
        per_page_value = max(int(per_page), 1)
    except ValueError:
        per_page_value = 10

    # Fetch employees and sites for filter dropdowns
    employees = Employee.objects.order_by('staff_name')
    sites = Site.objects.order_by('name')

    tada_entries = TADAEntry.objects.select_related('employee', 'site').prefetch_related('sub_items')

    # Apply filters
    if filter_site:
        tada_entries = tada_entries.filter(site_id=filter_site)
    if filter_employee:
        tada_entries = tada_entries.filter(employee_id=filter_employee)
    if filter_from_date:
        try:
            from_date_obj = datetime.strptime(filter_from_date, '%Y-%m-%d').date()
            tada_entries = tada_entries.filter(expense_date__gte=from_date_obj)
        except ValueError:
            pass
    if filter_to_date:
        try:
            to_date_obj = datetime.strptime(filter_to_date, '%Y-%m-%d').date()
            tada_entries = tada_entries.filter(expense_date__lte=to_date_obj)
        except ValueError:
            pass

    # Apply search
    if search_query:
        tada_entries = tada_entries.filter(
            Q(entry_no__icontains=search_query)
            | Q(batch_no__icontains=search_query)
            | Q(employee__staff_name__icontains=search_query)
            | Q(employee__staff_id__icontains=search_query)
            | Q(site__name__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(tada_entries, per_page_value)
    page_obj = paginator.get_page(page_number)

    context = {
        'tada_entries': page_obj,
        'employees': employees,
        'sites': sites,
        'per_page': per_page,
        'search_query': search_query,
        'filter_site': filter_site,
        'filter_employee': filter_employee,
        'filter_from_date': filter_from_date,
        'filter_to_date': filter_to_date,
    }
    return render(request, 'entry/tada_entry/list.html', context)


@permission_required('entry.add_tadaentry', raise_exception=True)
def tada_entry_create(request):
    employees = Employee.objects.order_by('staff_name')
    sites = Site.objects.order_by('name')
    expense_types = ExpenseType.objects.filter(is_active=True).order_by('name')
    sub_expense_types = SubExpense.objects.filter(status=SubExpense.STATUS_ACTIVE).select_related('expense_type').order_by('expense_type__name', 'name')

    values = {
        'expense_date': '',
        'batch_no': '',
        'site': '',
        'employee': '',
    }
    errors = {}
    selected_employee = None

    if request.method == 'POST':
        values['expense_date'] = request.POST.get('expense_date', '').strip()
        values['batch_no'] = request.POST.get('batch_no', '').strip()
        values['site'] = request.POST.get('site', '').strip()
        values['employee'] = request.POST.get('employee', '').strip()

        expense_date_obj = None

        if not values['expense_date']:
            errors['expense_date'] = 'Expense date is required.'
        else:
            try:
                expense_date_obj = datetime.strptime(values['expense_date'], '%Y-%m-%d').date()
            except ValueError:
                errors['expense_date'] = 'Invalid date format.'

        if not values['employee']:
            errors['employee'] = 'Employee selection is required.'
        elif not Employee.objects.filter(pk=values['employee']).exists():
            errors['employee'] = 'Selected employee does not exist.'
        else:
            selected_employee = Employee.objects.get(pk=values['employee'])

        if not values['site']:
            errors['site'] = 'Site selection is required.'
        elif not Site.objects.filter(pk=values['site']).exists():
            errors['site'] = 'Selected site does not exist.'

        # Process sub items
        sub_items_data = []
        sub_item_errors = []
        restored_sub_items = []  # For restoring items if validation fails
        
        # Get sub items from form (assuming they're sent as arrays)
        expense_types_post = request.POST.getlist('sub_items_expense_type[]')
        sub_expense_types_post = request.POST.getlist('sub_items_sub_expense_type[]')
        from_locations_post = request.POST.getlist('sub_items_from_location[]')
        to_locations_post = request.POST.getlist('sub_items_to_location[]')
        start_meters_post = request.POST.getlist('sub_items_start_meter[]')
        end_meters_post = request.POST.getlist('sub_items_end_meter[]')
        total_kilometers_post = request.POST.getlist('sub_items_total_kilometer[]')
        amounts_post = request.POST.getlist('sub_items_amount[]')
        descriptions_post = request.POST.getlist('sub_items_description[]')

        if not expense_types_post:
            errors['sub_items'] = 'At least one expense item is required.'

        # Collect sub items data (for both validation and restoration)
        for i in range(len(expense_types_post)):
            if not expense_types_post[i] or not amounts_post[i]:
                continue
            
            try:
                amount = float(amounts_post[i])
                if amount <= 0:
                    sub_item_errors.append(f'Item {i+1}: Amount must be greater than 0.')
                    continue
            except ValueError:
                sub_item_errors.append(f'Item {i+1}: Invalid amount format.')
                continue

            # Convert numeric fields to Decimal
            start_meter = None
            if i < len(start_meters_post) and start_meters_post[i]:
                try:
                    start_meter = Decimal(str(start_meters_post[i]))
                except (ValueError, InvalidOperation):
                    start_meter = None
            
            end_meter = None
            if i < len(end_meters_post) and end_meters_post[i]:
                try:
                    end_meter = Decimal(str(end_meters_post[i]))
                except (ValueError, InvalidOperation):
                    end_meter = None
            
            total_kilometer = None
            if i < len(total_kilometers_post) and total_kilometers_post[i]:
                try:
                    total_kilometer = Decimal(str(total_kilometers_post[i]))
                except (ValueError, InvalidOperation):
                    total_kilometer = None
            
            item_data = {
                'expense_type_id': expense_types_post[i],
                'sub_expense_type_id': sub_expense_types_post[i] if i < len(sub_expense_types_post) and sub_expense_types_post[i] else None,
                'from_location': from_locations_post[i] if i < len(from_locations_post) else '',
                'to_location': to_locations_post[i] if i < len(to_locations_post) else '',
                'start_meter': start_meter,
                'end_meter': end_meter,
                'total_kilometer': total_kilometer,
                'amount': Decimal(str(amount)),
                'description': descriptions_post[i] if i < len(descriptions_post) else '',
            }
            
            # Get expense type name for display
            try:
                expense_type_obj = ExpenseType.objects.get(pk=expense_types_post[i])
                item_data['expense_type_name'] = expense_type_obj.name
            except ExpenseType.DoesNotExist:
                item_data['expense_type_name'] = 'Unknown'
            
            # Get sub expense type name if exists
            if item_data['sub_expense_type_id']:
                try:
                    sub_expense_type_obj = SubExpense.objects.get(pk=item_data['sub_expense_type_id'])
                    item_data['sub_expense_type_name'] = sub_expense_type_obj.name
                except SubExpense.DoesNotExist:
                    item_data['sub_expense_type_name'] = ''
            else:
                item_data['sub_expense_type_name'] = ''
            
            sub_items_data.append(item_data)
            restored_sub_items.append(item_data)

        if sub_item_errors:
            errors['sub_items'] = '; '.join(sub_item_errors)

        if not errors and sub_items_data:
                # Create TADA entry (without calculating total_amount yet)
                tada_entry = TADAEntry.objects.create(
                    expense_date=expense_date_obj,
                    batch_no=values['batch_no'],
                    employee_id=values['employee'],
                    site_id=values['site'],
                    total_amount=0,  # Set to 0 initially
                )

                # Create sub items
                total_amount = Decimal('0')
                for item_data in sub_items_data:
                    TADAEntrySubItem.objects.create(
                        tada_entry=tada_entry,
                        expense_type_id=item_data['expense_type_id'],
                        sub_expense_type_id=item_data['sub_expense_type_id'],
                        from_location=item_data['from_location'],
                        to_location=item_data['to_location'],
                        start_meter=item_data['start_meter'],
                        end_meter=item_data['end_meter'],
                        total_kilometer=item_data['total_kilometer'],
                        amount=item_data['amount'],
                        description=item_data['description'],
                    )
                    total_amount += item_data['amount']

                # Update total amount after all sub items are created
                tada_entry.total_amount = total_amount
                tada_entry.save()

                messages.success(request, 'TADA entry created successfully.')
                return redirect('entry:tada_entry_list')

    # Serialize restored sub items for JavaScript
    restored_sub_items_json = json.dumps(restored_sub_items if request.method == 'POST' and errors else [])
    
    context = {
        'employees': employees,
        'sites': sites,
        'expense_types': expense_types,
        'sub_expense_types': sub_expense_types,
        'values': values,
        'errors': errors,
        'selected_employee': selected_employee,
        'restored_sub_items_json': restored_sub_items_json,
    }
    return render(request, 'entry/tada_entry/create.html', context)


@permission_required('entry.change_tadaentry', raise_exception=True)
def tada_entry_edit(request, pk):
    tada_entry = get_object_or_404(TADAEntry.objects.prefetch_related('sub_items'), pk=pk)
    employees = Employee.objects.order_by('staff_name')
    sites = Site.objects.order_by('name')
    expense_types = ExpenseType.objects.filter(is_active=True).order_by('name')
    sub_expense_types = SubExpense.objects.filter(status=SubExpense.STATUS_ACTIVE).select_related('expense_type').order_by('expense_type__name', 'name')

    values = {
        'expense_date': tada_entry.expense_date.strftime('%Y-%m-%d') if tada_entry.expense_date else '',
        'batch_no': tada_entry.batch_no,
        'site': str(tada_entry.site_id) if tada_entry.site_id else '',
        'employee': str(tada_entry.employee_id) if tada_entry.employee_id else '',
    }
    errors = {}
    selected_employee = tada_entry.employee
    
    # Initialize POST variables (will be populated in POST request)
    expense_types_post = []
    sub_expense_types_post = []
    from_locations_post = []
    to_locations_post = []
    start_meters_post = []
    end_meters_post = []
    total_kilometers_post = []
    amounts_post = []
    descriptions_post = []

    if request.method == 'POST':
        values['expense_date'] = request.POST.get('expense_date', '').strip()
        values['batch_no'] = request.POST.get('batch_no', '').strip()
        values['site'] = request.POST.get('site', '').strip()
        values['employee'] = request.POST.get('employee', '').strip()

        expense_date_obj = None

        if not values['expense_date']:
            errors['expense_date'] = 'Expense date is required.'
        else:
            try:
                expense_date_obj = datetime.strptime(values['expense_date'], '%Y-%m-%d').date()
            except ValueError:
                errors['expense_date'] = 'Invalid date format.'

        if not values['employee']:
            errors['employee'] = 'Employee selection is required.'
        elif not Employee.objects.filter(pk=values['employee']).exists():
            errors['employee'] = 'Selected employee does not exist.'
        else:
            selected_employee = Employee.objects.get(pk=values['employee'])

        if not values['site']:
            errors['site'] = 'Site selection is required.'
        elif not Site.objects.filter(pk=values['site']).exists():
            errors['site'] = 'Selected site does not exist.'

        # Process sub items
        sub_items_data = []
        sub_item_errors = []
        
        expense_types_post = request.POST.getlist('sub_items_expense_type[]')
        sub_expense_types_post = request.POST.getlist('sub_items_sub_expense_type[]')
        from_locations_post = request.POST.getlist('sub_items_from_location[]')
        to_locations_post = request.POST.getlist('sub_items_to_location[]')
        start_meters_post = request.POST.getlist('sub_items_start_meter[]')
        end_meters_post = request.POST.getlist('sub_items_end_meter[]')
        total_kilometers_post = request.POST.getlist('sub_items_total_kilometer[]')
        amounts_post = request.POST.getlist('sub_items_amount[]')
        descriptions_post = request.POST.getlist('sub_items_description[]')

        if not expense_types_post:
            errors['sub_items'] = 'At least one expense item is required.'

        if not errors:
            for i in range(len(expense_types_post)):
                if not expense_types_post[i] or not amounts_post[i]:
                    continue
                
                try:
                    amount = Decimal(str(amounts_post[i]))
                    if amount <= 0:
                        sub_item_errors.append(f'Item {i+1}: Amount must be greater than 0.')
                        continue
                except (ValueError, InvalidOperation):
                    sub_item_errors.append(f'Item {i+1}: Invalid amount format.')
                    continue

                # Convert numeric fields to Decimal
                start_meter = None
                if i < len(start_meters_post) and start_meters_post[i]:
                    try:
                        start_meter = Decimal(str(start_meters_post[i]))
                    except (ValueError, InvalidOperation):
                        start_meter = None
                
                end_meter = None
                if i < len(end_meters_post) and end_meters_post[i]:
                    try:
                        end_meter = Decimal(str(end_meters_post[i]))
                    except (ValueError, InvalidOperation):
                        end_meter = None
                
                total_kilometer = None
                if i < len(total_kilometers_post) and total_kilometers_post[i]:
                    try:
                        total_kilometer = Decimal(str(total_kilometers_post[i]))
                    except (ValueError, InvalidOperation):
                        total_kilometer = None

                sub_items_data.append({
                    'expense_type_id': expense_types_post[i],
                    'sub_expense_type_id': sub_expense_types_post[i] if i < len(sub_expense_types_post) and sub_expense_types_post[i] else None,
                    'from_location': from_locations_post[i] if i < len(from_locations_post) else '',
                    'to_location': to_locations_post[i] if i < len(to_locations_post) else '',
                    'start_meter': start_meter,
                    'end_meter': end_meter,
                    'total_kilometer': total_kilometer,
                    'amount': amount,
                    'description': descriptions_post[i] if i < len(descriptions_post) else '',
                })

            if sub_item_errors:
                errors['sub_items'] = '; '.join(sub_item_errors)

            if not errors and sub_items_data:
                # Update TADA entry
                tada_entry.expense_date = expense_date_obj
                tada_entry.batch_no = values['batch_no']
                tada_entry.employee_id = values['employee']
                tada_entry.site_id = values['site']
                tada_entry.save()

                # Delete existing sub items and create new ones
                tada_entry.sub_items.all().delete()
                total_amount = Decimal('0')
                for item_data in sub_items_data:
                    TADAEntrySubItem.objects.create(
                        tada_entry=tada_entry,
                        expense_type_id=item_data['expense_type_id'],
                        sub_expense_type_id=item_data['sub_expense_type_id'],
                        from_location=item_data['from_location'],
                        to_location=item_data['to_location'],
                        start_meter=item_data['start_meter'],
                        end_meter=item_data['end_meter'],
                        total_kilometer=item_data['total_kilometer'],
                        amount=item_data['amount'],
                        description=item_data['description'],
                    )
                    total_amount += item_data['amount']

                # Update total amount after all sub items are created
                tada_entry.total_amount = total_amount
                tada_entry.save()

                messages.success(request, 'TADA entry updated successfully.')
                return redirect('entry:tada_entry_list')

    # Prepare existing sub_items for template (for initial load)
    existing_sub_items = []
    if tada_entry and tada_entry.pk:
        for sub_item in tada_entry.sub_items.all():
            existing_sub_items.append({
                'expense_type_id': str(sub_item.expense_type_id),
                'expense_type_name': sub_item.expense_type.name if sub_item.expense_type else '',
                'sub_expense_type_id': str(sub_item.sub_expense_type_id) if sub_item.sub_expense_type_id else '',
                'sub_expense_type_name': sub_item.sub_expense_type.name if sub_item.sub_expense_type else '',
                'from_location': sub_item.from_location or '',
                'to_location': sub_item.to_location or '',
                'start_meter': str(sub_item.start_meter) if sub_item.start_meter else '',
                'end_meter': str(sub_item.end_meter) if sub_item.end_meter else '',
                'total_kilometer': str(sub_item.total_kilometer) if sub_item.total_kilometer else '',
                'amount': str(sub_item.amount),
                'description': sub_item.description or '',
            })
    
    # Serialize sub items for JavaScript (existing items or restored items on validation failure)
    restored_sub_items = []
    if request.method == 'POST' and errors:
        # On validation failure, restore from POST data
        for i in range(len(expense_types_post)):
            if not expense_types_post[i] or not amounts_post[i]:
                continue
            try:
                expense_type = ExpenseType.objects.get(pk=expense_types_post[i])
                sub_expense_type = None
                if i < len(sub_expense_types_post) and sub_expense_types_post[i]:
                    try:
                        sub_expense_type = SubExpense.objects.get(pk=sub_expense_types_post[i])
                    except SubExpense.DoesNotExist:
                        pass
                
                restored_sub_items.append({
                    'expense_type_id': expense_types_post[i],
                    'expense_type_name': expense_type.name,
                    'sub_expense_type_id': sub_expense_types_post[i] if i < len(sub_expense_types_post) and sub_expense_types_post[i] else '',
                    'sub_expense_type_name': sub_expense_type.name if sub_expense_type else '',
                    'from_location': from_locations_post[i] if i < len(from_locations_post) else '',
                    'to_location': to_locations_post[i] if i < len(to_locations_post) else '',
                    'start_meter': start_meters_post[i] if i < len(start_meters_post) and start_meters_post[i] else '',
                    'end_meter': end_meters_post[i] if i < len(end_meters_post) and end_meters_post[i] else '',
                    'total_kilometer': total_kilometers_post[i] if i < len(total_kilometers_post) and total_kilometers_post[i] else '',
                    'amount': amounts_post[i],
                    'description': descriptions_post[i] if i < len(descriptions_post) else '',
                })
            except ExpenseType.DoesNotExist:
                continue
    
    # Use restored items if validation failed, otherwise use existing items
    sub_items_json = json.dumps(restored_sub_items if restored_sub_items else existing_sub_items)
    
    context = {
        'tada_entry': tada_entry,
        'employees': employees,
        'sites': sites,
        'expense_types': expense_types,
        'sub_expense_types': sub_expense_types,
        'values': values,
        'errors': errors,
        'selected_employee': selected_employee,
        'restored_sub_items_json': sub_items_json,
    }
    return render(request, 'entry/tada_entry/edit.html', context)


@permission_required('entry.delete_tadaentry', raise_exception=True)
def tada_entry_delete(request, pk):
    tada_entry = get_object_or_404(TADAEntry, pk=pk)
    if request.method == 'POST':
        tada_entry.delete()
        messages.success(request, 'TADA entry deleted successfully.')
        return redirect('entry:tada_entry_list')
    
    context = {
        'tada_entry': tada_entry,
    }
    return render(request, 'entry/tada_entry/confirm_delete.html', context)


# ------------------------
# ENTRY -> TRAVEL
# ------------------------
@permission_required('entry.add_travelentry', raise_exception=True)
def travel_entry_create(request):
    return render(request, 'entry/travel_entry/create.html')

@permission_required('entry.view_travelentry', raise_exception=True)
def travel_entry_list(request):
    return render(request, 'entry/travel_entry/list.html')
