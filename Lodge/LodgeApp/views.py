from .imports import *

# Production Ready ✅
def sign_up(request):
    if request.user.is_authenticated:
        if request.user.company is not None:
            return redirect('dashboard')
        else:
            return redirect('onboarding')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        if Staff.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please choose a different email or sign in.')
        else:
            try:
                with transaction.atomic():
                    new_user = Staff.objects.create(
                        username=username,
                        email=email,
                    )
                    
                    new_user.set_password(password)
                    new_user.is_superuser = True
                    new_user.is_staff = False
                    new_user.save()
                    
                    new_user = authenticate(
                        request, 
                        email=email, 
                        password=password
                    )
                    if new_user is not None:
                        login(request, new_user)
                        return redirect('onboarding')
                    else:
                        messages.error(request, 'Authentication failed. Please try logging in with your new credentials.')
            except IntegrityError:
                messages.error(request, 'An error occurred while creating your account. Please try again.')
                return redirect('sign-up')
            except Exception:
                messages.error(request, 'An unexpected error occurred. Please try again.')
                return redirect('sign-up')

    context = {'page_name': 'Sign Up'}
    return render(request, 'pages-sign-up.html', context)

# Production Ready ✅
def onboarding(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    if request.user.is_authenticated and request.user.company is not None:
        return redirect('dashboard')
    
    if request.method == 'POST':
        company_name = request.POST.get('company_name').strip()
        
        if not company_name:
            messages.error(request, 'Company name is required.')
            return redirect('onboarding')
        
        suite_type_pattern = re.compile(r'suite_type_\d+')
        suite_types = [value.strip() for key, value in request.POST.items() if suite_type_pattern.match(key)]
        
        if len(set(suite_types))!=len(suite_types):
            messages.error(request, 'Please select unique suite types.')
            return redirect('onboarding')
        
        suite_price_pattern = re.compile(r'suite_price_\d+')
        suite_prices = [value.strip() for key, value in request.POST.items() if suite_price_pattern.match(key)]
        
        suite_rooms_pattern = re.compile(r'suite_rooms_\d+')
        suite_rooms = [value.strip() for key, value in request.POST.items() if suite_rooms_pattern.match(key)]
        
        if len(suite_types) != len(suite_prices) or len(suite_types) != len(suite_rooms):
            messages.error(request, 'Mismatch in number of suite types, prices, and rooms.')
            return redirect('onboarding')
        
        try:
            with transaction.atomic():
                company = Company.objects.create(name=company_name)

                for i in range(len(suite_types)):
                    suite_type = suite_types[i]
                    suite_price = suite_prices[i]
                    suite_room = suite_rooms[i]
                    
                    try:
                        suite_price = float(suite_price)
                        suite_room = int(suite_room)
                    except ValueError:
                        messages.error(request, 'Invalid price or room count.')
                        return redirect('onboarding')
                    
                    new_suite = Suite.objects.create(
                        company=company,
                        type=suite_type,
                        price=suite_price
                    )
                    
                    for room_tag in range(1,suite_room+1):
                        Room.objects.create(
                            suite=new_suite,
                            company=company,
                            room_tag=f"Room {room_tag}"
                        )
                
                owner = request.user
                owner.company = company
                owner.owner = True
                owner.save()
                
                no_of_rooms = Room.objects.filter(company=company).count()
                no_of_rooms = max(no_of_rooms, 20)
                
                subscription = Subscriptions.objects.create(
                    company=company,
                    amount=no_of_rooms * 1000,
                    due_date=timezone.now() + relativedelta(months=1)
                )
                
                start_date = subscription.start_date.strftime('%a %d %b %Y, %I:%M%p')
                due_date = subscription.due_date.strftime('%a %d %b %Y, %I:%M%p')
                
                mail = (f'Hello Isaac,\n\n{owner.username} from {owner.company} just subscribed to LodgeIt.\n'
                        f'Please send an invoice to {owner.email} as soon as possible.\n\n'
                        f'Invoice details\nClient: {owner.username}\nCompany: {owner.company}\n'
                        f'Subscription: ₦{subscription.amount}\nStart Date: {start_date}\nDue Date: {due_date}')
                
                # send_mail(
                #     'New LodgeIt Subscription',
                #     mail,
                #     'lodgeitng@gmail.com',
                #     ['Isaacenobun@gmail.com', 'etinosa.enobun@gmail.com', 'martyminaj@gmail.com']
                # )
                
                messages.success(request, f"An invoice for a Subscription fee of ₦{subscription.amount} has been sent to {owner.email}. Please pay within two days.")
                
                return redirect('dashboard')
        
        except:
            messages.error(request, 'An unexpected error occurred. Please try again.')
            return redirect('onboarding')
    
    return render(request, 'onboarding.html')

# Production Ready ✅
def sign_in(request):
    if request.user.is_authenticated:
        if request.user.company is not None:
            return redirect('dashboard')
        else:
            return redirect('onboarding')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not email or not password:
            messages.warning(request, 'Both email and password are required.')
            return redirect('sign-in')

        try:
            staff = Staff.objects.get(email=email.lower())
        except Staff.DoesNotExist:
            messages.warning(request, f"Staff with {email} does not exist")
            return redirect('sign-in')

        staff = authenticate(request, email=email.lower(), password=password)

        if staff is not None:
            login(request, staff)
            return redirect('dashboard')
        else:
            messages.warning(request, "Invalid password")
            return redirect('sign-in')
    
    context = {'page_name':'Sign in'}
    return render(request, 'pages-sign-in.html', context)

# Production Ready ✅
def sign_out(request):
    logout(request)
    return redirect('sign-in')

# Production Ready ✅
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    if request.user.is_authenticated and request.user.company is None:
        return redirect('onboarding')
    
    company = request.user.company
    
    try:
        logs = Log.objects.filter(
            company=request.user.company
            ).order_by('-id')[:5]
        active_guests = Guest.objects.filter(check_out__gte=timezone.now(),
                                            company=company)
        total_guests = Guest.objects.filter(company=company).count()
        available_rooms = Room.objects.filter(room_status=False,
                                            company=company)
        
        returning_guests = Guest.objects.filter(company=company, check_out__lte=timezone.now())
    except:
        messages.error(request, 'An unexpected error occurred while fetching data. Please try again later.')
        return redirect('logout')

    context = {
        'now':timezone.now(),
        'active_guests': active_guests,
        'total_guests': total_guests,
        'staff': request.user,
        'logs': logs,
        'available_rooms': available_rooms,
        'page_name':'Home',
        'returning_guests': returning_guests
    }
    return render(request, 'index.html', context)

# Production Ready ✅
def rooms(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    if request.user.company is None:
        return redirect('onboarding')
    
    company = request.user.company
    
    try:
        suite_types = Suite.objects.filter(company=request.user.company).values_list('type', flat=True).distinct()
        
        suite_types_dict = {}
        for suite_type in suite_types:
            suite_rooms = Room.objects.filter(suite__type=suite_type, company=company)
            suite_types_dict[suite_type] = suite_rooms
        
        # suite_types_dict['All'] = Room.objects.filter(company=company)
        
        guests = Guest.objects.filter(check_out__gt=timezone.now(),
                                    company=company
                                    )
        room_guest_mapping = {guest.room.id: guest for guest in guests}
        
        available_rooms = Room.objects.filter(room_status=False,
                                            company=company)
        returning_guests = Guest.objects.filter(company=company, check_out__lte=timezone.now())
        
        context = {
            'available_rooms':available_rooms,
            'suite_types': suite_types_dict,
            'room_guest_mapping': room_guest_mapping,
            'check_out_url': reverse('check-out'),
            'check_in_url': reverse('check-in'),
            'page_name':'Rooms',
            'returning_guests':returning_guests
        }
        
        return render(request, 'room-carousel.html', context)
    except:
        messages.error(request, 'An unexpected error occurred while retrieving data. Please try again later.')
        return redirect('logout')

# Production Ready ✅
def edit_rooms(request):
    room_ids = request.POST.getlist('rooms')
    room_tags = request.POST.getlist('room_tags')
    
    if len(room_ids) != len(room_tags):
        messages.error(request, "There was an error. Try again.")
        return redirect('rooms')
    try:
        rooms = Room.objects.filter(id__in=room_ids)
        if len(rooms) != len(room_ids):
            messages.error(request, "There was an error. Try again.")
            return redirect('rooms')
        
        for room, room_tag in zip(rooms, room_tags):
            if not room_tag:
                messages.warning(request, f"A room tag cannot be empty.")
                return redirect('rooms')
            else:
                room.room_tag = room_tag
                room.save()
        messages.success(request, f"Room tags edited successfully")
        return redirect('rooms')
    except:
        messages.error(request, "There was an error. Try again.")
        return redirect('rooms')

# Production Ready ✅
def extend(request):
    new_duration = request.POST.get('new_duration')
    
    if int(new_duration) < 1:
        messages.warning(request, f"You can't entend by 0 days")
        return redirect('rooms')
    
    try:
        with transaction.atomic():
            guest_id = request.POST.get('guest_id')
            guest = get_object_or_404(Guest, id=guest_id)
            
            guest.check_out= guest.check_out + timedelta(days=int(new_duration))
            guest.duration= int(new_duration) + (guest.check_out - guest.check_in).days
            guest.save()
            
            formatted_checkout = guest.check_out.strftime('%a %d %b %Y, %I:%M%p')
            
            guest.revenue.revenue = float(guest.revenue.revenue) + float(guest.duration) * float(guest.room.suite.price)
            guest.revenue.save()
            
            Log.objects.create(
                staff = request.user,
                action = f'{guest.name} extended checkout by {int(new_duration)} days to {formatted_checkout}',
                check_status = True,
                timestamp = timezone.now(),
                company = request.user.company
            )
            
            messages.success(request, f"{guest.name}'s check out date was extended by {new_duration} days to {formatted_checkout}")
    except:
        messages.error(request, "There was an error. Try again.")
        return redirect('rooms')
    
    return redirect('rooms')

# Production Ready ✅
def history(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    if request.user.is_authenticated and request.user.company is None:
        return redirect('onboarding')
    
    guests = Guest.objects.filter(company=request.user.company)
    available_rooms = Room.objects.filter(room_status=False,
                                          company=request.user.company)
    
    returning_guests = Guest.objects.filter(company=request.user.company, check_out__lte=timezone.now())
    
    context = {
        'available_rooms':available_rooms,
        'guests': guests,
        'returning_guests':returning_guests, 
        'page_name':'History'
    }
    return render(request, 'guest-history.html', context)

# Production Ready ✅
def download_history_csv(request):
    
    guests = Guest.objects.filter(company=request.user.company)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Guest List.csv"'

    writer = csv.writer(response)
    
    writer.writerow(['#', 'Name', 'Email', 'Phone Number', 'Suite', 'Room', 'Check-in Date', 'Check-Out Date'])  # CSV Header
    
    count = 1
    for guest in guests:
        suite_type = getattr(getattr(guest.room, 'suite', None), 'type', 'Deleted')
        room_tag = getattr(guest.room, 'room_tag', 'Deleted')
        writer.writerow([
            count,
            guest.name,
            guest.email,
            guest.number,
            suite_type,
            room_tag,
            guest.check_in.strftime('%a %d %b %Y, %I:%M%p'),
            guest.check_out.strftime('%a %d %b %Y, %I:%M%p')
        ])
        count += 1

    return response

# Production Ready ✅
def logs(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    if request.user.is_authenticated and request.user.company is None:
        return redirect('onboarding')
    
    available_rooms = Room.objects.filter(room_status=False,
                                          company=request.user.company)
    
    # Group logs
    logs = Log.objects.filter(company=request.user.company).order_by('-id')
    
    annotated_logs = logs.annotate(
        year=ExtractYear('timestamp'),
        month=ExtractMonth('timestamp'),
        day=ExtractDay('timestamp')
    )
    
    logs_by_year_month_day = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    
    for log in annotated_logs:
        month_name = calendar.month_name[log.month]
        logs_by_year_month_day[log.year][month_name][log.day].append(log)
        
    logs_structure = {
        year: {
            month: {
                day: list(day_logs) for day, day_logs in days.items()
            } for month, days in months.items()
        } for year, months in logs_by_year_month_day.items()
    }
    
    guests = Guest.objects.filter(company=request.user.company)
    
    returning_guests = Guest.objects.filter(company=request.user.company, check_out__lte=timezone.now())
    
    context={
        'available_rooms':available_rooms,
        'logs':logs,
        'page_name':'Logs',
        'guests':guests,
        'returning_guests':returning_guests,
        'logs_structure':logs_structure,
    }
    
    return render(request, 'logs.html', context)

# Production Ready ✅
def download_logs_csv(request):
    
    logs = Log.objects.filter(company=request.user.company).order_by('-id')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Logs.csv"'

    writer = csv.writer(response)
    
    writer.writerow(['#', 'Log', 'Time', 'Staff on duty'])  # CSV Header
    
    count=1
    for log in logs:
        writer.writerow([
            count, 
            log.action, 
            log.timestamp.strftime('%a %d %b %Y, %I:%M%p'), 
            log.staff
            ])
        count+=1

    return response

# Production Ready ✅
def staff_add(request):
    def validate_email(email):
        email_regex = re.compile(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        )
        return re.match(email_regex, email) is not None
    
    username = request.POST.get('username').strip()
    email = request.POST.get('email').strip()
    password = request.POST.get('password')
    admin_status = request.POST.get('admin')
    
    if not username:
            messages.error(request, 'Username is required.')
            return redirect('settings')
        
    if not validate_email(email):
            messages.error(request, 'Invalid email address. Please enter a valid email address.')
            return redirect('settings')
        
    if not password:
            messages.warning(request, 'You did not put in a password')
            return redirect('settings')
    
    if Staff.objects.filter(email=email.lower()).exists():
        messages.error(request, 'Email already exists. Please choose a different email.')
        return redirect('settings')
    else:
        try:
            with transaction.atomic():
                new_user = Staff.objects.create(
                    username=username,
                    email=email.lower(),
                    password=password,
                    company=request.user.company
                )
                
                if admin_status:
                    new_user.owner = True
                
                new_user.set_password(password)
                new_user.is_superuser = True
                new_user.is_staff = False
                new_user.save()
                
                # Send mail to added staff
                mail = (f'Hello {new_user.username},\n\nHere are your LodgeIt login details for {request.user.company}\n'
                        f'\nEmail: {new_user.email}\nPassword: {password.lower()}\n\nLog in here: www.lodgeitng.com/sign-in')
                
                # send_mail(
                #     'Your LodgeIt Login Details',
                #     mail,
                #     'lodgeitng@gmail.com',
                #     [new_user.email]
                # )
                
                messages.success(request, f"Staff added successfully")
                
                return redirect('settings')
        except:
            messages.error(request, 'An error occurred while creating a new staff account. Please try again.')
            return redirect('settings')
            
# Production Ready ✅
def staff_edit(request):
    def validate_email(email):
        email_regex = re.compile(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        )
        return re.match(email_regex, email) is not None
    
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password')
        
        if not username:
            messages.error(request, 'Username is required.')
            return redirect('settings')
        
        if not validate_email(email):
            messages.error(request, 'Invalid email address. Please enter a valid email address.')
            return redirect('settings')
        
        if not password:
            messages.warning(request, 'You did not put in a password')
            return redirect('settings')
        
        admin_status = request.POST.get('admin')
        
        if admin_status:
            admin_status = True
        else:
            admin_status = False
        
        try:
            with transaction.atomic():
                staff = Staff.objects.get(id=staff_id)
                
                if staff == request.user:
                    messages.error(request, 'You cannot edit your own account')
                    return redirect('settings')
                
                staff.username = username
                staff.email = email.lower()
                staff.set_password(password)
                staff.owner = admin_status
                staff.save()
                messages.success(request, 'Staff edited successfully')
                return redirect('settings')
        except:
            messages.error(request, 'An error occurred while editing the staff account. Please try again.')
            return redirect('settings')

# Production Ready ✅   
def delete_suite(request):
    if request.method == 'POST':
        suite_id = request.POST.get('suite_id')
        suite = Suite.objects.get(id=suite_id)
        
        try:
            with transaction.atomic():
                rooms = Room.objects.filter(suite=suite)
                for room in rooms:
                    guests = Guest.objects.filter(room=room)
                    if guests:
                        for guest in guests:
                            if guest.check_out >= timezone.now():
                                messages.error(request, 'Please check out all the guests in this suite first')
                                return redirect('settings')
                        
                suite_type = suite.type
                Log.objects.create(
                            staff=request.user,
                            action=f'{request.user} deleted the {suite_type} Suite',
                            check_status=False, 
                            timestamp=timezone.now(),
                            company=request.user.company
                        )
                suite.delete()
        except:
            messages.error(request, 'An error occurred while deleting the suite. Please try again.')
            return redirect('settings')
        
        messages.success(request, f"The {suite_type} Suite has been successfully deleted.")
        return redirect('settings')

# Production Ready ✅    
def settings(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    if request.user.is_authenticated and request.user.company is None:
        return redirect('onboarding')
    
    if request.method == 'POST':
        
        suites = Suite.objects.filter(company=request.user.company)
        rooms = Room.objects.filter(company=request.user.company)
        
        with transaction.atomic():
            new_company_name = request.POST.get('input_0')
            company = request.user.company
            if new_company_name:
                company.name=new_company_name.strip()
                company.save()
        
            suite_ids = request.POST.getlist('input_id')
            edit_suite_names = request.POST.getlist('input_1')
            edit_suite_prices = request.POST.getlist('input_3')
            edit_no_of_rooms = request.POST.getlist('input_2')
        
            for suite_id, new_name, new_price, new_no_of_rooms in zip(suite_ids, edit_suite_names, edit_suite_prices, edit_no_of_rooms):
                try:
                    suite = suites.get(id=suite_id)
                    
                    suite.type = new_name.strip()
                    if suites.exclude(id=suite_id).filter(type=suite.type).exists():
                        messages.error(request, f'Make sure the Suite names are unique.')
                        return redirect('settings')
                    
                    try:
                        suite.price = float(new_price.replace(',', ''))
                    except ValueError:
                        messages.error(request, f'Please enter a valid Suite price for the {suite.type} Suite')
                        return redirect('settings')
                    suite.save()
                    
                    current_rooms = rooms.filter(suite=suite).count()
                    try:
                        new_no_of_rooms = int(new_no_of_rooms)
                    except ValueError:
                        messages.error(request, f'Please enter a valid number of rooms for the {suite.type} Suite.')
                        return redirect('settings')
                    if new_no_of_rooms > current_rooms:
                        for i in range(current_rooms, new_no_of_rooms):
                            Room.objects.create(suite=suite, company=suite.company, room_tag=f'New room {i + 1}')
                    elif new_no_of_rooms < current_rooms:
                        rooms_to_remove = Room.objects.filter(suite=suite)[new_no_of_rooms:]
                        rooms_to_remove.delete()
                        
                except:
                    messages.error(request, f"There was a problem")
                    return redirect('settings')
        
            new_suites = request.POST.getlist('input_new')
            if new_suites:
                itr = iter(new_suites)
                
                for row in range(0,int(len(new_suites)/3)):
                    
                    try:
                        new_name = next(itr).strip()
                        if suites.filter(type=new_name).exists():
                            messages.error(request, f'Make sure the Suite names are unique.')
                            return redirect('settings')
                        new_suite = Suite.objects.create(
                        company=request.user.company,
                        type=new_name,
                        price=float(0),
                    )
                        try:
                            rooms_no = int(next(itr))
                        except ValueError:
                            messages.error(request, f'Please enter a valid number of rooms.')
                            return redirect('settings')
                        for room_tag in range(1,rooms_no+1):
                            new_room = Room.objects.create(
                                suite=new_suite,
                                company=request.user.company,
                                room_tag="Room "+str(room_tag)
                            )
                        
                        try:   
                            new_suite.price= float(next(itr))
                        except ValueError:
                            messages.error(request, f'Please enter valid Suite prices')
                            return redirect('settings')
                        new_suite.save()
                        
                    except:
                        messages.error(request, f"There was a problem")
                        return redirect('settings')
                        
            messages.success(request, f"Changes have been made successfully")
            return redirect('settings')
    
    company = request.user.company
    
    suites = Suite.objects.filter(company=company)
    
    suite_room_types_vacants={}
    for suite in suites:
        suite_room_types_vacants[suite] = [Room.objects.filter(suite=suite).count(),suite.price,[Room.objects.filter(suite=suite,room_status=False)]]
    print (suite_room_types_vacants)
    
    user = request.user
    owners = Staff.objects.filter(company = company, owner=True)
    staffs = Staff.objects.filter(company = company, is_active=True)
    returning_guests = Guest.objects.filter(company=company, check_out__lte=timezone.now())
    subscription = Subscriptions.objects.filter(company=company).order_by('-due_date')[0]
    
    context = {
        'suite_room_types_vacants':suite_room_types_vacants,
        'company':company,
        'user':user,
        'owners':owners,
        'staffs':staffs,
        'page_name':'Settings',
        'returning_guests':returning_guests,
        'subscription':subscription
    }
    return render(request, 'settings.html', context)

# Production Ready ✅ 
def check_in(request):
    if request.method == 'POST':
        
        if not request.POST.get('name_'):
            try:
                with transaction.atomic():
                    guest = Guest.objects.get(name=request.POST.get('name'), company=request.user.company)
                    
                    if guest.check_out>timezone.now():
                        messages.error(request, f"{guest.name} is already checked in.")
                        return redirect('dashboard')

                    # Create GuestHistory entry for the existing guest
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
                
                    # Update current record
                    room_id = request.POST.get('room')
                    room = get_object_or_404(Room, id=room_id)
                    
                    duration = request.POST.get('duration')
                    revenue = float(duration) * float(room.suite.price)
                    revenue = Revenue.objects.create(
                        revenue = revenue,
                        company = request.user.company
                    )
                    check_out = timezone.now() + timedelta(days=int(duration))
                    
                    guest.room = room
                    guest.check_in = timezone.now()
                    guest.staff = request.user
                    guest.check_out=check_out
                    guest.revenue = revenue
                    guest.duration = duration
                    
                    guest.save()

                    room.room_status = True
                    room.save()
                    
                    Log.objects.create(
                        staff=request.user,
                        action=f'{request.user} checked in {guest.name} into {guest.room.room_tag}',
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
                    
                    messages.success(request, f"{guest.name} checked in successfully")

                    return redirect('dashboard')
            
            except:
                with transaction.atomic():
                    
                    # Create new guest instance
                    room_id = request.POST.get('room')
                    room = get_object_or_404(Room, id=room_id)
                    
                    duration = request.POST.get('duration')
                    revenue = float(duration) * float(room.suite.price)
                    revenue = Revenue.objects.create(
                        revenue = revenue,
                        company = request.user.company
                    )
                    check_out = timezone.now() + timedelta(days=int(duration))
                    
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
                        action=f'{request.user} checked in {guest.name} into {guest.room.room_tag}',
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
                    
                    checkIn = CheckIns.objects.create(
                        company=guest.staff.company
                    )
                    
                    checkIn.time = checkIn.time
                    
                    messages.success(request, f"{guest.name} checked in successfully")

                    return redirect('dashboard')
        
        else:
            try:
                with transaction.atomic():
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
                    check_out = timezone.now() + timedelta(days=int(duration))
                    
                    guest.room = room
                    guest.check_in = timezone.now()
                    guest.staff = request.user
                    guest.check_out=check_out
                    guest.revenue = revenue
                    guest.duration = duration
                    
                    guest.save()

                    room.room_status = True
                    room.save()
                    
                    Log.objects.create(
                        staff=request.user,
                        action=f'{request.user} checked in {guest.name} into {guest.room.room_tag}',
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
                    
                    messages.success(request, f"{guest.name} checked in successfully")

                    return redirect('dashboard')
            except Exception as e:
                print (e)
                messages.error(request, 'Error checking in guest')
    
    return redirect('dashboard')

# Production Ready ✅
def check_out(request):
    guest_ids = request.POST.getlist('guest_ids')
    guests_to_check_out = Guest.objects.filter(id__in=guest_ids)

    for guest in guests_to_check_out:
        try:
            with transaction.atomic():
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
                    action=f'{request.user} checked out {guest.name} from {guest.room.room_tag}',
                    check_status=False, 
                    timestamp=guest.check_out,
                    company=request.user.company
                )
        except:
            messages.error(request, 'Error checking out guest')
        
    messages.success(request, f"Check out successful")
        
    return redirect('dashboard')

# Production Ready ✅
def analytics(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    
    if request.user.is_authenticated and request.user.company is None:
        return redirect('onboarding')
    
    guests = Guest.objects.filter(company=request.user.company)
    guest_history = GuestHistory.objects.filter(company=request.user.company)
    analytics_data = []
    
    for guest in guests:
        guest_data = {
            'current': {
                'name': guest.name,
                'email': guest.email,
                'number': guest.number,
                'room': guest.room,
                'check_in': guest.check_in,
                'staff': guest.staff,
                'check_out': guest.check_out,
                'revenue': guest.revenue,
                'company': guest.company,
                'duration': guest.duration,
            },
            'history': []
        }
        
        history = GuestHistory.objects.filter(guest=guest)
        for hist in history:
            guest_data['history'].append({
                'name': hist.name,
                'email': hist.email,
                'number': hist.number,
                'room': hist.room,
                'check_in': hist.check_in,
                'staff': hist.staff,
                'check_out': hist.check_out,
                'revenue': hist.revenue,
                'company': hist.company,
                'duration': hist.duration,
            })
            
        analytics_data.append(guest_data)
    
    current_month = timezone.now().month
    monthly_revenue = guests.filter(check_in__month=current_month).aggregate(Sum('revenue__revenue'))['revenue__revenue__sum'] or 0
    monthly_revenue += guest_history.filter(guest__in=guests, check_in__month=current_month).aggregate(Sum('revenue__revenue'))['revenue__revenue__sum'] or 0
    
    last_month = timezone.now() - timedelta(days=30)
    revenue_last_month = guests.filter(check_in__month=last_month.month).aggregate(Sum('revenue__revenue'))['revenue__revenue__sum'] or 0
    revenue_last_month += guest_history.filter(guest__in=guests, check_in__month=last_month.month).aggregate(Sum('revenue__revenue'))['revenue__revenue__sum'] or 0
    revenue_growth = ((monthly_revenue - revenue_last_month) / revenue_last_month) * 100 if revenue_last_month else 0
    
    check_ins = CheckIns.objects.filter(time__year=timezone.now().year, company=request.user.company)
    year_dict = {i:0 for i in range(1,13)}
    for check_in in check_ins:
        month = check_in.time.month
        year_dict[month] += 1
    check_in_data = list(year_dict.values())
    check_in_rate = float(check_in_data[timezone.now().month-1])/30
    
    top_guests = Guest.objects.filter(company=request.user.company).order_by('-revenue__revenue')[:5]
    
    total_guests_last_month = guests.filter(check_in__month=last_month.month).count()
    guest_growth = ((guests.count()) / total_guests_last_month) * 100 if total_guests_last_month else 0
    
    check_ins_this_month = CheckIns.objects.filter(time__month=timezone.now().month, company=request.user.company).count()
    check_ins_last_month = CheckIns.objects.filter(time__month=last_month.month, company=request.user.company).count()
    if check_ins_last_month > 0:
        guest_growth = ((check_ins_this_month - check_ins_last_month) / check_ins_last_month) * 100
    else:
        guest_growth = 0
    
    guests_data = []
    
    for guest in guests:
        current_revenue = guest.revenue.revenue
        history = guest_history.filter(guest=guest)
        historical_revenue = sum(hist.revenue.revenue for hist in history)
        total_revenue = current_revenue + historical_revenue
        
        guests_data.append({
            'name': guest.name,
            'email': guest.email,
            'number': guest.number,
            'total_revenue': total_revenue,
            'total_days': int(guest.duration) + sum(int(hist.duration) for hist in history),  
        })
    
    top_guests_data = sorted(guests_data, key=lambda x: x['total_revenue'], reverse=True)[:5]
    
    total_revenue = Revenue.objects.filter(company=request.user.company).aggregate(total=Sum('revenue'))['total']
    if total_revenue is None:
        total_revenue = 0
        
    # print (top_guests_data)
    
    available_rooms = Room.objects.filter(room_status=False,
                                          company=request.user.company)
    
    context = {
        'available_rooms':available_rooms,
        'check_in_data':check_in_data, 
        'guests':Guest.objects.filter(company=request.user.company), 
        'returning_guests':Guest.objects.filter(company=request.user.company, check_out__lte=timezone.now()),
        'top_guests':top_guests,
        'top_guests_data':top_guests_data,
        'check_in_rate':check_in_rate, 
        'guest_growth':guest_growth, 
        'total_revenue':float(total_revenue), 
        'monthly_revenue':monthly_revenue, 
        'revenue_growth':revenue_growth, 
        'page_name':'Analytics'
    }
    return render(request, 'analytics.html', context)

# Production Ready ✅
def download_analytics_csv(request):
    
    guests = Guest.objects.filter(company=request.user.company)
    guests_history = GuestHistory.objects.filter(company=request.user.company)
    
    checkins = CheckIns.objects.filter(company=request.user.company)
    
    rooms = Room.objects.filter(company=request.user.company)
    
    years_set = set()
    for checkin in checkins:
        years_set.add(checkin.time.year)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Report.csv"'

    writer = csv.writer(response)
    
    def calculate_rev(year,month=None,guests=guests,guests_history=guests_history):
        if month is not None:
            total = 0
            for guest in guests:
                if guest.check_in.year == year and guest.check_in.month == month:
                    total+=guest.revenue.revenue
            for guest in guests_history:
                if guest.check_in.year == year and guest.check_in.month == month:
                    total+=guest.revenue.revenue
            return round(total,1)
        
        total = 0
        for guest in guests:
            if guest.check_in.year == year:
                total+=guest.revenue.revenue
        for guest in guests_history:
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
    
    def avg_daily_revenue(year,month=None,guests=guests,guests_history=guests_history):
        if month is not None:
            return round(calculate_rev(year,month,guests=guests,guests_history=guests_history)/calendar.monthrange(year,month)[1],1)
        
        return round(calculate_rev(year,month=None,guests=guests,guests_history=guests_history)/365,1)
    
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
    
    def rev_per_room(year,month=None,guests=guests,rooms=rooms,guests_history=guests_history):
        if month is not None:
            return round(calculate_rev(year,month,guests=guests,guests_history=guests_history)/rooms.count(),1)
        
        return round(calculate_rev(year,month=None,guests=guests,guests_history=guests_history)/rooms.count(),1)
    
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

# Production Ready ✅
# For Demos
def sign_in_test(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        staff = Staff.objects.get(email=email)

        staff = authenticate(request, email=email, password=password)
        login(request, staff)
        return redirect('dashboard')
    
    else:
        context = {'page_name':'Sign in'}
        return render(request, 'pages-sign-in-test.html', context)

# Production Ready ✅
def landing(request):
    return render(request, 'landing.html')