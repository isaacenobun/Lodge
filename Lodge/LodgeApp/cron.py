from django.utils import timezone
from datetime import timedelta
from .models import Room, Guest

def check_room_status():
    now = timezone.now()
    
    active_rooms = Room.objects.filter(room_status=True)
    
    for room in active_rooms:
        guests = Guest.objects.filter(room=room)
        
        all_checked_out = all(guest.check_out <= now for guest in guests)
        
        if all_checked_out:
            room.room_status = False
            room.save()
    
    print(f'Room statuses updated at {now}')