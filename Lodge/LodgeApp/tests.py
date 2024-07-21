from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.utils import timezone
from .models import Staff, Company, Suite, Room, Subscriptions, Guest, Log

User = get_user_model()

class SignUpViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('sign-up')
    
    def test_sign_up_authenticated_user_with_company_redirects_to_dashboard(self):
        user = Staff.objects.create_user(username='testuser', email='test@example.com', password='password')
        company = Company.objects.create(name='Test Company')
        user.company = company
        user.save()
        
        self.client.login(username='test@example.com', password='password')
        response = self.client.get(self.url)
        
        self.assertRedirects(response, reverse('dashboard'))
    
    def test_sign_up_authenticated_user_without_company_redirects_to_onboarding(self):
        user = Staff.objects.create_user(username='testuser', email='test@example.com', password='password')
        
        self.client.login(username='test@example.com', password='password')
        response = self.client.get(self.url)
        
        self.assertRedirects(response, reverse('onboarding'))
    
    def test_sign_up_post_existing_email(self):
        Staff.objects.create_user(username='testuser', email='test@example.com', password='password')
        
        response = self.client.post(self.url, {
            'username': 'newuser',
            'email': 'test@example.com',
            'password': 'newpassword'
        })
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Email already exists. Please choose a different email or sign in.')
    
    def test_sign_up_post_success(self):
        response = self.client.post(self.url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        })
        
        self.assertRedirects(response, reverse('onboarding'))
        new_user = Staff.objects.get(email='newuser@example.com')
        self.assertTrue(new_user.check_password('newpassword'))
        self.assertTrue(new_user.is_superuser)
        self.assertFalse(new_user.is_staff)

class OnboardingViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('onboarding')
        self.user = Staff.objects.create_user(username='testuser', email='test@example.com', password='password')
    
    def test_onboarding_not_authenticated_redirects_to_sign_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('sign-in'))
    
    def test_onboarding_authenticated_user_with_company_redirects_to_dashboard(self):
        company = Company.objects.create(name='Test Company')
        self.user.company = company
        self.user.save()
        
        self.client.login(username='test@example.com', password='password')
        response = self.client.get(self.url)
        
        self.assertRedirects(response, reverse('dashboard'))
    
    def test_onboarding_post_success(self):
        self.client.login(username='test@example.com', password='password')
        response = self.client.post(self.url, {
            'company_name': 'New Company',
            'suite_type_1': 'Deluxe',
            'suite_price_1': '2000',
            'suite_rooms_1': '2'
        })
        
        company = Company.objects.get(name='New Company')
        self.assertEqual(self.user.company, company)
        self.assertTrue(self.user.owner)
        self.assertRedirects(response, reverse('dashboard'))

class SignInViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('sign-in')
        self.user = Staff.objects.create_user(username='testuser', email='test@example.com', password='password')
    
    def test_sign_in_authenticated_user_with_company_redirects_to_dashboard(self):
        company = Company.objects.create(name='Test Company')
        self.user.company = company
        self.user.save()
        
        self.client.login(username='test@example.com', password='password')
        response = self.client.get(self.url)
        
        self.assertRedirects(response, reverse('dashboard'))
    
    def test_sign_in_authenticated_user_without_company_redirects_to_onboarding(self):
        self.client.login(username='test@example.com', password='password')
        response = self.client.get(self.url)
        
        self.assertRedirects(response, reverse('onboarding'))
    
    def test_sign_in_post_invalid_email(self):
        response = self.client.post(self.url, {
            'email': 'invalid@example.com',
            'password': 'password'
        })
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Staff with invalid@example.com does not exist')
    
    def test_sign_in_post_invalid_password(self):
        response = self.client.post(self.url, {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid password')
    
    def test_sign_in_post_success(self):
        response = self.client.post(self.url, {
            'email': 'test@example.com',
            'password': 'password'
        })
        
        self.assertRedirects(response, reverse('dashboard'))
