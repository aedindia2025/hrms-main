from django.contrib import admin

from .models import SiteEntry


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
