from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_code', 'job_title', 'location')
    search_fields = (
        'user__username',
        'user__email',
        'employee_code',
        'job_title',
        'location',
    )
    list_filter = ('job_title', 'location')
