from django.shortcuts import render

from .models import *

# Create your views here.
def dashboard(request):
    guests = Guest.objects.all()
    context = {'guests':guests}
    return render(request, 'index.html', context)