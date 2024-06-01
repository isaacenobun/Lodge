from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('rooms/', views.rooms, name='rooms'),
    path('history/', views.history, name='history'),
    path('checkin/', views.check_in, name='check-in'),
]
