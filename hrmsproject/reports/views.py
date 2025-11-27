# reports/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# ==================== Reports ====================
@login_required
def daily_attendance_report(request):
    """Reports -> Daily Attendance report."""
    return render(request, 'content/reports/daily_report/list.html')


@login_required
def attendance_snapshot_view(request):
    """Reports -> Attendance Snapshot view."""
    return render(request, 'content/reports/attendance_report/view.html')


@login_required
def attendance_report_list(request):
    """Reports -> Attendance Report list."""
    return render(request, 'content/reports/attendance_report/list.html')


@login_required
def attendance_report_view(request):
    """Reports -> Attendance Report view."""
    return render(request, 'content/reports/attendance_report/view.html')


@login_required
def monthly_report_list(request):
    """Reports -> Monthly Report list."""
    return render(request, 'content/reports/monthly_report/list.html')


@login_required
def tada_report_list(request):
    """Reports -> TADA Report list."""
    return render(request, 'content/reports/tada_report/list.html')
