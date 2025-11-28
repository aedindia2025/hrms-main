from django.contrib import admin

from .models import CompOffEntry, SiteEntry


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
