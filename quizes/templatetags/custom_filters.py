from django import template

register = template.Library()

@register.filter
def round_number(value):
    return round(value)
