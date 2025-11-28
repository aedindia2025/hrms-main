 # entry/views.py
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Q

from master.models import Employee, Site
from .models import CompOffEntry, SiteEntry

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
    return render(request, 'content/entry/comp_entry/create.html', context)


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
    return render(request, 'content/entry/comp_entry/list.html', context)


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
    return render(request, 'content/entry/comp_entry/edit.html', context)


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
    return render(request, 'content/entry/comp_entry/confirm_delete.html', context)


# ------------------------
# ENTRY -> LEAVE
# ------------------------
@permission_required('entry.add_leaveentry', raise_exception=True)
def leave_entry_create(request):
    return render(request, 'content/entry/leave_entry/create.html')

@permission_required('entry.view_leaveentry', raise_exception=True)
def leave_entry_list(request):
    return render(request, 'content/entry/leave_entry/list.html')

@permission_required('entry.view_leaveentry', raise_exception=True)
def leave_entry_print(request):
    return render(request, 'content/entry/leave_entry/print.html')


# ------------------------
# ENTRY -> MANUAL
# ------------------------
@permission_required('entry.add_manualentry', raise_exception=True)
def manual_entry_create(request):
    return render(request, 'content/entry/manual_entry/create.html')

@permission_required('entry.view_manualentry', raise_exception=True)
def manual_entry_list(request):
    return render(request, 'content/entry/manual_entry/list.html')

@permission_required('entry.view_manualentry', raise_exception=True)
def manual_entry_print(request):
    return render(request, 'content/entry/manual_entry/print.html')


# ------------------------
# ENTRY -> PERMISSION
# ------------------------
@permission_required('entry.add_permissionentry', raise_exception=True)
def permission_entry_create(request):
    return render(request, 'content/entry/permission_entry/create.html')

@permission_required('entry.view_permissionentry', raise_exception=True)
def permission_entry_list(request):
    return render(request, 'content/entry/permission_entry/list.html')

@permission_required('entry.view_permissionentry', raise_exception=True)
def permission_entry_print(request):
    return render(request, 'content/entry/permission_entry/print.html')


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
    return render(request, 'content/entry/site_entry/list.html', context)


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
                transfer_type=values['transfer_type'] or None,
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
    return render(request, 'content/entry/site_entry/create.html', context)


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
    return render(request, 'content/entry/site_entry/edit.html', context)


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
    return render(request, 'content/entry/site_entry/confirm_delete.html', context)


# ------------------------
# ENTRY -> TADA
# ------------------------
@permission_required('entry.add_tadaentry', raise_exception=True)
def tada_entry_create(request):
    return render(request, 'content/entry/tada_entry/create.html')

@permission_required('entry.view_tadaentry', raise_exception=True)
def tada_entry_list(request):
    return render(request, 'content/entry/tada_entry/list.html')


# ------------------------
# ENTRY -> TRAVEL
# ------------------------
@permission_required('entry.add_travelentry', raise_exception=True)
def travel_entry_create(request):
    return render(request, 'content/entry/travel_entry/create.html')

@permission_required('entry.view_travelentry', raise_exception=True)
def travel_entry_list(request):
    return render(request, 'content/entry/travel_entry/list.html')
