from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='index'),
    path('home', views.dashboard, name='dashboard'),
    path('onboarding', views.onboarding, name='onboarding'),
    path('analytics', views.analytics, name='analytics'),
    path('rooms/', views.rooms, name='rooms'),
    path('history/', views.history, name='history'),
    path('logs/', views.logs, name='logs'),
    path('check-in/', views.check_in, name='check-in'),
    path('check-out/', views.check_out, name='check-out'),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('log-out/', views.sign_out, name='logout'),
    path('landing', views.landing, name='landing'),
    path('settings/', views.settings, name='settings'),
    path('delete-suite/', views.delete_suite, name='delete-suite'),
    path('staff-add/', views.staff_add, name='staff-add'),
    path('staff-edit/', views.staff_edit, name='staff-edit'),
    path('download-history-csv/', views.download_history_csv, name='download_history_csv'),
    path('download-analytics-csv/', views.download_analytics_csv, name='download_analytics_csv'),
    path('download-logs-csv/', views.download_logs_csv, name='download_logs_csv'),
    path('extend/', views.extend, name='extend'),
    path('edit-rooms/', views.edit_rooms, name='edit-rooms'),
    path('expenses/', views.expenses, name='expenses'),
]
