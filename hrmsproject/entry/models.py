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
