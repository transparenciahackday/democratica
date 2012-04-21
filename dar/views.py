#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import Day, Entry
from deputados.models import Government, Party, MP
from elections.models import Election
from django.http import HttpResponse, Http404
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template, redirect_to
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.template.defaultfilters import escape
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import redirect, render_to_response


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

    from democratica.dar.utils import days_for_year, all_years, elections_for_year

    all_days = days_for_year(year)
    words = {}
    for d in all_days:
        # criar dic de palavras mais mencionadas por dia
        if d.top5words:
            # ugly ugly way to get the (unknown name) key from a dict
            words[d.date] = d.top5words['words'][0].items()[0][0]
        else:
            words[d.date] = '-'
    extra['words'] = words

    all_dates = all_days.values_list('date', flat=True)
    extra['year'] = year
    extra['years'] = all_years
    extra['session_dates'] = all_dates

    election_dates = {}
    for el in elections_for_year(year):
        election_dates[el.date] = el.type
    extra['election_dates'] = election_dates
    
    return object_list(request, all_days, extra_context=extra)

def day_detail(request, year, month, day):
    d = datetime.date(year=int(year), month=int(month), day=int(day))
    day = Day.objects.get(date=d)
    entries = Entry.objects.filter(day=day).order_by('position')
    govs = Government.objects.filter(date_started__lt=day.date, date_ended__gt=day.date)
    # gov = govs.filter(date_ended__gt=day.date)

    #mps = frozenset([entry.mp for entry in entries])
    # mp_ids = frozenset(entries.values_list('mp', flat=True))
    # mps = list(MP.objects.filter(id__in=mp_ids))

    # mp_lookup = {}
    # for mp in mps:
    #    if not mp.id:
    #        continue
        #mp = mps.values('shortname', 'current_party', 'current_caucus', 'photo').get(id=mp_id)

    #     mp_lookup[int(mp.id)] = {'shortname': mp.shortname, 'current_party': mp.current_party,
    #             'current_caucus': mp.current_caucus, 'photo': mp.photo, 'id': mp.id}


    if govs:
        gov = govs[0]
    else:
        gov = govs[len(govs)-1] if govs else None

    return direct_to_template(request, 'dar/day_detail.html',
        extra_context={'day': day, 'entries': entries,
    #                   'gov': gov.number if gov else None,
    #                   'mp_lookup': mp_lookup,
                })

def day_statistics(request, year, month, day):
    d = datetime.date(year=int(year), month=int(month), day=int(day))
    day = Day.objects.get(date=d)
    all_days = Day.objects.all()
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
    if party_counts:
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

    # dia seguinte e anterior pró paginador
    next_date = None
    prev_date = None
    day_list = list(all_days.values_list('id', flat=True))
    try:
        next_id = day_list[day_list.index(day.id) + 1]
        next_day = Day.objects.get(id=next_id)
        next_date = next_day.date
    except (IndexError, AttributeError):
        pass
    try:
        prev_id = day_list[day_list.index(day.id) - 1]
        prev_day = Day.objects.get(id=prev_id)
        prev_date = prev_day.date
    except (IndexError, AttributeError):
        pass
    

    return object_detail(request, all_days, day.id,
            template_object_name = 'day', template_name='dar/day_detail_statistics.html',
            extra_context={'entries': entries,
                           'gov': gov.number if gov else None,
                           'party_counts': party_counts,
                           'party_colors': PARTY_COLORS,
                           'mb_counts': mb_counts,
                           'top5words': day.top5words['words'],
                           'nextdate': next_date, 'prevdate': prev_date,
                })

def statement_detail(request, id=None):
    if not id:
        raise Http404
    e = Entry.objects.get(id=id)
    url = e.day.get_absolute_url() + '#' + str(e.id)
    return redirect_to(request=request, url=url)

def wordlist(request):
    wordlist = {}
    all_years = list(set([d['date'].year for d in Day.objects.all().values('date')]))
    all_years.sort()
    for year in all_years:
        words = {}
        first_day_of_year = datetime.date(year=year, month=1, day=1)
        last_day_of_year = datetime.date(year=year, month=12, day=31)
        all_days = Day.objects.filter(date__gt=first_day_of_year, date__lt=last_day_of_year)
        for day in all_days:
            try:
                words[day.get_absolute_url()] = day.get_5words_list
            except KeyError:
                continue
        wordlist[year] = words

    return direct_to_template(request, 'dar/wordlist.html',
        extra_context={'wordlist': wordlist, })

#@ajax_login_required
@ensure_csrf_cookie
def entry_save(request):
    try:
        div_id = request.POST[u'id']
        value = request.POST[u'value']
    except:
        raise Exception(u'Invalid id')
    id = div_id.split('_')[-1]
    e = Entry.objects.get(id=int(id))
    e.raw_text = value
    e.save()
    if '\n\n' in value:
        from parsing import split_entry
        split_entry(e)
    e.parse_raw_text()
    return HttpResponse(e.text_as_html)

def fetch_raw_entry(request):
    id = request.GET.get('id')
    id = id.split('_')[-1]
    raw_text = Entry.objects.get(id=id).raw_text
    return HttpResponse(raw_text)

def mark_as_cont(request, id):
    e = Entry.objects.get(id=int(id))
    if e.type == '':
        from parsing import find_cont_speaker
        find_cont_speaker(e)
    e.type = 'continuacao'
    e.save()
    return HttpResponse('<p>%s</p>' % e.type)
def mark_as_main(request, id):
    e = Entry.objects.get(id=int(id))
    e.type = 'deputado_intervencao'
    e.save()
    return HttpResponse('<p>%s</p>' % e.type)

def unmark_as_cont(request, id):
    e = Entry.objects.get(id = int(id))
    e.determine_type()
    return redirect('statement_detail', id=id) 

def mark_as_aside(request, id):
    e = Entry.objects.get(id=int(id))
    if e.type == 'deputado_intervencao':
        e.type = 'deputado_aparte'
    elif e.type.startswith('pm'):
        e.type = 'pm_aparte'
    elif e.type.startswith('ministro'):
        e.type = 'ministro_aparte'
    elif e.type.startswith('secestado'):
        e.type = 'secestado_aparte'
    elif e.type.startswith('presidente'):
        e.type = 'presidente_aparte'
    e.save()
    return HttpResponse('<p>%s</p>' % e.type)

def join_entry_with_previous(request, id):
    e = Entry.objects.get(id = int(id))
    prev_e = e.get_previous()
    prev_e.raw_text += '\n' + e.raw_text
    if e.text and prev_e.text:
        prev_e.text += '\n' + e.text
    e.delete()
    prev_e.save()
    return HttpResponse('<p>OK</p>')

def refresh(request, id):
    skip_parsing = request.GET.get('skip_parsing')
    e = Entry.objects.get(id=int(id))
    if not skip_parsing:
        e.parse_raw_text()
    from django.template import Context, loader
    t = loader.get_template('dar/entry_snippet.html')
    c = Context({'entry': e})
    return HttpResponse(t.render(c))
