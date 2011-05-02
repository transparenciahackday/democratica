#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import Day, Entry
from deputados.models import Government, Party
from django.views.generic.list_detail import object_list, object_detail
from django.utils.safestring import mark_safe

import datetime
import dateutil.parser

PARTY_COLORS = {'ps': '#d888b5',
          'psd': '#cb8d41',
          'pcp': '#c74343',
          'be': '#671717',
          'cdspp': '#606798',
          'pev': '#607454',
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

def day_list(request, year=datetime.date.today().year):
    extra = {}
    # date_start = dateutil.parser.parse('2000-10-16')
    # date_end = dateutil.parser.parse('2011-09-10')
    # days = Day.objects.filter(date__gt=date_start, date__lt=date_end)

    all_days = Day.objects.all()
    all_dates = all_days.values_list('date', flat=True)
    all_years = list(set([d.year for d in all_dates]))

    extra['year'] = year
    extra['years'] = all_years
    extra['session_dates'] = all_dates

    return object_list(request, all_days, extra_context=extra)

def day_detail(request, object_id):
    day = Day.objects.get(id=object_id)
    entries = Entry.objects.filter(day=day).order_by('id')
    govs = Government.objects.filter(date_started__gt=day.date)
    gov = govs.filter(date_ended__gt=day.date)
    if gov:
        gov = gov[0]
    else:
        gov = govs[len(govs)-1] if govs else None

    return object_detail(request, Day.objects.all(), object_id,
            template_object_name = 'day',
            extra_context={'entries': entries,
                           'gov': gov.number if gov else None,
                })


def day_statistics(request, object_id):
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
            if party == 'CDS-PP':
                party = 'CDSPP'
            party_counts[party.lower()] = {}
            #if party == 'PEV':
            #    party = 'Os Verdes'
            if party == 'CDSPP':
                party = 'CDS-PP'
            if party == 'PEV':
                party = 'Os Verdes'
            party_entries = entries.filter(party=party)
            total_charcount = 0
            for mpname in frozenset(party_entries.all().values_list('mp__shortname', flat=True)):
                texts = party_entries.filter(mp__shortname=mpname).values_list('text', flat=True)
                mp_charcount = len(" ".join(texts))
                total_charcount += mp_charcount
                if party == 'CDS-PP':
                    party = 'CDSPP'
                if party == 'Os Verdes':
                    party = 'PEV'
                party_counts[party.lower()][mpname] = mp_charcount


            party_counts[party.lower()]['total'] = total_charcount

    # sum must be 100
    total = 0
    for party in party_counts:
        total += party_counts[party]['total']
    factor = 100. / total

    for party in party_counts:
        # party_counts[party]['total'] = party_counts[party]['total'] * factor
        for mpname in party_counts[party]:
            party_counts[party][mpname] = party_counts[party][mpname] * factor  

    # Muito bem!
    mb_counts = {}
    for party in set(entries.values_list('party', flat=True)):
        if party == 'Os Verdes':
            party = 'PEV'
        if Party.objects.filter(abbrev=party):
            if party == 'PEV':
                party = 'Os Verdes'
            mbs = entries.filter(party=party, text__icontains='Muito bem!') | entries.filter(speaker__contains=party, text__icontains='Muito bem!')
            mbs = mbs.distinct()
            if party == 'Os Verdes':
                party = 'PEV'
            if party == 'CDS-PP':
                party = 'CDSPP'
            mb_counts[party.lower()] = len(mbs)

    return object_detail(request, Day.objects.all(), object_id,
            template_object_name = 'day', template_name='dar/day_detail_statistics.html',
            extra_context={'entries': entries,
                           'gov': gov.number if gov else None,
                           'party_counts': party_counts,
                           'party_colors': PARTY_COLORS,
                           'mb_counts': mb_counts,
                })
