from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Staff, Room, Guest, Log, Revenue, CheckIns, Company, Suite

from django.contrib.auth import login, authenticate, logout, get_user_model

Staff = get_user_model()

from datetime import datetime, date, timedelta
from django.utils import timezone

import numpy as np
import re

from collections import defaultdict

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
        context = {'page_name':'Sign in'}
        return render(request, 'pages-sign-in.html', context)

def sign_out(request):
    logout(request)
    return redirect('sign-in')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    logs = Log.objects.filter(
        timestamp__date=timezone.now().date(),
        company=request.user.company
        ).order_by('-id')[:5]
    active_guests = Guest.objects.filter(check_out__isnull=True,
                                         company=request.user.company)
    total_guests = Guest.objects.filter(company=request.user.company).count()
    available_rooms = Room.objects.filter(room_status=False,
                                          company=request.user.company).count()
    
    context = {
        'active_guests': active_guests,
        'total_guests': total_guests,
        'staff': request.user,
        'logs': logs,
        'available_rooms': available_rooms,
        'page_name':'Home'
    }
    return render(request, 'index.html', context)

def rooms(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    suite_types = Suite.objects.values_list('type', flat=True).distinct()
    
    suite_types_dict = {}
    for suite_type in suite_types:
        suite_rooms = Room.objects.filter(suite__type=suite_type, company=request.user.company)
        suite_types_dict[suite_type] = suite_rooms
        
    guests = Guest.objects.filter(check_out__isnull=True, company=request.user.company)
    room_guest_mapping = {guest.room.id: guest for guest in guests}
    
    context = {
        'suite_types': suite_types_dict,
        'room_guest_mapping': room_guest_mapping,
        'check_out_url': reverse('check-out'),
        'check_in_url': reverse('check-in'),
        'page_name':'Rooms'
    }
    
    return render(request, 'room-carousel.html', context)

def history(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    guests = Guest.objects.filter(company=request.user.company)
    context = {'guests': guests, 'page_name':'History'}
    return render(request, 'guest-history.html', context)

def check_in(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    if request.method == 'POST':
        room_id = request.POST.get('room')
        room = get_object_or_404(Room, id=room_id)

        guest = Guest.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            number=request.POST.get('phone'),
            room=room,
            staff=request.user,
            company=request.user.company
        )

        room.room_status = True
        room.save()
        
        Log.objects.create(
            staff=request.user,
            check_in_action=f'{request.user} checked in {guest.name} into Room {guest.room.room_number}',
            check_status=True, 
            timestamp=guest.check_in,
            company=guest.company
        )
        
        CheckIns.objects.create(
            company=guest.staff.company
        )

        return redirect('dashboard')
    
    rooms = Room.objects.filter(room_status=False)
    context = {'rooms': rooms, 'page_name':'Check In'}
    return render(request, 'check-in.html', context)

@csrf_exempt
def check_out(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    if request.method == 'POST':
        guest_ids = request.POST.getlist('guest_ids')
        guests_to_check_out = Guest.objects.filter(id__in=guest_ids)

        for guest in guests_to_check_out:
            guest.check_out = timezone.now()
            guest.save()
            
            revenue_amount = guest.room.room_price * (guest.check_out - guest.check_in).days
            revenue = Revenue.objects.create(revenue=revenue_amount, company=request.user.company)
            
            guest.revenue = revenue
            guest.save()
            
            guest.room.room_status = False
            guest.room.save()
            
            Log.objects.create(
                staff=request.user,
                check_out_action=f'{request.user} checked out {guest.name} from Room {guest.room.room_number}',
                check_status=False, 
                timestamp=guest.check_out,
                company=request.user.company
            )
        return redirect('dashboard')
    
    return redirect('sign-in')

@csrf_exempt
def onboarding(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        
        company = Company.objects.create(name=company_name)
        
        suite_type_pattern = re.compile(r'suite_type_\d+')
        suite_types = [value for key, value in request.POST.items() if suite_type_pattern.match(key)]
        
        suite_price_pattern = re.compile(r'suite_price_\d+')
        suite_prices = [value for key, value in request.POST.items() if suite_price_pattern.match(key)]
        
        suite_rooms_pattern = re.compile(r'suite_rooms_\d+')
        suite_rooms = [value for key, value in request.POST.items() if suite_rooms_pattern.match(key)]
        
        room_tag_pattern = re.compile(r'room_tag_(\d+)_\d+')
        room_tags_grouped = defaultdict(list)
        for key, value in request.POST.items():
            match = room_tag_pattern.match(key)
            if match:
                suite_number = int(match.group(1))
                room_tags_grouped[suite_number].append((key, value))
        
        for iter in range(len(suite_types)):
            suite_type = suite_types[iter]
            suite_price = suite_prices[iter]
            
            new_suite = Suite.objects.create(
                company=company,
                type=suite_type,
                price=suite_price
            )
            
            for room in room_tags_grouped[iter + 1]:
                room_tag = room[1]
                new_room = Room.objects.create(
                    suite=new_suite,
                    company=company,
                    room_number=room_tag
                )
            
        return redirect('sign-in')
    
    return render(request, 'onboarding.html')

def analytics(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    top_guests = Guest.objects.all().order_by('-id')[:5]
    guests = Guest.objects.all()
    
    check_ins = CheckIns.objects.filter(time__year=timezone.now().year, company=request.user.company)
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
    
    total_revenue = 0
    for guest in guests:
        try:
            rev = guest.revenue
            total_revenue += rev.revenue
        except:
            total_revenue += 0
        
    monthly_revenue = (total_revenue/(timezone.now().month))/1000
    
    month_revenue_guests = Guest.objects.filter(check_out__month=timezone.now().month, company=request.user.company)
    
    if timezone.now().month != 1:
        prev_month_revenue_guests = Guest.objects.filter(check_out__month=(timezone.now().month)-1, company=request.user.company)
    else:
        prev_month_revenue_guests = {}
    
    month_revenue = 0
    for guests in month_revenue_guests:
        revenue = guests.revenue
        try:
            month_revenue+= revenue.revenue
        except:
            month_revenue+= 0
        
    prev_month_revenue = 0
    for guests in prev_month_revenue_guests:
        revenue = guests.revenue
        try:
            prev_month_revenue+= revenue.revenue
        except:
            prev_month_revenue+= 0
        
    try:
        revenue_growth = ((month_revenue-prev_month_revenue)/prev_month_revenue)*100
    except:
        revenue_growth = 0
    
    context = {'check_in_data':check_in_data, 'guests':Guest.objects.all(), 'top_guests':top_guests, 'check_in_rate':check_in_rate, 'guest_growth':guest_growth, 'total_revenue':int(total_revenue)/1000, 'monthly_revenue':monthly_revenue, 'revenue_growth':revenue_growth, 'page_name':'Analytics'}
    return render(request, 'analytics.html', context)