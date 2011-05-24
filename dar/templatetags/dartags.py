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
    from datetime import date
    if int(year) == date.today().year:
        month = date.today().month
        return MESES[:month]
    return MESES

@register.filter
def days_for_month(month, year):
    import calendar, datetime
    year = int(year)
    month_number = MESES.index(month)+1
    number_days = calendar.monthrange(year, month_number)[1]
    dates = []
    for day in range(1, number_days+1):
        if not datetime.date(year, month_number, day) > datetime.date.today():
            dates.append(datetime.date(year, month_number, day))
    return dates

@register.filter
def month_abbrev(month):
    return month[:3]

@register.filter
def slice_year(y):
    return str(y)[2:]

@register.filter
def is_weekend(d):
    return True if d.weekday() in (5,6) else False

@register.filter
def session_url(day):
    from democratica.dar.models import Day
    d = Day.objects.get(date=day)
    return d.get_absolute_url()

@register.filter
def day_padding(day):
    output = ''
    for x in range(day.weekday()):
        output += '<li><span class="empty">&nbsp;</span></li>'
    return mark_safe(output)

# stolen from http://stackoverflow.com/questions/783897/truncating-floats-in-python
def trunc(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    slen = len('%.*f' % (n, f))
    return str(f)[:slen]


@register.filter
def floatise(s):
    return mark_safe(trunc(s, 2).replace(',','.'))

@register.filter
def lookup(dict, index):
    if index in dict:
        return dict[index]
    assert False
    return ''

@register.filter
def lookuplookup(dict, index1, index2):
    if index1 in dict:
        if index2 in dict[index1]:
            return dict[index1][index2]
    return ''
