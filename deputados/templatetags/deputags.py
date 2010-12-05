from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def filter_timestring(obj): 
    import dateutil.parser

    output = dateutil.parser.parse(obj)
    
    return output
