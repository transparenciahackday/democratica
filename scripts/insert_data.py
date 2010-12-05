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
from django.contrib.auth.models import User

from dptd.deputados.models import MP, Caucus, FactType, Fact, Activity, Party, LinkSet

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
        MP.objects.create(id = int(mp_id),
                          name = name,
                          shortname = shortname,
                          dob = d,
                          occupation = occupation
                          )

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

        Caucus.objects.create(mp = MP.objects.get(id=mp_id),
                            session = session,
                            date_begin = date_begin,
                            date_end = date_end,
                            constituency = constituency,
                            party = p,
                            has_activity = bool(has_activity),
                            has_registointeresses = bool(has_registointeresses),
                            )
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

def insert_linksets(csvfile=os.path.join(DATASET_DIR, 'redes_sociais.csv')):
    print 'A processar links...'
    linkset = csv.reader(open(csvfile), delimiter=';', quotechar='"')
    for id, name, post, email, wikipedia_url, facebook_url, twitter_url, blog_url, website_url, linkedin_url, twitica_url, radio_url, tv_url in linkset:
        # ignorar primeira linha
        if "MPID" in id:
            continue
        LinkSet.objects.create(mp = MP.objects.get(id=int(id)),
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

if __name__ == '__main__':
    # insert_mps()
    # insert_facts()
    # insert_caucus()
    # insert_activities()
    insert_linksets()

