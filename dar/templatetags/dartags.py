# -*- coding: utf-8 -*-

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

REGIOES = ['Lisboa', 'Porto', 'Portugal']

MESES = [
    'Janeiro',
    'Fevereiro',
    'Março',
    'Abril',
    'Maio',
    'Junho',
    'Julho',
    'Agosto',
    'Setembro',
    'Outubro',
    'Novembro',
    'Dezembro',
    ]

@register.filter
def months_for_year(year):
    # yes, this function is a bit derp
    return MESES

@register.filter
def days_for_month(month, year):
    import calendar, datetime
    year = int(year)
    month_number = MESES.index(month)+1
    number_days = calendar.monthrange(year, month_number)[1]
    dates = []
    for day in range(1, number_days+1):
        dates.append(datetime.date(year, month_number, day))
    return dates

@register.filter
def month_abbrev(month):
    return month[:3]

@register.filter
def is_weekend(d):
    return True if d.weekday() in (5,6) else False

@register.filter
def session_url(day):
    from democratica.dar.models import Day
    d = Day.objects.get(date=day)
    return d.get_absolute_url()

