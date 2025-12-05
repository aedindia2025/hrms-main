from datetime import datetime, timedelta

from django.db import models
from django.core.validators import MinValueValidator

from master.models import Employee, Site, ExpenseType, SubExpense


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
        blank=True,
        null=True
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
    
    def get_approver_name(self):
        """Get the name of the person who approved/rejected this entry."""
        try:
            from approval.models import PermissionApproval
            from django.utils import timezone
            from datetime import timedelta
            
            # Map PermissionEntry status to PermissionApproval status
            status_mapping = {
                'approved': 'approved',
                'cancelled': 'rejected',
            }
            approval_status = status_mapping.get(self.status)
            
            if approval_status:
                # Try to match by checking if approval_note contains this entry's ID
                # The approval view stores entry ID in approval_note as a workaround
                approval = PermissionApproval.objects.filter(
                    approval_status=approval_status,
                    approved_by__isnull=False,
                    approval_note__contains=f'entry_id:{self.pk}'
                ).select_related('approved_by').order_by('-created_at').first()
                
                # If not found by entry ID, try to match by approval_date (more accurate than created_at)
                if not approval:
                    time_window_start = self.updated_at - timedelta(minutes=15)
                    time_window_end = self.updated_at + timedelta(minutes=5)
                    approval = PermissionApproval.objects.filter(
                        approval_status=approval_status,
                        approved_by__isnull=False,
                        approval_date__isnull=False,
                        approval_date__gte=time_window_start,
                        approval_date__lte=time_window_end
                    ).select_related('approved_by').order_by('-approval_date').first()
                
                # If no match found by approval_date, try matching by created_at
                if not approval:
                    time_window_start = self.updated_at - timedelta(minutes=15)
                    time_window_end = self.updated_at + timedelta(minutes=5)
                    approval = PermissionApproval.objects.filter(
                        approval_status=approval_status,
                        approved_by__isnull=False,
                        created_at__gte=time_window_start,
                        created_at__lte=time_window_end
                    ).select_related('approved_by').order_by('-created_at').first()
                
                # Last fallback: get the most recent approval with matching status
                # This is less reliable but better than showing nothing
                if not approval:
                    approval = PermissionApproval.objects.filter(
                        approval_status=approval_status,
                        approved_by__isnull=False
                    ).select_related('approved_by').order_by('-approval_date', '-created_at').first()
                
                if approval and approval.approved_by:
                    return approval.approved_by.get_full_name() or approval.approved_by.username
        except Exception as e:
            # Log the exception for debugging (optional)
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error getting approver name for PermissionEntry {self.pk}: {str(e)}")
        return None


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


class TADAEntry(models.Model):
    APPROVAL_PENDING = 'pending'
    APPROVAL_APPROVED = 'approved'
    APPROVAL_REJECTED = 'rejected'
    APPROVAL_CHOICES = [
        (APPROVAL_PENDING, 'Pending'),
        (APPROVAL_APPROVED, 'Approved'),
        (APPROVAL_REJECTED, 'Rejected'),
    ]

    entry_date = models.DateField(auto_now_add=True)
    expense_date = models.DateField()
    entry_no = models.CharField(max_length=50, unique=True, blank=True, null=True)
    batch_no = models.CharField(max_length=50, blank=True)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='tada_entries',
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        related_name='tada_entries',
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    head_approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_CHOICES,
        default=APPROVAL_PENDING,
    )
    hr_approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_CHOICES,
        default=APPROVAL_PENDING,
    )
    acc_approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_CHOICES,
        default=APPROVAL_PENDING,
    )
    is_printed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-expense_date', '-entry_date', 'employee__staff_name']
        verbose_name = 'TADA Entry'
        verbose_name_plural = 'TADA Entries'

    def __str__(self):
        return f'{self.employee} - {self.expense_date} (Entry: {self.entry_no or "N/A"})'

    def save(self, *args, **kwargs):
        if not self.entry_no:
            # Generate entry number: TADA-YYYYMMDD-XXX
            today = datetime.now().date()
            prefix = f'TADA-{today.strftime("%Y%m%d")}'
            last_entry = TADAEntry.objects.filter(entry_no__startswith=prefix).order_by('-entry_no').first()
            if last_entry and last_entry.entry_no:
                try:
                    last_num = int(last_entry.entry_no.split('-')[-1])
                    new_num = last_num + 1
                except (ValueError, IndexError):
                    new_num = 1
            else:
                new_num = 1
            self.entry_no = f'{prefix}-{new_num:03d}'
        
        # Calculate total amount from sub items only if entry has a primary key
        # (can't access related objects before saving)
        if self.pk:
            self.total_amount = sum(item.amount for item in self.sub_items.all())
        else:
            # For new entries, total_amount will be calculated after sub_items are created
            # Set to 0 initially if not already set
            if not hasattr(self, '_total_amount_set'):
                self.total_amount = 0
        
        super().save(*args, **kwargs)

    @property
    def head_approval_badge_class(self) -> str:
        mapping = {
            self.APPROVAL_APPROVED: 'text-success bg-success-subtle border border-success',
            self.APPROVAL_REJECTED: 'text-danger bg-danger-subtle border border-danger',
            self.APPROVAL_PENDING: 'text-info bg-info-subtle border border-info',
        }
        return mapping.get(self.head_approval_status, 'text-secondary bg-secondary-subtle border border-secondary')

    @property
    def hr_approval_badge_class(self) -> str:
        mapping = {
            self.APPROVAL_APPROVED: 'text-success bg-success-subtle border border-success',
            self.APPROVAL_REJECTED: 'text-danger bg-danger-subtle border border-danger',
            self.APPROVAL_PENDING: 'text-info bg-info-subtle border border-info',
        }
        return mapping.get(self.hr_approval_status, 'text-secondary bg-secondary-subtle border border-secondary')

    @property
    def acc_approval_badge_class(self) -> str:
        mapping = {
            self.APPROVAL_APPROVED: 'text-success bg-success-subtle border border-success',
            self.APPROVAL_REJECTED: 'text-danger bg-danger-subtle border border-danger',
            self.APPROVAL_PENDING: 'text-info bg-info-subtle border border-info',
        }
        return mapping.get(self.acc_approval_status, 'text-secondary bg-secondary-subtle border border-secondary')


class TADAEntrySubItem(models.Model):
    tada_entry = models.ForeignKey(
        TADAEntry,
        on_delete=models.CASCADE,
        related_name='sub_items',
    )
    expense_type = models.ForeignKey(
        ExpenseType,
        on_delete=models.PROTECT,
        related_name='tada_sub_items',
    )
    sub_expense_type = models.ForeignKey(
        SubExpense,
        on_delete=models.PROTECT,
        related_name='tada_sub_items',
        null=True,
        blank=True,
    )
    from_location = models.CharField(max_length=255)
    to_location = models.CharField(max_length=255)
    start_meter = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    end_meter = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    total_kilometer = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    upload_image = models.ImageField(
        upload_to='tada_entry/images/',
        null=True,
        blank=True,
    )
    meter_upload_image = models.ImageField(
        upload_to='tada_entry/meter_images/',
        null=True,
        blank=True,
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'TADA Entry Sub Item'
        verbose_name_plural = 'TADA Entry Sub Items'

    def __str__(self):
        return f'{self.tada_entry.entry_no} - {self.expense_type.name} - {self.amount}'

    def save(self, *args, **kwargs):
        # Calculate total kilometer if start and end meter are provided
        if self.start_meter is not None and self.end_meter is not None:
            try:
                # Convert to Decimal if they're strings
                from decimal import Decimal
                start = Decimal(str(self.start_meter)) if not isinstance(self.start_meter, Decimal) else self.start_meter
                end = Decimal(str(self.end_meter)) if not isinstance(self.end_meter, Decimal) else self.end_meter
                
                if end >= start:
                    self.total_kilometer = end - start
                else:
                    # Handle meter rollover
                    self.total_kilometer = (Decimal('999999') - start) + end
            except (ValueError, TypeError):
                # If conversion fails, leave total_kilometer as is
                pass
        super().save(*args, **kwargs)