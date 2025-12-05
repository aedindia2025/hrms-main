from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import CompOffEntry, SiteEntry, PermissionEntry, LeaveEntry


@admin.register(CompOffEntry)
class CompOffEntryAdmin(admin.ModelAdmin):
    list_display = (
        'work_date',
        'employee',
        'site',
        'day_status',
        'head_approval_status',
    )
    list_filter = ('day_status', 'head_approval_status', 'work_date')
    search_fields = (
        'employee__staff_name',
        'employee__staff_id',
        'site__name',
    )
    autocomplete_fields = ('employee', 'site')
    date_hierarchy = 'work_date'


@admin.register(SiteEntry)
class SiteEntryAdmin(admin.ModelAdmin):
    list_display = (
        'employee_name',
        'transfer_date',
        'from_site',
        'to_site',
        'transfer_type',
    )
    search_fields = ('employee_name', 'from_site', 'to_site')
    list_filter = ('transfer_type', 'transfer_date')
    date_hierarchy = 'transfer_date'


# ==================== Permission Management Admin ====================
# This admin class helps manage permissions for models that may not be fully registered
# It allows you to see and manage permissions through Django admin

class PermissionAdmin(admin.ModelAdmin):
    """
    Enhanced Permission admin for better permission management.
    This makes it easier to find and assign permissions for approval pages.
    """
    list_display = ('name', 'content_type', 'codename')
    list_filter = ('content_type__app_label', 'content_type__model')
    search_fields = ('name', 'codename', 'content_type__app_label', 'content_type__model')
    readonly_fields = ('name', 'content_type', 'codename')

    def has_add_permission(self, request):
        """Permissions are auto-created by Django, so we disable manual creation."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Don't allow deletion of permissions."""
        return False


# Unregister default Permission admin and register our enhanced version
# Only unregister if it's already registered
if admin.site.is_registered(Permission):
    admin.site.unregister(Permission)
admin.site.register(Permission, PermissionAdmin)


# ==================== Helper: Register models for permission management ====================
# If you have other Entry models (LeaveEntry, PermissionEntry, TADAEntry, TravelEntry, ManualEntry)
# that are not yet created, you can register them here when they are created.
# For now, Django will automatically create permissions for any models that exist.

@admin.register(PermissionEntry)
class PermissionEntryAdmin(admin.ModelAdmin):
    list_display = (
        'permission_date',
        'employee',
        'site',
        'per_hr_count',
        'status',
    )
    list_filter = ('status', 'permission_date')
    search_fields = (
        'employee__staff_name',
        'employee__staff_id',
        'site__name',
    )
    autocomplete_fields = ('employee', 'site')
    date_hierarchy = 'permission_date'


@admin.register(LeaveEntry)
class LeaveEntryAdmin(admin.ModelAdmin):
    list_display = (
        'from_date',
        'to_date',
        'employee',
        'site',
        'leave_type',
        'leave_days',
        'approval_status',
    )
    list_filter = ('leave_type', 'approval_status', 'leave_duration_type', 'from_date')
    search_fields = (
        'employee__staff_name',
        'employee__staff_id',
        'site__name',
        'reason',
    )
    autocomplete_fields = ('employee', 'site')
    date_hierarchy = 'from_date'
#
# @admin.register(TADAEntry)
# class TADAEntryAdmin(admin.ModelAdmin):
#     list_display = ('id', '__str__')
#
# @admin.register(TravelEntry)
# class TravelEntryAdmin(admin.ModelAdmin):
#     list_display = ('id', '__str__')
#
# @admin.register(ManualEntry)
# class ManualEntryAdmin(admin.ModelAdmin):
#     list_display = ('id', '__str__')
