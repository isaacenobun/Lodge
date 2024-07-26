from django.contrib import admin
from .models import Staff, Room, Guest, GuestHistory, Log, Revenue, CheckIns, Company, Suite, Subscriptions
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('company', 'amount', 'start_date', 'due_date', 'payment_status')
    search_fields = ('company__name', 'due_date')

class SuiteAdmin(admin.ModelAdmin):
    list_display = ('type', 'company', 'price')
    search_fields = ('type', 'company__name')

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_tag', 'suite', 'company', 'room_status')
    search_fields = ('room_tag', 'suite__type', 'company__name')

class RevenueAdmin(admin.ModelAdmin):
    list_display = ('revenue', 'company')
    search_fields = ('company__name',)

class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'number', 'room', 'check_in', 'check_out', 'staff', 'company', 'duration')
    search_fields = ('name', 'email', 'room__room_number', 'company__name', 'staff__username')

class GuestHistoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'number', 'room', 'check_in', 'check_out', 'staff', 'company', 'duration')
    search_fields = ('name', 'email', 'room__room_number', 'company__name', 'staff__username')

class LogAdmin(admin.ModelAdmin):
    list_display = ('staff', 'action', 'check_status', 'timestamp', 'company')
    search_fields = ('staff__username', 'company__name')

class CheckInsAdmin(admin.ModelAdmin):
    list_display = ('time', 'company')
    search_fields = ('company__name',)

class StaffAdmin(UserAdmin):
    # Customize the admin form to include email, username, and company fields
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('company',)}),  # Include custom fields
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'username', 'company','owner')}),  # Include custom fields for the add user form
    )

    list_display = ('email', 'username', 'company', 'owner', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(Company, CompanyAdmin)
admin.site.register(Subscriptions, SubscriptionsAdmin)
admin.site.register(Suite, SuiteAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Revenue, RevenueAdmin)
admin.site.register(Guest, GuestAdmin)
admin.site.register(GuestHistory, GuestHistoryAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(CheckIns, CheckInsAdmin)