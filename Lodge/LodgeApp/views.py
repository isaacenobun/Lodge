from django.shortcuts import render, get_object_or_404

from .models import *

# Create your views here.
def dashboard(request):
    guests = Guest.objects.all()
    context = {'guests':guests}
    return render(request, 'index.html', context)

def rooms(request):
    
    context = {}
    return render(request, 'pages-room-carousel.html', context)

def history(request):
    guests = Guest.objects.all()
    context = {'guests':guests}
    return render(request, 'pages-guest-history.html', context)

def check_in(request):
    if request.method == 'POST':
        room_id = request.POST.get('room')
        room = get_object_or_404(Room, id=room_id)

        guest = Guest.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            number=request.POST.get('phone'),
            room=room
        )

        room.room_status = True
        room.save()

        guests = Guest.objects.all()
        context = {'guests': guests}
        return render(request, 'index.html', context)
    
    rooms = Room.objects.filter(room_status=True) # Need to change to False
    context = {'rooms':rooms}
    return render(request, 'pages-check-in-out.html', context)