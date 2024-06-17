from django import template

register = template.Library()

# @register.simple_tag
# def calculate_revenue(date1, date2, price):
#     try:
#         return (date2 - date1).days * price/1000
#     except:
#         return 0