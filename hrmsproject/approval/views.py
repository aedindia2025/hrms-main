# approval/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# ==================== HR Approval ====================
@login_required
def hr_comp_off_approval(request):
    """Approval -> HR Comp-Off Approval list."""
    return render(request, 'content/approval/hr_approval/list.html')


# ==================== Daily Attendance ====================
@login_required
def daily_attendance_print(request):
    """Approval -> Daily Attendance -> Print view."""
    return render(request, 'content/approval/dailyAttendance_approval/print.html')


# ==================== Leave ====================
@login_required
def leave_approval_list(request):
    """Approval -> Leave Approval list."""
    return render(request, 'content/approval/leave_approval/list.html')


# ==================== Permission ====================
@login_required
def permission_approval_list(request):
    """Approval -> Permission Approval list."""
    return render(request, 'content/approval/permission_approval/list.html')


# ==================== TADA ====================
@login_required
def tada_approval_list(request):
    """Approval -> TADA Approval list."""
    return render(request, 'content/approval/tada_approval/list.html')


@login_required
def tada_head_approval_list(request):
    """Approval -> TADA Head Approval list."""
    return render(request, 'content/approval/tadaHead_approval/list.html')


@login_required
def tada_hr_approval_list(request):
    """Approval -> TADA HR Approval list."""
    return render(request, 'content/approval/tadaHr_approval/list.html')


@login_required
def tada_hr_print(request):
    """Approval -> TADA HR Print page."""
    return render(request, 'content/approval/tadaHr_approval/print.html')


# ==================== Travel HR ====================
@login_required
def travel_hr_approval_list(request):
    """Approval -> Travel HR Approval list."""
    return render(request, 'content/approval/travelHr_approval/list.html')
