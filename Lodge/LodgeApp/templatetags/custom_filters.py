from django import template
from datetime import timedelta, datetime

register = template.Library()

@register.filter(name='add_one_hour')
def add_one_hour(value):
    if isinstance(value, datetime):
        return value + timedelta(hours=1)
    return value