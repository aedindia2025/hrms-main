from django.contrib import admin

from .models import (
    HRCompOffApproval,
    LeaveApproval,
    PermissionApproval,
    TADAApproval,
    TravelApproval,
)


@admin.register(HRCompOffApproval)
class HRCompOffApprovalAdmin(admin.ModelAdmin):
    """
    Admin interface for HR Comp-Off Approvals.
    This allows managing permissions through Django admin.
    """
    list_display = (
        'comp_off_entry',
        'hr_approval_status',
        'hr_approval_by',
        'hr_approval_date',
        'created_at',
    )
    list_filter = (
        'hr_approval_status',
        'hr_approval_date',
        'created_at',
    )
    search_fields = (
        'comp_off_entry__employee__staff_name',
        'comp_off_entry__employee__staff_id',
        'hr_approval_by__username',
        'hr_approval_note',
    )
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Comp-Off Entry', {
            'fields': ('comp_off_entry',)
        }),
        ('HR Approval', {
            'fields': (
                'hr_approval_status',
                'hr_approval_by',
                'hr_approval_note',
                'hr_approval_date',
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(LeaveApproval)
class LeaveApprovalAdmin(admin.ModelAdmin):
    """Admin interface for Leave Approvals."""
    list_display = (
        'approval_status',
        'approved_by',
        'approval_date',
        'created_at',
    )
    list_filter = ('approval_status', 'approval_date', 'created_at')
    search_fields = ('approval_note', 'approved_by__username')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(PermissionApproval)
class PermissionApprovalAdmin(admin.ModelAdmin):
    """Admin interface for Permission Approvals."""
    list_display = (
        'approval_status',
        'approved_by',
        'approval_date',
        'created_at',
    )
    list_filter = ('approval_status', 'approval_date', 'created_at')
    search_fields = ('approval_note', 'approved_by__username')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(TADAApproval)
class TADAApprovalAdmin(admin.ModelAdmin):
    """Admin interface for TADA Approvals."""
    list_display = (
        'approval_status',
        'approved_by',
        'approval_date',
        'created_at',
    )
    list_filter = ('approval_status', 'approval_date', 'created_at')
    search_fields = ('approval_note', 'approved_by__username')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(TravelApproval)
class TravelApprovalAdmin(admin.ModelAdmin):
    """Admin interface for Travel Approvals."""
    list_display = (
        'approval_status',
        'approved_by',
        'approval_date',
        'created_at',
    )
    list_filter = ('approval_status', 'approval_date', 'created_at')
    search_fields = ('approval_note', 'approved_by__username')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
