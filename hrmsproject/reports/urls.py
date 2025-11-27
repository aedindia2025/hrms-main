from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('daily-attendance/', views.daily_attendance_report, name='daily_attendance_report'),
    path('attendance-snapshot/', views.attendance_snapshot_view, name='attendance_snapshot_view'),
    path('attendance/', views.attendance_report_list, name='attendance_report_list'),
    path('attendance/view/', views.attendance_report_view, name='attendance_report_view'),
    path('monthly/', views.monthly_report_list, name='monthly_report_list'),
    path('tada/', views.tada_report_list, name='tada_report_list'),
]
