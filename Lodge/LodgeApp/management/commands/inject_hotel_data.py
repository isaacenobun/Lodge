import random
from django.core.management.base import BaseCommand
from LodgeApp.models import Company, Subscriptions, Suite, Room, Staff, Revenue, Guest, GuestHistory, Log, CheckIns
from django.utils import timezone
import datetime
from datetime import timedelta

class Command(BaseCommand):
    help = 'Inject custom data into the database'

    def handle(self, *args, **kwargs):
        # Create Company
        company = Company.objects.create(name='Test Company')

        # Create Staff member
        staff = Staff.objects.create_user(email='test@gmail.com', username='Tester', password='1234', company=company, owner=True)

        # Create Suites
        suites = []
        suite_types = ['Executive', 'Deluxe', 'Standard']
        suite_prices = [45000.00, 35000.00, 25000.00]
        for suite_type, suite_price in zip(suite_types, suite_prices):
            suite = Suite.objects.create(company=company, type=suite_type, price=suite_price)
            suites.append(suite)

        # Create Rooms
        rooms = []
        for suite in suites:
            num_rooms = random.randint(5, 10)
            for i in range(num_rooms):
                room_tag = f'{suite.type[:3]}-{i+1}'
                room = Room.objects.create(suite=suite, company=company, room_tag=room_tag)
                rooms.append(room)

        # Generate data for one year
        start_date = timezone.make_aware(timezone.datetime(2024, 1, 1))
        end_date = timezone.now()
        dates_list = []
        
        current_date = start_date
        while current_date <= end_date:
            dates_list.append(current_date)
            current_date += datetime.timedelta(days=1)
        
        for date in dates_list:
            for i in range(random.randint(0, 1),random.randint(2, 4)):
                # Generate Guest
                room = random.choice(rooms)
                check_in=date
                check_out=date + timedelta(days=random.randint(1, 5))
                duration=(check_out - check_in).days
                revenue = Revenue.objects.create(
                    revenue = float(duration) * float(room.suite.price),
                    company=company
                )
                guest = Guest.objects.create(company=company, 
                                            name=f'Guest {random.randint(1,1000)}', 
                                            email=f'guest{random.randint(1, 1000)}@gmail.com', 
                                            number=random.randint(1000000000, 9999999999),
                                            room = room,
                                            check_in=check_in,
                                            staff=staff,
                                            check_out=date + timedelta(days=random.randint(1, 5)),
                                            duration=duration,
                                            revenue=revenue
                )
                
                Log.objects.create(staff=staff, 
                                action='Checked in guest', 
                                check_status=True, 
                                timestamp=check_in, 
                                company=company
                                )
                Log.objects.create(staff=staff, 
                                action='Checked out guest', 
                                check_status=False, 
                                timestamp=check_out,
                                company=company
                                )
                CheckIns.objects.create(company=company, 
                                        time=check_in
                                        )
        # Create Subscription
        Subscriptions.objects.create(company=company, amount=300000,start_date=start_date, due_date=start_date + timedelta(days=30))
        
        self.stdout.write(self.style.SUCCESS('Successfully injected custom data into the database'))
