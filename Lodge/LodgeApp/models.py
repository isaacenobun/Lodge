from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
class Room(models.Model):
    ROOM_NUMBERS = [(str(num),str(num)) for num in range(1,21)]
    
    room_number = models.CharField(max_length=2, choices=ROOM_NUMBERS)
    room_status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.room_number

class Guest(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    number = models.IntegerField()
    room  = models.OneToOneField(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField(auto_now=True)
    check_out = models.DateTimeField(null=True,blank=True)
    
    def __str__(self):
        return self.name
    
class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.action