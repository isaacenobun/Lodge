from django.shortcuts import render, get_object_or_404, redirect

from .models import *

from django.contrib.auth import login, authenticate, logout, get_user_model

Staff = get_user_model()

from datetime import datetime, date, timedelta
from django.utils import timezone

import numpy as np

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
        
        active_guests = Guest.objects.filter(check_out__isnull=True)
        total_guests = Guest.objects.all()
        rooms = Room.objects.filter(room_status='False')
        
        logs = Log.objects.filter(timestamp__date=timezone.now().date()).order_by('-id')[:5]
        context = {'active_guests':active_guests, 'total_guests':total_guests, 'staff':staff, 'logs':logs, 'rooms':rooms}
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
                check_in_action = f'{request.user} checked in {guest.name} into Room {guest.room.room_number}',
                check_status = True, 
                timestamp = guest.check_in
            )
            
            checkIn = CheckIns.objects.create(
            
            )
            
            return redirect('dashboard')
        
        rooms = Room.objects.filter(room_status=False)
        context = {'rooms':rooms}
        return render(request, 'pages-check-in-out.html', context)
    else:
        return redirect('sign-in')
    
def check_out(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            guest_ids = request.POST.getlist('guest_ids')

            guests_to_check_out = Guest.objects.filter(id__in=guest_ids)

            for guest in guests_to_check_out:
                guest.check_out = timezone.now()
                guest.save()
                guest.room.room_status = False
                guest.room.save()
                
                Log.objects.create(
                    staff = request.user,
                    check_in_action = f'{request.user} checked out {guest.name} from Room {guest.room.room_number}',
                    check_status = False, 
                    timestamp = guest.check_out
                )
                
                Revenue.objects.create(
                    revenue = guest.room.room_price,
                    guest_check_out = guest
                )

            return redirect('dashboard') 
    
    return redirect('sign-in')

def onboarding(request):
    return render(request, 'onboarding.html')

def analytics(request):
    
    check_ins = CheckIns.objects.filter(time__year=timezone.now().year)
    year_dict = {i:0 for i in range(1,13)}
    
    for check_in in check_ins:
        month = check_in.time.month
        year_dict[month] += 1
    
    # check_in_data = list(year_dict.values())
    check_in_data = [8,8,8,8,8,15]
    
    check_in_rate = int(np.sum(check_in_data)/(timezone.now().month * 4))
    
    if timezone.now().month == 1:
        guest_growth = 0
    else:
        try:
            guest_growth = (check_in_data[(timezone.now().month)-1] - check_in_data[(timezone.now().month)-2])/check_in_data[(timezone.now().month)-2] *100
        except:
            guest_growth = 0
    
    
    top_guests = Guest.objects.all().order_by('-id')[:5]
    guests = Guest.objects.all()
    
    revenues = Revenue.objects.all()
    
    total_revenue = 0
    for rev in revenues:
        total_revenue += rev.revenue
        
    weekly_revenue = (total_revenue/(timezone.now().month*4))/1000
    
    month_revenue_guests = Guest.objects.filter(check_out__month=timezone.now().month)
    
    if timezone.now().month != 1:
        prev_month_revenue_guests = Guest.objects.filter(check_out__month=(timezone.now().month)-1)
    else:
        prev_month_revenue_guests = {}
    
    month_revenue = 0
    for guests in month_revenue_guests:
        month_revenue+= guests.room.room_price
    
    prev_month_revenue = 0
    for guests in prev_month_revenue_guests:
        prev_month_revenue+= guests.room.room_price
    
    try:
        revenue_growth = ((month_revenue-prev_month_revenue)/prev_month_revenue)*100
    except:
        revenue_growth = 0
    
    context = {'check_in_data':check_in_data, 'guests':guests, 'top_guests':top_guests, 'check_in_rate':check_in_rate, 'guest_growth':guest_growth, 'total_revenue':int(total_revenue)/1000, 'weekly_revenue':weekly_revenue, 'revenue_growth':revenue_growth}
    return render(request, 'analytics.html', context)