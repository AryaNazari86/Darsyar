
import persian
from django import template

register = template.Library()

@register.filter
def convert_en_numbers(number):
    return persian.convert_en_numbers(str(number))

@register.filter()
def rangeFilter(max):
    return range(max)