# entry/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# ------------------------
# ENTRY -> COMP OFF
# ------------------------
@login_required
def comp_off_create(request):
    return render(request, 'content/entry/comp_entry/create.html')

@login_required
def comp_off_list(request):
    return render(request, 'content/entry/comp_entry/list.html')


# ------------------------
# ENTRY -> LEAVE
# ------------------------
@login_required
def leave_entry_create(request):
    return render(request, 'content/entry/leave_entry/create.html')

@login_required
def leave_entry_list(request):
    return render(request, 'content/entry/leave_entry/list.html')

@login_required
def leave_entry_print(request):
    return render(request, 'content/entry/leave_entry/print.html')


# ------------------------
# ENTRY -> MANUAL
# ------------------------
@login_required
def manual_entry_create(request):
    return render(request, 'content/entry/manual_entry/create.html')

@login_required
def manual_entry_list(request):
    return render(request, 'content/entry/manual_entry/list.html')

@login_required
def manual_entry_print(request):
    return render(request, 'content/entry/manual_entry/print.html')


# ------------------------
# ENTRY -> PERMISSION
# ------------------------
@login_required
def permission_entry_create(request):
    return render(request, 'content/entry/permission_entry/create.html')

@login_required
def permission_entry_list(request):
    return render(request, 'content/entry/permission_entry/list.html')

@login_required
def permission_entry_print(request):
    return render(request, 'content/entry/permission_entry/print.html')


# ------------------------
# ENTRY -> SITE
# ------------------------
@login_required
def site_entry_create(request):
    return render(request, 'content/entry/site_entry/create.html')

@login_required
def site_entry_edit(request):
    return render(request, 'content/entry/site_entry/edit.html')

@login_required
def site_entry_list(request):
    return render(request, 'content/entry/site_entry/list.html')


# ------------------------
# ENTRY -> TADA
# ------------------------
@login_required
def tada_entry_create(request):
    return render(request, 'content/entry/tada_entry/create.html')

@login_required
def tada_entry_list(request):
    return render(request, 'content/entry/tada_entry/list.html')


# ------------------------
# ENTRY -> TRAVEL
# ------------------------
@login_required
def travel_entry_create(request):
    return render(request, 'content/entry/travel_entry/create.html')

@login_required
def travel_entry_list(request):
    return render(request, 'content/entry/travel_entry/list.html')
