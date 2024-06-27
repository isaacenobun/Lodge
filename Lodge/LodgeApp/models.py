from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255, unique=True, default='TestCompany')
    
    def __str__(self):
        return self.name
    
class Suite(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'{self.type} - {self.company.name}'
    
class Room(models.Model):
    suite = models.ForeignKey(Suite, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    room_number = models.CharField(max_length=10)
    room_status = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Room {self.room_number} - {self.suite.type}'

class Staff(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
class Revenue(models.Model):
    revenue = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f'{self.revenue}'

class Guest(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    number = models.IntegerField()
    room  = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField(auto_now_add=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    check_out = models.DateTimeField(null=True,blank=True)
    revenue = models.ForeignKey(Revenue, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name
    
class Log(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    check_in_action = models.CharField(max_length=300, blank=True)
    check_out_action = models.CharField(max_length=300, blank=True)
    check_status = models.BooleanField(default=False)
    timestamp = models.DateTimeField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f'{self.check_in_action} {self.check_out_action}'
    
class CheckIns(models.Model):
    time = models.DateField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.time