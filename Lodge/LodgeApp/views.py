from django.shortcuts import render, get_object_or_404, redirect

from .models import *

from django.contrib.auth import login, authenticate, logout

from datetime import datetime, date, timedelta
from django.utils import timezone

def filter_datetimes_for_today(datetimes):
    today = date.today()
    filtered_datetimes = [dt for dt in datetimes if dt.date() == today]
    return filtered_datetimes

# Create your views here.
def sign_in(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            staff = Staff.objects.get(email=email)
        except Staff.DoesNotExist:
            # messages.warning(request, f"Staff with {email} does not exist")
            return redirect('sign-in')

        staff = authenticate(request, email=email, password=password)

        if staff is not None:
            login(request, staff)
            # messages.success(request, f"Welcome {request.POST.get('email')}")
            return redirect('dashboard')
        else:
            # messages.warning(request, "Invalid password")
            return redirect('sign-in')
    else:
        return render(request, 'sign-in.html')

def sign_out(request):
    logout(request)
    return redirect('sign-in')

def dashboard(request):
    if request.user.is_authenticated:
        logs = Log.objects.all()
        staff = request.user
        guests = Guest.objects.all()
        
        logs = Log.objects.filter(timestamp__date=timezone.now().date()).order_by('-id')[:5]
        context = {'guests':guests, 'staff':staff, 'logs':logs}
        return render(request, 'index.html', context)
    else:
        return redirect('sign-in')

def rooms(request):
    
    context = {}
    return render(request, 'pages-room-carousel.html', context)

def history(request):
    if request.user.is_authenticated:
        guests = Guest.objects.all()
        context = {'guests':guests}
        return render(request, 'pages-guest-history.html', context)
    else:
        return redirect('sign-in')

def check_in(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            room_id = request.POST.get('room')
            room = get_object_or_404(Room, id=room_id)

            guest = Guest.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                number=request.POST.get('phone'),
                room=room,
                staff = request.user
            )

            room.room_status = True
            room.save()
            
            Log.objects.create(
                staff = request.user,
                action = f'{request.user} checked in {guest.name} into Room {guest.room.room_number}',
                check_status = True 
            )
            return redirect('dashboard')
        
        rooms = Room.objects.filter(room_status=False)
        context = {'rooms':rooms}
        return render(request, 'pages-check-in-out.html', context)
    else:
        return redirect('sign-in')