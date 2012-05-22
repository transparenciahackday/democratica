#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template, redirect_to
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.template.defaultfilters import escape
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import redirect, render_to_response
import reversion
from dar.models import Day, Entry
from deputados.models import Government, Party, MP
from elections.models import Election


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
    extra['years'] = all_years(reverse=True)
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
    gov = govs.filter(date_ended__gt=day.date)

    #mps = frozenset([entry.mp for entry in entries])
    mp_ids = frozenset(entries.values_list('mp', flat=True))
    mps = list(MP.objects.filter(id__in=mp_ids).distinct())

    mp_lookup = {}
    for mp in mps:
        if not mp.id:
            continue
        from deputados.utils import get_mandate_for_date
        mandate = get_mandate_for_date(mp, d)
        if mandate:
            mp_lookup[int(mp.id)] = {'shortname': mp.shortname, 'party_abbrev': mandate.party.abbrev, 
                    'constituency': mandate.constituency.name,
                    'current_mandate': mandate, 'photo': mp.photo, 'id': int(mp.id), 'url': mp.get_absolute_url()}

    if govs:
        gov = govs[0]
    else:
        gov = govs[len(govs)-1] if govs else None

    if day.legislature.number >= 7:
        from democratica.core.darpdfurls import encode_url
        pdf_url = encode_url(day.legislature.number, day.legislative_session, day.diary_number)
    else:
        pdf_url = None

    return direct_to_template(request, 'dar/day_detail.html',
        extra_context={'day': day, 'entries': entries,
                       'gov': gov.number if gov else None,
                       'mpdict': mp_lookup,
                       'pdf_url': pdf_url,
                })

def entry_detail(request, year, month, day, position):
    d = datetime.date(year=int(year), month=int(month), day=int(day))
    day = Day.objects.get(date=d)
    try:
        e = Entry.objects.get(day=day, position=position)
    except Entry.DoesNotExist:
        e = Entry.objects.filter(day=day, position__lt=position).order_by('-position')[0]
    url = day.get_absolute_url() + '#' + str(e.position)
    return redirect_to(request=request, url=url)


def day_statistics(request, year, month, day):
    d = datetime.date(year=int(year), month=int(month), day=int(day))
    day = Day.objects.get(date=d)
    all_days = Day.objects.all()
    entries = Entry.objects.filter(day=day).order_by('position')
    govs = Government.objects.filter(date_started__lt=day.date, date_ended__gt=day.date)
    gov = govs.filter(date_ended__gt=day.date)
    if govs:
        gov = govs[0]
    else:
        gov = govs[len(govs)-1] if govs else None

    from deputados.models import Mandate
    from deputados.utils import get_legislature_for_date
    leg = get_legislature_for_date(d)
    # generate party speaking chart
    party_counts = {}
    mb_counts = {}
    mp_ids = frozenset(entries.values_list('mp__id', flat=True))
    mps = MP.objects.filter(id__in=mp_ids)
    for mp in mps:
        # determine party at time of session
        mandate = Mandate.objects.get(mp=mp, legislature=leg)
        party = mandate.party
        # get entries
        mp_entries = entries.filter(mp__id=mp.id)
        muitobem_count = mp_entries.filter(text__icontains='Muito bem!').count()
        # we need lowercase party names and no hyphens because we reuse them as css classes
        party_abbrev = party.abbrev.lower()
        if party_abbrev == 'cds-pp':
            party_abbrev = 'cdspp'
        if not mb_counts.get(party_abbrev):
            mb_counts[party_abbrev] = 0
        mb_counts[party_abbrev] += muitobem_count
        texts = mp_entries.values_list('text', flat=True)
        charcount = len(" ".join(texts))
        if not party_counts.get(party_abbrev):
            party_counts[party_abbrev] = {}
        party_counts[party_abbrev][mp.shortname] = charcount
        if not party_counts[party_abbrev].get('total'):
            party_counts[party_abbrev]['total'] = 0
        party_counts[party_abbrev]['total'] += charcount

    # Vozes
    for party_abbrev in party_counts:
        if party_abbrev == 'cdspp':
            party_abbrev = 'cds-pp'
        mb_party = entries.filter(speaker__contains=party_abbrev.upper(), text__icontains='Muito bem!').count()
        if party_abbrev == 'cds-pp':
            party_abbrev = 'cdspp'
        mb_counts[party_abbrev] += mb_party

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

    # FIXME: isto podia estar bem melhor optimizado
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
    
    # criar dic de palavras mais mencionadas neste dia
    if day.top5words:
        # ugly ugly way to get the (unknown name) key from a dict
        words = day.top5words['words'][0].items()[0][0]
    else:
        words = {}

    return object_detail(request, all_days, day.id,
            template_object_name = 'day', template_name='dar/day_detail_statistics.html',
            extra_context={'entries': entries,
                           'gov': gov.number if gov else None,
                           'party_counts': party_counts,
                           'party_colors': PARTY_COLORS,
                           'mb_counts': mb_counts,
                           'top5words': words,
                           'nextdate': next_date, 'prevdate': prev_date,
                })

def day_revisions(request, year, month, day):
    from reversion.helpers import generate_patch_html
    d = datetime.date(year=int(year), month=int(month), day=int(day))
    day = Day.objects.get(date=d)
    entries = Entry.objects.filter(day=day).order_by('position')
    all_versions = []
    for e in entries:
        versions = list(reversion.get_for_object(e))
        if len(versions) > 1:
            count = 0
            for v in versions:
                try:
                    next_v = versions[versions.index(v)-1]
                    if count:
                        diffstr = generate_patch_html(v, next_v, "raw_text", cleanup="efficiency") 
                    else:
                        diffstr = ''
                except IndexError:
                    next_v = None
                    diffstr = ''
                # if not v.revision.comment == "Initial version.":
                all_versions.append((v, diffstr))
                count += 1

    '''
    from reversion.helpers import generate_patch
    # Get the page object to generate diffs for.
    page = Page.objects.all()[0]
    # Get the two versions to compare.
    available_versions = Version.objects.get_for_object(page)
    old_version = available_versions[0]
    new_version = available_versions[1]
    '''

    return direct_to_template(request, 'dar/day_revisions.html',
        extra_context={'day': day, 'revs': all_versions,
                })

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
                words[day.get_absolute_url()] = day.get_5words_list()
            except KeyError:
                continue
        wordlist[year] = words

    return direct_to_template(request, 'dar/wordlist.html',
        extra_context={'wordlist': wordlist, })

#@ajax_login_required
@ensure_csrf_cookie
@reversion.create_revision()
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

def parse_session_entries(request, id):
    from django.contrib import messages
    from dar.tasks import parse_entries_task
    t = parse_entries_task.delay(id)
    messages.info(request, "Catalogação agendada! Demora uns 5 minutos.")
    d = Day.objects.get(id=int(id))
    return day_list(request, year=d.date.year)

@reversion.create_revision()
def mark_as_cont(request, id):
    e = Entry.objects.get(id=int(id))
    if e.type == '':
        from parsing import find_cont_speaker
        find_cont_speaker(e)
    e.type = 'continuacao'
    e.save()
    return HttpResponse('<p>%s</p>' % e.type)
@reversion.create_revision()
def mark_as_main(request, id):
    e = Entry.objects.get(id=int(id))
    e.type = 'deputado_intervencao'
    e.save()
    return HttpResponse('<p>%s</p>' % e.type)

@reversion.create_revision()
def unmark_as_cont(request, id):
    e = Entry.objects.get(id = int(id))
    e.determine_type()
    return HttpResponse('<p>%s</p>' % e.type)

@reversion.create_revision()
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

@reversion.create_revision()
def join_entry_with_previous(request, id):
    e = Entry.objects.get(id = int(id))
    prev_e = Entry.objects.get(id=e.prev_id)
    next_e = Entry.objects.get(id=e.next_id)
    prev_e.raw_text += '\n' + e.raw_text
    if e.text and prev_e.text:
        prev_e.text += '\n' + e.text
    e.delete()
    prev_e.save()
    prev_e.calculate_neighbors()
    next_e.calculate_neighbors()
    return HttpResponse('<p>OK</p>')

@reversion.create_revision()
def correct_newlines(request, id):
    e = Entry.objects.get(id = int(id))
    lines = e.raw_text.split('\n')
    output = ''
    for line in lines:
        if not line.strip().endswith(('.', '?', '!')):
            output += line.strip() + ' '
        elif 65 < len(line) < 140:
            output += line.strip() + ' '
        else:
            output += line.strip() + '\n'
    current_type = e.type
    e.raw_text = output
    e.save()
    e.parse_raw_text()
    e.type = current_type
    e.save()
    return HttpResponse('<p>OK</p>')


@reversion.create_revision()
def refresh(request, id):
    skip_parsing = request.GET.get('skip_parsing')
    e = Entry.objects.get(id=int(id))
    if not skip_parsing:
        e.parse_raw_text()
    from django.template import Context, loader
    if e.mp:
        mp = e.mp
        mpdict = {}
        mpdict[int(mp.id)] = {'shortname': mp.shortname, 'party_abbrev': mp.current_party.abbrev, 
                'constituency': mp.current_mandate.constituency.name,
                'current_mandate': mp.current_mandate, 'photo': mp.photo, 'id': int(mp.id)}
        c = Context({'entry': e, 'mpdict': mpdict})
    else:
        c = Context({'entry': e})
    from dar.templatetags.dartags import get_template_from_entry_type
    t = loader.get_template(get_template_from_entry_type(e.type))
    return HttpResponse(t.render(c))
