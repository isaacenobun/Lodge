from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class Subscriptions(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    start_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    payment_status = models.BooleanField(default=False)

class Suite(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'{self.type} - {self.company.name}'
    
class Room(models.Model):
    suite = models.ForeignKey(Suite, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    room_tag = models.CharField(max_length=50)
    room_status = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Room {self.room_tag} - {self.suite.type}'

class Staff(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(max_length=50, blank=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
class Revenue(models.Model):
    revenue = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.revenue}'

class Guest(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    number = models.BigIntegerField()
    room  = models.ForeignKey(Room, on_delete=models.PROTECT,blank=True)
    check_in = models.DateTimeField(auto_now_add=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    check_out = models.DateTimeField()
    revenue = models.ForeignKey(Revenue, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    duration = models.BigIntegerField()
    
    def __str__(self):
        return self.name
    
class GuestHistory(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='history')
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    number = models.CharField(max_length=50)
    room  = models.ForeignKey(Room, on_delete=models.PROTECT,blank=True)
    check_in = models.DateTimeField()
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    check_out = models.DateTimeField()
    revenue = models.ForeignKey(Revenue, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    duration = models.BigIntegerField()
    
    def __str__(self):
        return f'{self.guest}'
    
class Log(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    action = models.CharField(max_length=300, blank=True)
    check_status = models.BooleanField(default=False)
    timestamp = models.DateTimeField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.action}'
    
class CheckIns(models.Model):
    time = models.DateField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)