from django.db import models
from django.contrib.auth import get_user_model

from entry.models import CompOffEntry, LeaveEntry
from master.models import Employee

User = get_user_model()


class HRCompOffApproval(models.Model):
    """
    Separate model for HR Comp-Off Approvals.
    This allows proper permission management through Django admin.
    """
    APPROVAL_PENDING = 'pending'
    APPROVAL_APPROVED = 'approved'
    APPROVAL_REJECTED = 'rejected'
    APPROVAL_CHOICES = [
        (APPROVAL_PENDING, 'Pending'),
        (APPROVAL_APPROVED, 'Approved'),
        (APPROVAL_REJECTED, 'Rejected'),
    ]

    comp_off_entry = models.OneToOneField(
        CompOffEntry,
        on_delete=models.CASCADE,
        related_name='hr_approval',
        help_text='The Comp-Off Entry being approved'
    )
    hr_approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_CHOICES,
        default=APPROVAL_PENDING,
    )
    hr_approval_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hr_comp_off_approvals',
        help_text='HR user who approved/rejected'
    )
    hr_approval_note = models.TextField(
        blank=True,
        help_text='Notes or comments from HR'
    )
    hr_approval_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Date and time of HR approval'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'HR Comp-Off Approval'
        verbose_name_plural = 'HR Comp-Off Approvals'
        ordering = ['-created_at']
        permissions = [
            ('view_hr_compoff_approval', 'Can view HR Comp-Off Approvals'),
            ('approve_hr_compoff_approval', 'Can approve HR Comp-Off Approvals'),
            ('reject_hr_compoff_approval', 'Can reject HR Comp-Off Approvals'),
        ]

    def __str__(self):
        return f'HR Approval for {self.comp_off_entry} - {self.get_hr_approval_status_display()}'

    @property
    def hr_approval_badge_class(self) -> str:
        """Return Bootstrap badge class for approval status."""
        mapping = {
            self.APPROVAL_APPROVED: 'text-success bg-success-subtle border border-success',
            self.APPROVAL_REJECTED: 'text-danger bg-danger-subtle border border-danger',
            self.APPROVAL_PENDING: 'text-info bg-info-subtle border border-info',
        }
        return mapping.get(
            self.hr_approval_status,
            'text-secondary bg-secondary-subtle border border-secondary'
        )


class LeaveApproval(models.Model):
    """
    Model for Leave Approvals.
    Connected to LeaveEntry model.
    """
    APPROVAL_PENDING = 'pending'
    APPROVAL_APPROVED = 'approved'
    APPROVAL_REJECTED = 'rejected'
    APPROVAL_CHOICES = [
        (APPROVAL_PENDING, 'Pending'),
        (APPROVAL_APPROVED, 'Approved'),
        (APPROVAL_REJECTED, 'Rejected'),
    ]

    leave_entry = models.OneToOneField(
        LeaveEntry,
        on_delete=models.CASCADE,
        related_name='leave_approval',
        help_text='The Leave Entry being approved',
        null=True,
        blank=True
    )
    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_CHOICES,
        default=APPROVAL_PENDING,
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leave_approvals',
        help_text='User who approved/rejected'
    )
    approval_note = models.TextField(blank=True, help_text='Notes or comments from approver')
    approval_date = models.DateTimeField(null=True, blank=True, help_text='Date and time of approval')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Leave Approval'
        verbose_name_plural = 'Leave Approvals'
        ordering = ['-created_at']
        permissions = [
            ('view_leave_approval', 'Can view Leave Approvals'),
            ('approve_leave_approval', 'Can approve Leave Approvals'),
        ]

    def __str__(self):
        if self.leave_entry:
            return f'Leave Approval for {self.leave_entry} - {self.get_approval_status_display()}'
        return f'Leave Approval - {self.get_approval_status_display()}'

    @property
    def approval_badge_class(self) -> str:
        """Return CSS classes for approval status badge."""
        mapping = {
            self.APPROVAL_APPROVED: 'background-color:#d4edda; color:#155724;',
            self.APPROVAL_REJECTED: 'background-color:#f8d7da; color:#721c24;',
            self.APPROVAL_PENDING: 'background-color:#d1ecf1; color:#0c5460;',
        }
        return mapping.get(self.approval_status, 'background-color:#e2e3e5; color:#383d41;')

    @property
    def approval_icon_color(self) -> str:
        """Return icon color for approval status."""
        mapping = {
            self.APPROVAL_APPROVED: '#28a745',
            self.APPROVAL_REJECTED: '#dc3545',
            self.APPROVAL_PENDING: '#17a2b8',
        }
        return mapping.get(self.approval_status, '#6c757d')


class PermissionApproval(models.Model):
    """
    Model for Permission Approvals.
    Can be extended when PermissionEntry model is created.
    """
    APPROVAL_PENDING = 'pending'
    APPROVAL_APPROVED = 'approved'
    APPROVAL_REJECTED = 'rejected'
    APPROVAL_CHOICES = [
        (APPROVAL_PENDING, 'Pending'),
        (APPROVAL_APPROVED, 'Approved'),
        (APPROVAL_REJECTED, 'Rejected'),
    ]

    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_CHOICES,
        default=APPROVAL_PENDING,
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='permission_approvals',
    )
    approval_note = models.TextField(blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Permission Approval'
        verbose_name_plural = 'Permission Approvals'
        ordering = ['-created_at']
        permissions = [
            ('view_permission_approval', 'Can view Permission Approvals'),
            ('approve_permission_approval', 'Can approve Permission Approvals'),
        ]

    def __str__(self):
        return f'Permission Approval - {self.get_approval_status_display()}'


class TADAApproval(models.Model):
    """
    Model for TADA Approvals.
    Can be extended when TADAEntry model is created.
    """
    APPROVAL_PENDING = 'pending'
    APPROVAL_APPROVED = 'approved'
    APPROVAL_REJECTED = 'rejected'
    APPROVAL_CHOICES = [
        (APPROVAL_PENDING, 'Pending'),
        (APPROVAL_APPROVED, 'Approved'),
        (APPROVAL_REJECTED, 'Rejected'),
    ]

    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_CHOICES,
        default=APPROVAL_PENDING,
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tada_approvals',
    )
    approval_note = models.TextField(blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'TADA Approval'
        verbose_name_plural = 'TADA Approvals'
        ordering = ['-created_at']
        permissions = [
            ('view_tada_approval', 'Can view TADA Approvals'),
            ('approve_tada_approval', 'Can approve TADA Approvals'),
        ]

    def __str__(self):
        return f'TADA Approval - {self.get_approval_status_display()}'


class TravelApproval(models.Model):
    """
    Model for Travel Approvals.
    Can be extended when TravelEntry model is created.
    """
    APPROVAL_PENDING = 'pending'
    APPROVAL_APPROVED = 'approved'
    APPROVAL_REJECTED = 'rejected'
    APPROVAL_CHOICES = [
        (APPROVAL_PENDING, 'Pending'),
        (APPROVAL_APPROVED, 'Approved'),
        (APPROVAL_REJECTED, 'Rejected'),
    ]

    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_CHOICES,
        default=APPROVAL_PENDING,
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='travel_approvals',
    )
    approval_note = models.TextField(blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Travel Approval'
        verbose_name_plural = 'Travel Approvals'
        ordering = ['-created_at']
        permissions = [
            ('view_travel_approval', 'Can view Travel Approvals'),
            ('approve_travel_approval', 'Can approve Travel Approvals'),
        ]

    def __str__(self):
        return f'Travel Approval - {self.get_approval_status_display()}'
