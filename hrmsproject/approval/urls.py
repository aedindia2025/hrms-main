# approval/urls.py
from django.urls import path
from . import views

app_name = 'approval'

urlpatterns = [
    # ==================== HR Approval ====================
    path('hr/', views.hr_comp_off_approval, name='hr_comp_off_approval'),
    
    # ==================== Daily Attendance ====================
    path('daily-attendance/print/', views.daily_attendance_print, name='daily_attendance_print'),

    # ==================== Leave ====================
    path('leave/', views.leave_approval_list, name='leave_approval_list'),

    # ==================== Permission ====================
    path('permission/', views.permission_approval_list, name='permission_approval_list'),

    # ==================== TADA ====================
    path('tada/', views.tada_approval_list, name='tada_approval_list'),
    path('tada-head/', views.tada_head_approval_list, name='tada_head_approval_list'),
    path('tada-hr/', views.tada_hr_approval_list, name='tada_hr_approval_list'),
    path('tada-hr/print/', views.tada_hr_print, name='tada_hr_print'),

    # ==================== Travel HR ====================
    path('travel-hr/', views.travel_hr_approval_list, name='travel_hr_approval_list'),
]
