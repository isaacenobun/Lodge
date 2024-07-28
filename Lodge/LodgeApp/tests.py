from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.utils import timezone
from .models import Staff, Company, Suite, Room, Subscriptions, Guest, GuestHistory, Log, Revenue
from datetime import timedelta
import csv
class SignUpViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('sign-up')
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
        }

    def test_sign_up_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages-sign-up.html')

    def test_sign_up_post_success(self):
        response = self.client.post(self.url, self.user_data)
        self.assertRedirects(response, reverse('onboarding'))
        user = get_user_model().objects.get(email=self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))

    def test_sign_up_post_email_exists(self):
        get_user_model().objects.create_user(**self.user_data)
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.level_tag == 'error' for message in messages))
        
class OnboardingViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            name = 'company'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            company = self.company
        )
        self.client.login(email='testuser@example.com', password='password123')
        self.url = reverse('onboarding')

    def test_onboarding_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'onboarding.html')

    def test_onboarding_post_success(self):
        data = {
            'company_name': 'Test Company',
            'suite_type_0': 'Suite Type 1',
            'suite_price_0': '1000',
            'suite_rooms_0': '2',
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('dashboard'))

    def test_onboarding_post_missing_company_name(self):
        data = {
            'suite_type_0': 'Suite Type 1',
            'suite_price_0': '1000',
            'suite_rooms_0': '2',
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, self.url)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.level_tag == 'error' for message in messages))

    def test_onboarding_post_invalid_suite_price(self):
        data = {
            'company_name': 'Test Company',
            'suite_type_0': 'Suite Type 1',
            'suite_price_0': 'invalid',
            'suite_rooms_0': '2',
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, self.url)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.level_tag == 'error' for message in messages))

    def test_onboarding_post_non_unique_suite_types(self):
        data = {
            'company_name': 'Test Company',
            'suite_type_0': 'Suite Type 1',
            'suite_price_0': '1000',
            'suite_rooms_0': '2',
            'suite_type_1': 'Suite Type 1',
            'suite_price_1': '2000',
            'suite_rooms_1': '3',
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, self.url)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.level_tag == 'error' for message in messages))
        
class SignInViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('sign-in')
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'password123',
        }
        self.company = Company.objects.create(
            name = 'company'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            company = self.company
        )

    def test_sign_in_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages-sign-in.html')

    def test_sign_in_post_success(self):
        response = self.client.post(self.url, self.user_data)
        self.assertRedirects(response, reverse('dashboard'))

    def test_sign_in_post_invalid_password(self):
        self.user_data['password'] = 'wrongpassword'
        response = self.client.post(self.url, self.user_data)
        self.assertRedirects(response, self.url)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.level_tag == 'warning' for message in messages))

    def test_sign_in_post_nonexistent_user(self):
        self.user_data['email'] = 'nonexistent@example.com'
        response = self.client.post(self.url, self.user_data)
        self.assertRedirects(response, self.url)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.level_tag == 'warning' for message in messages))

class SignOutViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            name = 'company'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            company = self.company
        )
        self.client.login(email='testuser@example.com', password='password123')

    def test_sign_out(self):
        response = self.client.get(reverse('sign-out'))
        self.assertRedirects(response, reverse('sign-in'))
        self.assertFalse('_auth_user_id' in self.client.session)

class DashboardViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            name = 'company'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            company = self.company
        )
        self.client.login(email='testuser@example.com', password='password123')
        self.url = reverse('dashboard')

    def test_dashboard_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_dashboard_redirect_if_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('sign-in'))

class RoomsViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            name = 'company'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            company = self.company
        )
        self.client.login(email='testuser@example.com', password='password123')
        self.url = reverse('rooms')

    def test_rooms_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'room-carousel.html')

    def test_rooms_redirect_if_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('sign-in'))

class EditRoomsViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            name = 'company'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            company = self.company
        )
        self.client.login(email='testuser@example.com', password='password123')
        self.url = reverse('edit-rooms')
        self.suite = Suite.objects.create(company=self.user.company,type='Executive', price=100)

    def test_edit_rooms_post_success(self):
        room = Room.objects.create(room_tag='Room 1', room_status=False, company=self.user.company,suite=self.suite)
        data = {
            'rooms': [room.id],
            'room_tags': ['New Room 1'],
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('rooms'))
        room.refresh_from_db()
        self.assertEqual(room.room_tag, 'New Room 1')

    def test_edit_rooms_post_invalid_data(self):
        response = self.client.post(self.url, {})
        self.assertRedirects(response, reverse('rooms'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.level_tag == 'error' for message in messages))

class ExtendViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            name = 'company'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            company = self.company
        )
        self.client.login(email='testuser@example.com', password='password123')
        self.url = reverse('extend')
        self.suite = Suite.objects.create(company=self.user.company,type='Executive', price=100)

    def test_extend_post_success(self):
        room = Room.objects.create(room_tag='Room 1', room_status=False, company=self.user.company,suite=self.suite)
        extension_data = {
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'room': room.id,
        }
        response = self.client.post(self.url, extension_data)
        self.assertRedirects(response, reverse('rooms'))
        extension = Guest.objects.get(room=room)
        self.assertEqual(extension.check_in.strftime('%Y-%m-%d'), '2024-01-01')
        self.assertEqual(extension.check_out.strftime('%Y-%m-%d'), '2024-12-31')

    def test_extend_post_invalid_data(self):
        response = self.client.post(self.url, {})
        self.assertRedirects(response, reverse('rooms'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.level_tag == 'error' for message in messages))

class HistoryViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            name = 'company'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            company = self.company
        )
        self.client.login(email='testuser@example.com', password='password123')
        self.url = reverse('history')

    def test_history_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'history.html')

    def test_history_redirect_if_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('sign-in'))

class DownloadHistoryCSVViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            name = 'company'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            company = self.company
        )
        self.client.login(email='testuser@example.com', password='password123')
        self.url = reverse('download_history_csv')

    def test_download_history_csv(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')

class LogsViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            name = 'company'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            company = self.company
        )
        self.client.login(email='testuser@example.com', password='password123')
        self.url = reverse('logs')

    def test_logs_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logs.html')

    def test_logs_redirect_if_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('sign-in'))

class DownloadLogsCSVViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            name = 'company'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            company = self.company
        )
        self.client.login(email='testuser@example.com', password='password123')
        self.url = reverse('download-logs-csv')

    def test_download_logs_csv(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')

class StaffAddViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            name = 'company'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            company = self.company
        )
        self.client.login(email='testuser@example.com', password='password123')
        self.url = reverse('staff-add')

    def test_staff_add_post_success(self):
        data = {
            'name': 'New Staff',
            'email': 'staff@example.com',
            'phone_number': '1234567890',
            'role': 'Manager',
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('staff-add'))
        staff = Staff.objects.get(email=data['email'])
        self.assertEqual(staff.name, data['name'])

    def test_staff_add_post_invalid_data(self):
        response = self.client.post(self.url, {})
        self.assertRedirects(response, reverse('staff-add'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.level_tag == 'error' for message in messages))

class StaffEditViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            name = 'company'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            company = self.company
        )
        self.client.login(email='testuser@example.com', password='password123')
        self.staff = Staff.objects.create(
            name='Staff Member',
            email='staff@example.com',
            phone_number='1234567890',
            role='Manager',
            company=self.user.company
        )
        self.url = reverse('staff-edit', kwargs={'staff_id': self.staff.id})

    def test_staff_edit_post_success(self):
        data = {
            'name': 'Updated Staff',
            'email': 'staff@example.com',
            'phone_number': '0987654321',
            'role': 'Supervisor',
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('staff-edit', kwargs={'staff_id': self.staff.id}))
        self.staff.refresh_from_db()
        self.assertEqual(self.staff.name, data['name'])
        self.assertEqual(self.staff.phone_number, data['phone_number'])
        self.assertEqual(self.staff.role, data['role'])

    def test_staff_edit_post_invalid_data(self):
        response = self.client.post(self.url, {})
        self.assertRedirects(response, reverse('staff-edit', kwargs={'staff_id': self.staff.id}))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.level_tag == 'error' for message in messages))

class DeleteSuiteViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            name = 'company'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            company = self.company
        )
        self.client.login(email='testuser@example.com', password='password123')
        self.suite = Suite.objects.create(
            type='Suite Type',
            price=1000,
            company=self.user.company
        )
        self.url = reverse('delete-suite', kwargs={'suite_id': self.suite.id})

    def test_delete_suite(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('rooms'))
        with self.assertRaises(Suite.DoesNotExist):
            Suite.objects.get(id=self.suite.id)

class SettingsViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            name = 'company'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            company = self.company
        )
        self.client.login(email='testuser@example.com', password='password123')
        self.url = reverse('settings')

    def test_settings_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings.html')

    def test_settings_post_success(self):
        data = {
            'company_name': 'New Company Name',
            'contact_name': 'New Contact Name',
            'contact_phone': '1234567890',
            'contact_email': 'newcontact@example.com',
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('settings'))
        self.user.company.refresh_from_db()
        self.assertEqual(self.user.company.company_name, data['company_name'])
        self.assertEqual(self.user.company.contact_name, data['contact_name'])
        self.assertEqual(self.user.company.contact_phone, data['contact_phone'])
        self.assertEqual(self.user.company.contact_email, data['contact_email'])

    def test_settings_post_invalid_data(self):
        response = self.client.post(self.url, {})
        self.assertRedirects(response, reverse('settings'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.level_tag == 'error' for message in messages))

class CheckInViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            name = 'company'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            company = self.company
        )
        self.suite = Suite.objects.create(company=self.user.company,type='Executive', price=100)
        self.room = Room.objects.create(room_tag='101', room_status=False, company=self.user.company,suite=self.suite)
        self.guest = Guest.objects.create(name='John Doe', company=self.user.company)
    
    def test_check_in_existing_guest(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('check_in'), {
            'name': 'John Doe',
            'room': self.room.id,
            'duration': 2,
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.guest.refresh_from_db()
        self.assertEqual(self.guest.room, self.room)
        self.assertEqual(self.guest.duration, 2)
        self.assertTrue(self.guest.check_in <= timezone.now())
        self.assertTrue(self.guest.check_out > timezone.now())
        self.assertTrue(self.room.room_status)
    
    def test_check_in_new_guest(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('check_in'), {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'phone': '1234567890',
            'room': self.room.id,
            'duration': 3,
        })
        self.assertRedirects(response, reverse('dashboard'))
        new_guest = Guest.objects.get(name='Jane Doe')
        self.assertEqual(new_guest.room, self.room)
        self.assertEqual(new_guest.duration, 3)
        self.assertTrue(new_guest.check_in <= timezone.now())
        self.assertTrue(new_guest.check_out > timezone.now())
        self.assertTrue(self.room.room_status)

class CheckOutViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            name = 'company'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            company = self.company
        )
        self.suite = Suite.objects.create(company=self.user.company,type='Executive', price=100)
        self.room = Room.objects.create(room_tag='101', room_status=False, company=self.user.company,suite=self.suite)
        self.guest = Guest.objects.create(name='John Doe', room=self.room, check_in=timezone.now()-timedelta(days=2), check_out=timezone.now()+timedelta(days=1), company=self.user.company)
    
    def test_check_out_guest(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('check_out'), {
            'guest_ids': [self.guest.id],
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.guest.refresh_from_db()
        self.assertTrue(self.guest.check_out <= timezone.now())
        self.assertEqual(self.guest.duration, 2)
        self.assertFalse(self.room.room_status)

class AnalyticsViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            name = 'company'
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            company = self.company
        )
        self.suite = Suite.objects.create(
            company=self.user.company,
            type='Executive', 
            price=100)
        self.room = Room.objects.create(
            room_tag='101', 
            room_status=False, 
            company=self.user.company,
            suite=self.suite
            )
        self.duration=3
        self.revenue = Revenue.objects.create(
            revenue = self.duration * self.suite.price
        )
        self.guest = Guest.objects.create(
            name='John Doe', 
            email='John@mail.com', 
            number= 8065748220,
            room=self.room,
            check_in=timezone.now()-timedelta(days=2), 
            staff=self.user,
            check_out=timezone.now()+timedelta(days=1), 
            duration = 3,
            revenue=self.revenue.revenue,
            company=self.user.company,
            )
        self.guest_history = GuestHistory.objects.create(
            guest=self.guest, 
            name=self.guest.name, 
            email=self.guest.email,
            number=self.guest.number,
            room=self.guest.room,
            check_in=self.guest.check_in, 
            check_out=self.guest.check_out, 
            company=self.user.company
            )
    
    def test_analytics_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Analytics')
        self.assertContains(response, 'John Doe')

class DownloadAnalyticsCSVViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            company = 'company'
        )
        self.suite = Suite.objects.create(company=self.user.company,type='Executive', price=100)
        self.room = Room.objects.create(room_tag='101', room_status=False, company=self.user.company,suite=self.suite)
        self.guest = Guest.objects.create(name='John Doe', room=self.room, check_in=timezone.now()-timedelta(days=2), check_out=timezone.now()+timedelta(days=1), company=self.user.company)
        self.guest_history = GuestHistory.objects.create(guest=self.guest, name=self.guest.name, check_in=self.guest.check_in, check_out=self.guest.check_out, company=self.user.company)
    
    def test_download_analytics_csv(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('download_analytics_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('attachment; filename="Report.csv"', response['Content-Disposition'])
