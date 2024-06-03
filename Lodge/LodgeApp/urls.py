from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('rooms/', views.rooms, name='rooms'),
    path('history/', views.history, name='history'),
    path('check-in/', views.check_in, name='check-in'),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('log-out/', views.sign_out, name='logout'),
]
