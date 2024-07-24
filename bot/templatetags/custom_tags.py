
import persian
from django import template

register = template.Library()

@register.simple_tag
def convert_en_numbers(number):
    return persian.convert_en_numbers(str(number))