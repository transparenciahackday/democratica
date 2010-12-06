#!/usr/bin/env python
# -*- coding: utf-8 -*-

DATASET_DIR = '../../datasets/'

### Set up Django path
import sys, os
projectpath = os.path.abspath('../../')
if projectpath not in sys.path:
    sys.path.append(projectpath)
    sys.path.append(os.path.join(projectpath, 'dptd/'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'dptd.settings'

import csv
import datetime, time

from dptd.deputados.models import *
import dptd.deputados.utils as utils

def insert_mps(csvfile=os.path.join(DATASET_DIR, 'MP.csv')):
    print 'A processar deputados...'
    mps = csv.reader(open(csvfile), delimiter='|', quotechar='"')
    for id, mp_id, name, dob, occupation, date_added  in mps:
        if name == 'N/A':
            continue
        first_name = name.split(' ')[0]
        last_name = name.split(' ')[-1]
        shortname = '%s %s' % (first_name, last_name)
        dateformat = '%d-%m-%Y'
        try:
            c = time.strptime(dob, dateformat)
            d = datetime.date(year=c[0], month=c[1], day=c[2])
        except ValueError:
            d = None
        gender = utils.get_gender_from_name(first_name)
        MP.objects.create(id = int(mp_id),
                          gender = gender,
                          name = name,
                          shortname = shortname,
                          dob = d,
                          occupation = occupation
                          )
    print 'A associar fotos dos deputados...'
    from django.core.files.base import ContentFile
    for mp in MP.objects.all():
        imgfilename = os.path.join(projectpath, 'dptd/media/fotos-deputados', '%d.jpg' % mp.id)
        if os.path.exists(imgfilename):
            file_content = ContentFile(open(imgfilename, 'rb').read())
            mp.photo.save(imgfilename, file_content)
            file_content.close()
        else:
            pass

def insert_facts(csvfile=os.path.join(DATASET_DIR, 'Facts.csv')):
    print 'A processar factos...'
    facts = csv.reader(open(csvfile), delimiter='|', quotechar='"')
    for id, mp_id, fact_type, value, date_added in facts:
        if FactType.objects.filter(name=fact_type):
            f = FactType.objects.get(name=fact_type)
        else:
            f = FactType.objects.create(name=fact_type)

        Fact.objects.create(mp = MP.objects.get(id=mp_id),
                            fact_type = f,
                            value = value,
                            )

def insert_caucus(csvfile=os.path.join(DATASET_DIR, 'Caucus.csv')):
    print 'A processar círculos eleitorais...'
    caucus = csv.reader(open(csvfile), delimiter='|', quotechar='"')
    for id, mp_id, session, dates, constituency, party, has_activity, has_registointeresses, date_added in caucus:
        if Party.objects.filter(abbrev=party):
            p = Party.objects.get(abbrev=party)
        else:
            p = Party.objects.create(abbrev=party)

        from roman import fromRoman
        session_number = fromRoman(session)
        if Session.objects.filter(number=session_number):
            s = Session.objects.get(number=session_number)
        else:
            s = Session.objects.create(number=session_number)

        dates = dates.split(' ')
        date_begin = dates[1].replace('[', '')
        date_end = dates[3].replace(']', '')

        dateformat = '%Y-%m-%d'
        try:
            c = time.strptime(date_begin, dateformat)
            date_begin = datetime.date(year=c[0], month=c[1], day=c[2])
        except ValueError:
            print 'Error - Begin: ' + date_begin
            date_begin = None
        try:
            c = time.strptime(date_end, dateformat)
            date_end = datetime.date(year=c[0], month=c[1], day=c[2])
        except ValueError:
            if not date_begin:
                print 'Error - End: ' + date_end
            date_end = None

        if Constituency.objects.filter(name=constituency):
            c = Constituency.objects.get(name=constituency)
        else:
            c = Constituency.objects.create(name=constituency)

        Caucus.objects.create(mp = MP.objects.get(id=mp_id),
                            session = s,
                            date_begin = date_begin,
                            date_end = date_end,
                            constituency = c,
                            party = p,
                            has_activity = bool(has_activity),
                            has_registointeresses = bool(has_registointeresses),
                            )

    constituency_file = csv.reader(open(os.path.join(DATASET_DIR, 'circulos_eleitorais.csv')), delimiter='|', quotechar='"')
    print constituency_file
    for name, article in constituency_file:
        c = Constituency.objects.get(name=name)
        c.article = article
        c.save()

def insert_activities(csvfile=os.path.join(DATASET_DIR, 'Activities.csv')):
    print 'A processar actividades...'
    caucus = csv.reader(open(csvfile), delimiter='|', quotechar='"')
    for id, mp_id, caucus, type1, type2, number, session, content, date_added, external_id in caucus:
        if Activity.objects.filter(id=id):
            continue
        Activity.objects.create(mp = MP.objects.get(id=int(mp_id)),
                            caucus = Caucus.objects.get(id=int(caucus)),
                            type1 = type1,
                            type2 = type2,
                            number = number,
                            session = session,
                            content = content,
                            external_id = external_id,
                             )
    for mp in MP.objects.all():
        mp.has_activity = bool(mp.activity_set.all())
        mp.save()

def insert_linksets(csvfile=os.path.join(DATASET_DIR, 'redes_sociais.csv')):
    print 'A processar links...'
    linkset = csv.reader(open(csvfile), delimiter=';', quotechar='"')
    for id, name, post, email, wikipedia_url, facebook_url, twitter_url, blog_url, website_url, linkedin_url, twitica_url, radio_url, tv_url in linkset:
        # ignorar primeira linha
        if "MPID" in id:
            continue
        wikipedia_url = wikipedia_url.replace('http://', '')
        blog_url = blog_url.replace('http://', '')
        mp = MP.objects.get(id=int(id))
        LinkSet.objects.create(mp = mp,
                               email = email,
                               wikipedia_url = wikipedia_url,
                               facebook_url = facebook_url,
                               twitter_url = twitter_url,
                               blog_url = blog_url,
                               website_url = website_url,
                               linkedin_url = linkedin_url,
                               twitica_url = twitica_url,
                               radio_url = radio_url,
                               tv_url = tv_url
                )
        if name:
            mp.shortname = name.strip()
            mp.save()

    # criar LinkSets inactivos, senão há erros totós no databrowse
    # e noutros sítios
    for mp in MP.objects.all():
        try:
            l = MP.linkset
        except LinkSet.DoesNotExist:
            Linkset.objects.create(mp=mp, active=False)

def insert_parties(csvfile=os.path.join(DATASET_DIR, 'listagem_partidos.csv')):
    print 'A processar partidos...'
    party = csv.reader(open(csvfile), delimiter='|', quotechar='"')
    for abbrev, name, tendency, info in party:
        # ignorar primeira linha
        if "Sigla" in abbrev:
            continue
        if Party.objects.filter(abbrev=abbrev):
            p = Party.objects.get(abbrev=abbrev)
        else:
            p = Party.objects.create(abbrev=abbrev, has_mps=False)
        p.name = name
        p.tendency = tendency
        p.info = info
        p.save()



if __name__ == '__main__':
    insert_mps()
    insert_facts()
    insert_caucus()
    insert_activities()
    insert_linksets()
    insert_parties()
