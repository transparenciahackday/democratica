# -*- coding: utf-8 -*-

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

REGIOES = ['Lisboa', 'Porto', 'Portugal']

@register.filter
def filter_timestring(obj): 
    import dateutil.parser
    output = dateutil.parser.parse(obj)
    return output

@register.filter
def filter_news_tuple(obj):
    url = obj['url']
    title = obj['title']
    date = obj['date']
    s = title.split(' - ')
    if s[-1] in REGIOES:
        # Caso o título da agência seja algo como "Diário de Notícias - Lisboa", em que tem
        # o pedaço " - " que estamos a detectar para dividir o título e a agência, temos de
        # juntar tudo
        agency = s[-2] + " - " + s[-1]
        s.pop(-1)
        s.pop(-1)
    else:
        # Senão, tá-se bem!
        agency = s.pop(-1)
    title = " - ".join(s)
    output = '<a href="%s">%s</a><small> %s</small>' % (url, title, agency)
    return mark_safe(output)

@register.filter
def get_post_on(obj, gov_number):
    post = obj.post_on(gov_number)
    if post:
        return post.name
    return None
