from datetime import datetime, timedelta

from django.db import models

from master.models import Employee, Site


class CompOffEntry(models.Model):
    DAY_STATUS_FULL = 'full_day'
    DAY_STATUS_HALF = 'half_day'
    DAY_STATUS_OVERTIME = 'overtime'
    DAY_STATUS_CHOICES = [
        (DAY_STATUS_FULL, 'Full Day'),
        (DAY_STATUS_HALF, 'Half Day'),
        (DAY_STATUS_OVERTIME, 'Overtime'),
    ]

    APPROVAL_PENDING = 'pending'
    APPROVAL_APPROVED = 'approved'
    APPROVAL_REJECTED = 'rejected'
    APPROVAL_CHOICES = [
        (APPROVAL_PENDING, 'Pending'),
        (APPROVAL_APPROVED, 'Approved'),
        (APPROVAL_REJECTED, 'Rejected'),
    ]

    work_date = models.DateField()
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='comp_off_entries',
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        related_name='comp_off_entries',
    )
    in_time = models.TimeField()
    out_time = models.TimeField()
    worked_duration = models.DurationField(
        null=True,
        blank=True,
        help_text='Stores total worked duration for the day.',
    )
    day_status = models.CharField(
        max_length=20,
        choices=DAY_STATUS_CHOICES,
    )
    head_approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_CHOICES,
        default=APPROVAL_PENDING,
    )
    head_approval_by = models.CharField(max_length=255, blank=True)
    head_approval_note = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-work_date', 'employee__staff_name']
        verbose_name = 'Comp-Off Entry'
        verbose_name_plural = 'Comp-Off Entries'

    def __str__(self):
        return f'{self.employee} - {self.work_date}'

    def save(self, *args, **kwargs):
        if self.in_time and self.out_time:
            in_dt = datetime.combine(self.work_date, self.in_time)
            out_dt = datetime.combine(self.work_date, self.out_time)
            if out_dt <= in_dt:
                out_dt += timedelta(days=1)
            self.worked_duration = out_dt - in_dt
        super().save(*args, **kwargs)

    @property
    def worked_hours_display(self) -> str:
        if not self.worked_duration:
            return ''
        total_minutes = int(self.worked_duration.total_seconds() // 60)
        hours, minutes = divmod(total_minutes, 60)
        parts = []
        if hours:
            parts.append(f'{hours} hr{"s" if hours != 1 else ""}')
        if minutes:
            parts.append(f'{minutes} min{"s" if minutes != 1 else ""}')
        return ' '.join(parts) or '0 mins'

    @property
    def head_approval_badge_class(self) -> str:
        mapping = {
            self.APPROVAL_APPROVED: 'text-success bg-success-subtle border border-success',
            self.APPROVAL_REJECTED: 'text-danger bg-danger-subtle border border-danger',
            self.APPROVAL_PENDING: 'text-info bg-info-subtle border border-info',
        }
        return mapping.get(self.head_approval_status, 'text-secondary bg-secondary-subtle border border-secondary')





class SiteEntry(models.Model):
    TRANSFER_TYPE_MONTH = 'Month'
    TRANSFER_TYPE_WEEK = 'Week'
    TRANSFER_TYPE_CHOICES = [
        (TRANSFER_TYPE_MONTH, 'Month'),
        (TRANSFER_TYPE_WEEK, 'Week'),
    ]

    transfer_date = models.DateField()
    employee_name = models.CharField(max_length=255)
    from_site = models.CharField(max_length=255)
    to_site = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    transfer_type = models.CharField(
        max_length=10,
        choices=TRANSFER_TYPE_CHOICES,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-transfer_date', 'employee_name']
        verbose_name = 'Site Transfer Entry'
        verbose_name_plural = 'Site Transfer Entries'

    def __str__(self):
        return f'{self.employee_name} - {self.transfer_date}'


class PermissionEntry(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_CANCELLED, 'Cancel'),
    ]

    entry_date = models.DateField(auto_now_add=True)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='permission_entries',
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        related_name='permission_entries',
    )
    permission_date = models.DateField()
    permission_start_time = models.TimeField(null=True, blank=True)
    permission_end_time = models.TimeField(null=True, blank=True)
    per_hr_count = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        help_text='Permission hours counted (e.g. 1.50 = 1 hour 30 minutes)'
    )
    reason = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    is_printed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-permission_date', 'employee__staff_name']
        verbose_name = 'Permission Entry'
        verbose_name_plural = 'Permission Entries'

    def __str__(self):
        return f'{self.employee} - {self.permission_date} ({self.status})'

    @property
    def permission_timings_display(self) -> str:
        if self.permission_start_time and self.permission_end_time:
            return f"{self.permission_start_time.strftime('%H:%M')} - {self.permission_end_time.strftime('%H:%M')}"
        return ''


class LeaveEntry(models.Model):
    LEAVE_TYPE_COMPENSATORY = 'compensatory-leave'
    LEAVE_TYPE_EARNED = 'earned-leave'
    LEAVE_TYPE_LOP = 'LOP'
    LEAVE_TYPE_SICK = 'Sick-leave'
    LEAVE_TYPE_CASUAL = 'casual-leave'
    LEAVE_TYPE_CHOICES = [
        (LEAVE_TYPE_COMPENSATORY, 'Compensatory Leave/Off'),
        (LEAVE_TYPE_EARNED, 'Earned Leave'),
        (LEAVE_TYPE_LOP, 'Loss of Pay'),
        (LEAVE_TYPE_SICK, 'Sick Leave'),
        (LEAVE_TYPE_CASUAL, 'Casual Leave'),
    ]

    DURATION_FULL_DAY = 'full_day'
    DURATION_FORENOON = 'forenoon'
    DURATION_AFTERNOON = 'afternoon'
    DURATION_CHOICES = [
        (DURATION_FULL_DAY, 'Full day'),
        (DURATION_FORENOON, 'Forenoon'),
        (DURATION_AFTERNOON, 'Afternoon'),
    ]

    APPROVAL_PENDING = 'pending'
    APPROVAL_STAFF_APPROVED = 'staff_approved'
    APPROVAL_HR_APPROVED = 'hr_approved'
    APPROVAL_REJECTED = 'rejected'
    APPROVAL_CHOICES = [
        (APPROVAL_PENDING, 'Pending'),
        (APPROVAL_STAFF_APPROVED, 'Staff Approved'),
        (APPROVAL_HR_APPROVED, 'HR Approved'),
        (APPROVAL_REJECTED, 'Rejected'),
    ]

    entry_date = models.DateField(auto_now_add=True)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='leave_entries',
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        related_name='leave_entries',
    )
    from_date = models.DateField()
    to_date = models.DateField()
    leave_days = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text='Number of leave days (e.g. 1.00 for full day, 0.50 for half day)'
    )
    leave_type = models.CharField(
        max_length=50,
        choices=LEAVE_TYPE_CHOICES,
    )
    leave_duration_type = models.CharField(
        max_length=20,
        choices=DURATION_CHOICES,
        default=DURATION_FULL_DAY,
    )
    reason = models.TextField()
    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_CHOICES,
        default=APPROVAL_PENDING,
    )
    approved_by = models.CharField(max_length=255, blank=True)
    approval_note = models.CharField(max_length=255, blank=True)
    is_printed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-from_date', 'employee__staff_name']
        verbose_name = 'Leave Entry'
        verbose_name_plural = 'Leave Entries'

    def __str__(self):
        return f'{self.employee} - {self.from_date} to {self.to_date} ({self.get_leave_type_display()})'

    def save(self, *args, **kwargs):
        # Calculate leave days based on from_date, to_date, and duration_type
        if self.from_date and self.to_date:
            if self.to_date < self.from_date:
                raise ValueError("To date cannot be before from date")
            
            days_diff = (self.to_date - self.from_date).days + 1
            
            # Adjust based on duration type
            if self.leave_duration_type == self.DURATION_FULL_DAY:
                self.leave_days = days_diff
            elif self.leave_duration_type in [self.DURATION_FORENOON, self.DURATION_AFTERNOON]:
                # Half day calculation
                if days_diff == 1:
                    self.leave_days = 0.50
                else:
                    # Multiple days: full days + half day
                    self.leave_days = (days_diff - 1) + 0.50
            else:
                self.leave_days = days_diff
        super().save(*args, **kwargs)

    @property
    def leave_dates_display(self) -> str:
        """Returns formatted leave dates range"""
        if self.from_date == self.to_date:
            return self.from_date.strftime('%d-%m-%Y')
        return f"{self.from_date.strftime('%d-%m-%Y')} / {self.to_date.strftime('%d-%m-%Y')}"

    @property
    def approval_badge_class(self) -> str:
        """Returns CSS classes for approval status badge"""
        mapping = {
            self.APPROVAL_HR_APPROVED: 'background-color:#d4edda; color:#155724;',
            self.APPROVAL_STAFF_APPROVED: 'background-color:#fff3cd; color:#856404;',
            self.APPROVAL_REJECTED: 'background-color:#f8d7da; color:#721c24;',
            self.APPROVAL_PENDING: 'background-color:#d1ecf1; color:#0c5460;',
        }
        return mapping.get(self.approval_status, 'background-color:#e2e3e5; color:#383d41;')

    @property
    def approval_icon_color(self) -> str:
        """Returns icon color for approval status"""
        mapping = {
            self.APPROVAL_HR_APPROVED: '#28a745',
            self.APPROVAL_STAFF_APPROVED: '#ffc107',
            self.APPROVAL_REJECTED: '#dc3545',
            self.APPROVAL_PENDING: '#17a2b8',
        }
        return mapping.get(self.approval_status, '#6c757d')