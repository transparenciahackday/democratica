#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import Day, Entry
from deputados.models import Government, Party
from django.views.generic.list_detail import object_list, object_detail
from django.utils.safestring import mark_safe

import dateutil.parser

COLORS = {'PS': 'd888b5',
          'PSD': 'cb8d41',
          'PCP': 'c74343',
          'BE': '671717',
          'CDS-PP': '606798',
          'Os Verdes': '607454',
          }

MESES = {
    'JANEIRO': 31,
    'FEVEREIRO': 28,
    'MARÇO': 31,
    'ABRIL': 30,
    'MAIO': 31,
    'JUNHO': 30,
    'JULHO': 31,
    'AGOSTO': 31,
    'SETEMBRO': 30,
    'OUTUBRO': 31,
    'NOVEMBRO': 30,
    'DEZEMBRO': 31,
    }

def day_list(request):
    extra = {}
    date_start = dateutil.parser.parse('2000-10-16')
    date_end = dateutil.parser.parse('2011-09-10')
    days = Day.objects.filter(date__gt=date_start, date__lt=date_end)

    all_dates = days.values_list('date', flat=True)
    years = list(set([d.year for d in all_dates]))

    extra['years'] = years
    extra['session_dates'] = all_dates

    return object_list(request, days, extra_context=extra)

def day_detail(request, object_id):
    day = Day.objects.get(id=object_id)
    entries = Entry.objects.filter(day=day).order_by('id')
    govs = Government.objects.filter(date_started__gt=day.date)
    gov = govs.filter(date_ended__gt=day.date)
    if gov:
        gov = gov[0]
    else:
        gov = govs[len(govs)-1] if govs else None

    # generate party speaking chart
    party_counts = {}
    for party in set(entries.values_list('party', flat=True)):
        if party == 'Os Verdes':
            party = 'PEV'
        if Party.objects.filter(abbrev=party):
            if party == 'PEV':
                party = 'Os Verdes'
            texts = entries.filter(party=party).values_list('text', flat=True)
            texts = " ".join(texts)
            charcount = len(texts)
            party_counts[party] = charcount
    # sum must be 100
    total = 0
    for party in party_counts:
        total += party_counts[party]
    factor = 100. / total
    for party in party_counts:
        party_counts[party] = party_counts[party] * factor
    querystring = ''
    labels = []
    colors = []
    values = []
    for party in party_counts:
        labels.append(party)
        colors.append(COLORS[party])
        values.append(str(party_counts[party]))
    labelstring = 'chdl=' + '|'.join(labels)
    valuestring = 'chd=t:' + ','.join(values)
    colorstring = 'chco=' + '|'.join(colors)
    options = ['chf=bg,s,65432100',
               'cht=p',
               'chs=250x100']
    optionstring = '&'.join(options) 
    querystring = '&'.join([optionstring, labelstring, valuestring, colorstring])
    speaker_chart_url = mark_safe('http://chart.apis.google.com/chart?%s' % querystring)

    # Muito bem!
    mb_counts = {}
    for party in set(entries.values_list('party', flat=True)):
        if party == 'Os Verdes':
            party = 'PEV'
        if Party.objects.filter(abbrev=party):
            if party == 'PEV':
                party = 'Os Verdes'
            mbs = entries.filter(party=party, text__icontains='Muito bem!')
            mb_counts[party] = len(mbs)
    labels = []
    colors = []
    values = []
    for party in mb_counts:
        labels.append(party)
        colors.append(COLORS[party])
        values.append(str(mb_counts[party]))
    labelstring = 'chdl=' + '|'.join(labels)
    valuestring = 'chd=t:' + ','.join(values)
    colorstring = 'chco=' + '|'.join(colors)
    options = ['chf=bg,s,65432100', 
               'cht=bhs', 
               'chs=250x200',
               'chbh=10,2,1',
               'chxt=x'
               #'chtt=Muito+bem!'
               ]
    optionstring = '&'.join(options) 
    querystring = '&'.join([optionstring, labelstring, valuestring, colorstring])
    mb_chart_url = mark_safe('http://chart.apis.google.com/chart?%s' % querystring)

    return object_detail(request, Day.objects.all(), object_id,
            template_object_name = 'day',
            extra_context={'entries': entries,
                           'gov': gov.number if gov else None,
                           'speaker_chart_url': speaker_chart_url,
                           'mb_chart_url': mb_chart_url,
                })
