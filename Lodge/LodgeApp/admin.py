from django.contrib import admin
from .models import Staff, Room, Guest, Log, Revenue, CheckIns, Company, Suite

# Register your models here.
admin.site.register(Staff)
admin.site.register(Room)
admin.site.register(Guest)
admin.site.register(Log)
admin.site.register(Revenue)
admin.site.register(CheckIns)
admin.site.register(Company)
admin.site.register(Suite)