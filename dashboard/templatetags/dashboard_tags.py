
from django import template

register = template.Library()

@register.filter
def absolute(number):
    print(number)
    return abs(number)

@register.filter
def mul(value, arg):
    return value * arg

@register.filter
def div(value, arg):
    return value // arg