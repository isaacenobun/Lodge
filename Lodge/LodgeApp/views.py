from .imports import *

def sign_up(request):
    if request.user.is_authenticated:
        if request.user.company is not None:
            return redirect('dashboard')
        else:
            return redirect('onboarding')

    if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            new_user = Staff.objects.create(
                username = username,
                email = email,
                password = password
            )
            
            new_user.set_password(password)
            new_user.is_superuser = True
            new_user.is_staff = True
            new_user.save()
            
            new_user = authenticate(
                request, 
                email=email, 
                password=password
            )
            login(request, new_user)
            return redirect('onboarding')

    context = {'page_name': 'Sign Up'}
    return render(request, 'pages-sign-up.html', context)

@csrf_exempt
def onboarding(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    if request.user.is_authenticated and request.user.company is not None:
        return redirect('dashboard')
    
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        
        company = Company.objects.create(name=company_name)
        
        suite_type_pattern = re.compile(r'suite_type_\d+')
        suite_types = [value for key, value in request.POST.items() if suite_type_pattern.match(key)]
        print (suite_types)
        
        suite_price_pattern = re.compile(r'suite_price_\d+')
        suite_prices = [value for key, value in request.POST.items() if suite_price_pattern.match(key)]
        print (suite_prices)
        
        suite_rooms_pattern = re.compile(r'suite_rooms_\d+')
        suite_rooms = [value for key, value in request.POST.items() if suite_rooms_pattern.match(key)]
        print (suite_rooms)
        
        for iter in range(len(suite_types)):
            suite_type = suite_types[iter]
            suite_price = suite_prices[iter]
            suite_room = suite_rooms[iter]
            
            new_suite = Suite.objects.create(
                company=company,
                type=suite_type,
                price=float(suite_price)
            )
            
            for room_number in range(1,int(suite_room)+1):
                new_room = Room.objects.create(
                    suite=new_suite,
                    company=company,
                    room_number=room_number
                )
        owner = request.user
        owner.company = company
        owner.owner = True
        owner.save()
            
        return redirect('dashboard')
    
    return render(request, 'onboarding.html')

def sign_in(request):
    if request.user.is_authenticated:
        if request.user.company is not None:
            return redirect('dashboard')
        else:
            return redirect('onboarding')
    
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
    
    elif request.user.is_authenticated and request.user.company is None:
        return redirect('onboarding')
    
    now=timezone.now()
    
    logs = Log.objects.filter(
        company=request.user.company
        ).order_by('-id')[:5]
    active_guests = Guest.objects.filter(check_out__gte=now,
                                         company=request.user.company)
    total_guests = Guest.objects.filter(company=request.user.company).count()
    available_rooms = Room.objects.filter(room_status=False,
                                          company=request.user.company)
    guests = Guest.objects.filter(company=request.user.company)

    context = {
        'now':now,
        'active_guests': active_guests,
        'total_guests': total_guests,
        'staff': request.user,
        'logs': logs,
        'available_rooms': available_rooms,
        'page_name':'Home',
        'guests': guests
    }
    return render(request, 'index.html', context)

def rooms(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    if request.user.is_authenticated and request.user.company is None:
        return redirect('onboarding')
    
    now = timezone.now()
    
    suite_types = Suite.objects.filter(company=request.user.company).values_list('type', flat=True).distinct()
    
    suite_types_dict = {}
    for suite_type in suite_types:
        suite_rooms = Room.objects.filter(suite__type=suite_type, company=request.user.company)
        suite_types_dict[suite_type] = suite_rooms
    
    suite_types_dict['All'] = Room.objects.filter(company=request.user.company)
    
    guests = Guest.objects.filter(check_out__gt=now,
                                  company=request.user.company
                                  )
    room_guest_mapping = {guest.room.id: guest for guest in guests}
    
    available_rooms = Room.objects.filter(room_status=False,
                                          company=request.user.company)
    guests = Guest.objects.filter(company=request.user.company)
    context = {
        'available_rooms':available_rooms,
        'suite_types': suite_types_dict,
        'room_guest_mapping': room_guest_mapping,
        'check_out_url': reverse('check-out'),
        'check_in_url': reverse('check-in'),
        'page_name':'Rooms',
        'guests':guests
    }
    
    return render(request, 'room-carousel.html', context)

def history(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    if request.user.is_authenticated and request.user.company is None:
        return redirect('onboarding')
    
    guests = Guest.objects.filter(company=request.user.company)
    available_rooms = Room.objects.filter(room_status=False,
                                          company=request.user.company)
    context = {
        'available_rooms':available_rooms,
        'guests': guests, 
        'page_name':'History'
    }
    return render(request, 'guest-history.html', context)

def download_history_csv(request):
    
    guests = Guest.objects.filter(company=request.user.company)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Guest List.csv"'

    writer = csv.writer(response)
    
    writer.writerow(['#', 'Name', 'Email', 'Phone Number', 'Suite', 'Room', 'Check-in Date', 'Check-Out Date'])  # CSV Header
    
    count=1
    for guest in guests:
        writer.writerow([count, guest.name, guest.email, guest.number, guest.room.suite.type, guest.room.room_number, guest.check_in.strftime('%a %d %b %Y, %I:%M%p'), guest.check_out.strftime('%a %d %b %Y, %I:%M%p')])
        count+=1

    return response

def logs(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    if request.user.is_authenticated and request.user.company is None:
        return redirect('onboarding')
    
    available_rooms = Room.objects.filter(room_status=False,
                                          company=request.user.company)
    logs = Log.objects.filter(company=request.user.company).order_by('-id')
    
    guests = Guest.objects.filter(company=request.user.company)
    
    context={
        'available_rooms':available_rooms,
        'logs':logs,
        'page_name':'Logs',
        'guests':guests
    }
    
    return render(request, 'logs.html', context)

def settings(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    if request.user.is_authenticated and request.user.company is None:
        return redirect('onboarding')
    
    staffs = Staff.objects.filter(company = request.user.company)
    
    guests = Guest.objects.filter(company=request.user.company)
    
    context = {
        'staffs':staffs,
        'page_name':'Settings',
        'guests':guests
    }
    return render(request, 'settings.html', context)

def check_in(request):
    if request.method == 'POST':
        
        if not request.POST.get('name_'):
            room_id = request.POST.get('room')
            room = get_object_or_404(Room, id=room_id)
            
            duration = request.POST.get('duration')
            revenue = float(duration) * float(room.suite.price)
            revenue = Revenue.objects.create(
                revenue = revenue,
                company = request.user.company
            )
            check_out = datetime.now() + timedelta(days=int(duration))
            
            guest = Guest.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                number=request.POST.get('phone'),
                room=room,
                staff=request.user,
                check_out=check_out,
                revenue=revenue,
                company=request.user.company,
                duration=request.POST.get('duration')
            )

            room.room_status = True
            room.save()
            
            Log.objects.create(
                staff=request.user,
                action=f'{request.user} checked in {guest.name} into Room {guest.room.room_number}',
                check_status=True, 
                timestamp=guest.check_in,
                company=guest.company
            )
            
            Log.objects.create(
                staff=request.user,
                action=f'{guest.name} paid N{revenue.revenue}',
                check_status=True, 
                timestamp=guest.check_in,
                company=guest.company
            )
            
            CheckIns.objects.create(
                company=guest.staff.company
            )

            return redirect('dashboard')
        
        else:
            # Push old record to history
            name_ = request.POST.get('name_')
            guest = Guest.objects.get(name=name_)
            
            GuestHistory.objects.create(
                guest=guest,
                name=guest.name,
                email=guest.email,
                number=guest.number,
                room=guest.room,
                check_in=guest.check_in,
                staff=guest.staff,
                check_out=guest.check_out,
                revenue=guest.revenue,
                company=guest.company,
                duration=guest.duration
            )
            
            # Update old record instance to new record
            room_id = request.POST.get('room_')
            room = get_object_or_404(Room, id=room_id)
            
            duration = request.POST.get('duration_')
            revenue = float(duration) * float(room.suite.price)
            revenue = Revenue.objects.create(
                revenue = revenue,
                company = request.user.company
            )
            check_out = datetime.now() + timedelta(days=int(duration))
            
            guest.room = room
            guest.check_in = datetime.now()
            guest.staff = request.user
            guest.check_out=check_out
            guest.revenue = revenue
            guest.duration = duration
            
            guest.save()

            room.room_status = True
            room.save()
            
            Log.objects.create(
                staff=request.user,
                action=f'{request.user} checked in {guest.name} into Room {guest.room.room_number}',
                check_status=True, 
                timestamp=guest.check_in,
                company=guest.company
            )
            
            Log.objects.create(
                staff=request.user,
                action=f'{guest.name} paid N{revenue.revenue}',
                check_status=True, 
                timestamp=guest.check_in,
                company=guest.company
            )
            
            CheckIns.objects.create(
                company=guest.staff.company
            )

            return redirect('dashboard')

@csrf_exempt
def check_out(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    if request.method == 'POST':
        guest_ids = request.POST.getlist('guest_ids')
        guests_to_check_out = Guest.objects.filter(id__in=guest_ids)

        for guest in guests_to_check_out:
            guest.check_out = timezone.now()
            new_duration = (guest.check_out - guest.check_in).days
            guest.duration = new_duration
            guest.save()
            guest.revenue.revenue = new_duration * guest.room.suite.price
            guest.revenue.save()
            
            guest.room.room_status = False
            guest.room.save()
            
            Log.objects.create(
                staff=request.user,
                action=f'{request.user} checked out {guest.name} from Room {guest.room.room_number}',
                check_status=False, 
                timestamp=guest.check_out,
                company=request.user.company
            )
        return redirect('dashboard')
    
    return redirect('sign-in')

# Under construction
# -------------------------------------------------
def extend(request):
    # This function will take in a new date that is then saved as the new check out date for a user.
    # The changes will reflect in the guest duration and revenue.
    
    new_time = request.POST.get('new_date')
    guest_id = request.POST.get('guest_id')
    guest = get_object_or_404(Guest, id=guest_id)
    
    guest.check_out=new_time
    new_duration = new_time - guest.check_in
    guest.duration= new_duration
    guest.save()
    guest.revenue.revenue = float(guest.duration) * float(guest.room.suite.price)
    guest.revenue.save()
    
    Log.objects.create(
        staff = request.user,
        action = f'{guest.name} extended checkout to {guest.check_out}',
        check_status = True,
        timestamp = timezone.now(),
        company = request.user.company
    )
    context = {
        
    }
    return render(request, '', context)
# -------------------------------------------------

def analytics(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    top_guests = Guest.objects.filter(company=request.user.company).order_by('-revenue__revenue')[:5]
    guests = Guest.objects.filter(company=request.user.company)
    
    check_ins = CheckIns.objects.filter(time__year=timezone.now().year, company=request.user.company)
    year_dict = {i:0 for i in range(1,13)}
    for check_in in check_ins:
        month = check_in.time.month
        year_dict[month] += 1
    check_in_data = list(year_dict.values())
    # check_in_data = [8,8,8,8,8,15]
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
        
    monthly_revenue = (total_revenue/(timezone.now().month))
    
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
        
    available_rooms = Room.objects.filter(room_status=False,
                                          company=request.user.company)
    
    context = {
        'available_rooms':available_rooms,
        'check_in_data':check_in_data, 
        'guests':Guest.objects.filter(company=request.user.company), 
        'top_guests':top_guests, 
        'check_in_rate':check_in_rate, 
        'guest_growth':guest_growth, 
        'total_revenue':float(total_revenue), 
        'monthly_revenue':monthly_revenue, 
        'revenue_growth':revenue_growth, 
        'page_name':'Analytics'
    }
    return render(request, 'analytics.html', context)

def download_analytics_csv(request):
    
    guests = Guest.objects.filter(company=request.user.company)
    
    checkins = CheckIns.objects.filter(company=request.user.company)
    
    rooms = Room.objects.filter(company=request.user.company)
    
    years_set = set()
    for guest in guests:
        years_set.add(guest.check_in.year)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Report.csv"'

    writer = csv.writer(response)
    
    def calculate_rev(year,month=None,guests=guests):
        if month is not None:
            total = 0
            for guest in guests:
                if guest.check_in.year == year and guest.check_in.month == month:
                    total+=guest.revenue.revenue
            return round(total,1)
        
        total = 0
        for guest in guests:
            if guest.check_in.year == year:
                total+=guest.revenue.revenue
        return round(total,1)
        
        
    def total_guests(year,month=None,guests=guests):
        if month is not None:
            total = 0
            for guest in guests:
                if guest.check_in.year == year and guest.check_in.month == month:
                    total+=1
            return round(total,1)
        
        total = 0
        for guest in guests:
            if guest.check_in.year == year:
                total+=1
        return round(total,1)
    
    def avg_daily_revenue(year,month=None,guests=guests):
        if month is not None:
            return round(calculate_rev(year,month,guests=guests)/calendar.monthrange(year,month)[1],1)
        
        return round(calculate_rev(year,month=None,guests=guests)/365,1)
    
    def occupancy_rate(year,month=None,checkins=checkins,rooms=rooms):
        if month is not None:
            total = 0
            for checkin in checkins:
                if checkin.time.year == year and checkin.time.month == month:
                    total+=1
            return round(total/rooms.count(),1)
        
        total = 0
        for checkin in checkins:
            if checkin.time.year == year:
                total+=1
        return round(total/rooms.count(),1)
    
    def rev_per_room(year,month=None,guests=guests,rooms=rooms):
        if month is not None:
            return calculate_rev(year,month,guests=guests)/rooms.count()
        
        return calculate_rev(year,month=None,guests=guests)/rooms.count()
    
    for year_ in years_set:
         writer.writerow([year_])  # CSV Header
         writer.writerow(['Month','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Total'])
         
         writer.writerow(['Revenue (Naira)',calculate_rev(year_,month=1),calculate_rev(year_,month=2),calculate_rev(year_,month=3),calculate_rev(year_,month=4),calculate_rev(year_,month=5),calculate_rev(year_,month=6),calculate_rev(year_,month=7),calculate_rev(year_,month=8),calculate_rev(year_,month=9),calculate_rev(year_,month=10),calculate_rev(year_,month=11),calculate_rev(year_,month=12),calculate_rev(year_,month=None)])
         
         writer.writerow(['Total Guests',total_guests(year_,month=1),total_guests(year_,month=2),total_guests(year_,month=3),total_guests(year_,month=4),total_guests(year_,month=5),total_guests(year_,month=6),total_guests(year_,month=7),total_guests(year_,month=8),total_guests(year_,month=9),total_guests(year_,month=10),total_guests(year_,month=11),total_guests(year_,month=12),total_guests(year_,month=None)])
         
         writer.writerow(['Average Daily Revenue (Naira)',avg_daily_revenue(year_,month=1),avg_daily_revenue(year_,month=2),avg_daily_revenue(year_,month=3),avg_daily_revenue(year_,month=4),avg_daily_revenue(year_,month=5),avg_daily_revenue(year_,month=6),avg_daily_revenue(year_,month=7),avg_daily_revenue(year_,month=8),avg_daily_revenue(year_,month=9),avg_daily_revenue(year_,month=10),avg_daily_revenue(year_,month=11),avg_daily_revenue(year_,month=12),avg_daily_revenue(year_,month=None)])
         
         writer.writerow(['Occupancy Rate',occupancy_rate(year_,month=1),occupancy_rate(year_,month=2),occupancy_rate(year_,month=3),occupancy_rate(year_,month=4),occupancy_rate(year_,month=5),occupancy_rate(year_,month=6),occupancy_rate(year_,month=7),occupancy_rate(year_,month=8),occupancy_rate(year_,month=9),occupancy_rate(year_,month=10),occupancy_rate(year_,month=11),occupancy_rate(year_,month=12),occupancy_rate(year_,month=None)])
         
         writer.writerow(['Revenue Per Available Room',rev_per_room(year_,month=1),rev_per_room(year_,month=2),rev_per_room(year_,month=3),rev_per_room(year_,month=4),rev_per_room(year_,month=5),rev_per_room(year_,month=6),rev_per_room(year_,month=7),rev_per_room(year_,month=8),rev_per_room(year_,month=9),rev_per_room(year_,month=10),rev_per_room(year_,month=11),rev_per_room(year_,month=12),rev_per_room(year_,month=None)])
         
         writer.writerow([''])

    return response

# For Demos
def sign_in_test(request):
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
        return render(request, 'pages-sign-in-test.html', context)
    
def landing(request):
    return render(request, 'landing.html')