from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Staff(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
class Room(models.Model):
    ROOM_NUMBERS = [(str(num),str(num)) for num in range(1,21)]
    ROOM_TYPES = [('regular', 'Regular'),
                   ('business', 'Business'),
                   ('executive', 'Executive')
                  ]
    
    room_number = models.CharField(max_length=2, choices=ROOM_NUMBERS, unique=True)
    room_status = models.BooleanField(default=False)
    room_price = models.IntegerField(default=10000)
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES, default='Regular')
    
    def __str__(self):
        return f'{self.room_number} - {self.room_status}'

class Guest(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    number = models.IntegerField()
    room  = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField(auto_now_add=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    check_out = models.DateTimeField(null=True,blank=True)
    
    def __str__(self):
        return self.name
    
class Log(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    check_in_action = models.CharField(max_length=300, blank=True)
    check_out_action = models.CharField(max_length=300, blank=True)
    check_status = models.BooleanField(default=False)
    timestamp = models.DateTimeField()
    
    def __str__(self):
        return f'{self.check_in_action} {self.check_out_action}'
    
class Revenue(models.Model):
    revenue = models.DecimalField(max_digits=10, decimal_places=1)
    guest_check_out = models.ForeignKey(Guest, on_delete=models.PROTECT)
    
    def __str__(self):
        return f'{self.revenue}'
    
class CheckIns(models.Model):
    time = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.time