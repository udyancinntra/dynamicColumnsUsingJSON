from django import template

register = template.Library()

@register.filter(name='split')
def split(value, delimiter):
    if isinstance(value, str):
        return value.split(delimiter)
    return []
