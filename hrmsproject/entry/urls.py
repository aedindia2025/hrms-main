# entry/urls.py
from django.urls import path
from . import views

app_name = 'entry'

urlpatterns = [
    # Entry -> Comp Off
    path('comp-off/create/', views.comp_off_create, name='comp_off_create'),
    path('comp-off/list/', views.comp_off_list, name='comp_off_list'),
    path('comp-off/edit/<int:pk>/', views.comp_off_edit, name='comp_off_edit'),
    path('comp-off/delete/<int:pk>/', views.comp_off_delete, name='comp_off_delete'),

    # Entry -> Leave
    path('leave/create/', views.leave_entry_create, name='leave_entry_create'),
    path('leave/list/', views.leave_entry_list, name='leave_entry_list'),
    path('leave/edit/<int:pk>/', views.leave_entry_edit, name='leave_entry_edit'),
    path('leave/delete/<int:pk>/', views.leave_entry_delete, name='leave_entry_delete'),
    path('leave/print/', views.leave_entry_print, name='leave_entry_print'),

    # Entry -> Manual
    path('manual/create/', views.manual_entry_create, name='manual_entry_create'),
    path('manual/list/', views.manual_entry_list, name='manual_entry_list'),
    path('manual/print/', views.manual_entry_print, name='manual_entry_print'),

    # Entry -> Permission
    path('permission/create/', views.permission_entry_create, name='permission_entry_create'),
    path('permission/list/', views.permission_entry_list, name='permission_entry_list'),
    path('permission/edit/<int:pk>/', views.permission_entry_edit, name='permission_entry_edit'),
    path('permission/delete/<int:pk>/', views.permission_entry_delete, name='permission_entry_delete'),
    path('permission/print/', views.permission_entry_print, name='permission_entry_print'),

    # Entry -> Site
    path('site/list/', views.site_entry_list, name='site_entry_list'),
    path('site/create/', views.site_entry_create, name='site_entry_create'),
    path('site/edit/<int:pk>/', views.site_entry_edit, name='site_entry_edit'),
    path('site/delete/<int:pk>/', views.site_entry_delete, name='site_entry_delete'),

    # Entry -> TADA
    path('tada/create/', views.tada_entry_create, name='tada_entry_create'),
    path('tada/list/', views.tada_entry_list, name='tada_entry_list'),
    path('tada/edit/<int:pk>/', views.tada_entry_edit, name='tada_entry_edit'),
    path('tada/delete/<int:pk>/', views.tada_entry_delete, name='tada_entry_delete'),

    # Entry -> Travel
    path('travel/create/', views.travel_entry_create, name='travel_entry_create'),
    path('travel/list/', views.travel_entry_list, name='travel_entry_list'),
]
