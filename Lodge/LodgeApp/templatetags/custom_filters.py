from django import template
from datetime import timedelta, datetime

register = template.Library()

@register.filter(name='add_one_hour')
def add_one_hour(value):
    # if isinstance(value, datetime):
    return value + timedelta(hours=1)
    # return value

@register.filter(name='days_between')
def days_between(date1, date2):
    try:
        return (date2 - date1).days
    except:
        return 0
    
@register.filter(name='get_guest_name')
def get_guest_name(room_id, room_guest_mapping):
    guest = room_guest_mapping.get(room_id)
    return guest.name

@register.filter(name='get_guest_id')
def get_guest_id(room_id, room_guest_mapping):
    guest = room_guest_mapping.get(room_id)
    return guest.id