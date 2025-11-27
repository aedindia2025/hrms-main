# accounts/urls.py
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    # ==================== Home & Authentication ====================
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # ==================== Profile & Settings ====================
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('inbox/', views.inbox, name='inbox'),

    # ==================== Accounts ====================
    path('cash-reports/', views.cash_reports_list, name='cash_reports_list'),

    # ==================== Demo ====================
    path('demo/add/', views.demo_add, name='demo_add'),
    path('demo/store/', views.demo_store, name='demo_store'),
    path('demo/list/', views.demo_list, name='demo_list'),
]
