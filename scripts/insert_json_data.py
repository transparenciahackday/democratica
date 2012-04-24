#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Script para criar os modelos do Django a partir dos datasets
Copyright 2010-2011 Ricardo Lafuente <r@sollec.org>

Licenciado segundo a GPL v3
http://www.gnu.org/licenses/gpl.html

'''


### Set up Django path
import sys, os
projectpath = os.path.abspath('../../')
if projectpath not in sys.path:
    sys.path.append(projectpath)
    sys.path.append(os.path.join(projectpath, 'democratica/'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'democratica.settings'

from democratica.settings import DATASET_DIR, PHOTO_DIR

MP_FILE = 'deputados.json'
GENDERS_FILE = 'deputados-genero.csv'
FACTS_FILE = 'deputados-factos.csv'
CAUCUS_FILE = 'deputados-legislaturas.csv'
ACTIVITIES_FILE = 'deputados-actividades.csv'
LINKSETS_FILE = 'deputados-links.csv'
PARTIES_FILE = 'partidos.csv'
SHORTNAMES_FILE = 'deputados-nomes.csv'
CONSTITUENCIES_FILE = 'regioes.csv'
GOVERNMENT_FILE = 'governos-cargos.csv'

def check_for_files():
    all_files = [MP_FILE, GENDERS_FILE, FACTS_FILE, CAUCUS_FILE, ACTIVITIES_FILE, 
                 LINKSETS_FILE, PARTIES_FILE, CONSTITUENCIES_FILE, GOVERNMENT_FILE]
    
    for f in all_files:
        path = os.path.join(DATASET_DIR, f)
        if not os.path.exists(path):
            print 'File %s not found! Check this and try again.' % (f)
            sys.exit()

import csv, json
import datetime, time

from democratica.deputados.models import *

def insert_mps(jsonfile=os.path.join(DATASET_DIR, MP_FILE)):
    import dateutil.parser
    print 'A processar deputados...'
    # criar círculos eleitorais
    constituency_file = csv.reader(open(os.path.join(DATASET_DIR, CONSTITUENCIES_FILE)), delimiter='|', quotechar='"')
    for name, article in constituency_file:
        c, created = Constituency.objects.get_or_create(name=name, article=article)

    # importar dados deputados
    mps = json.loads(open(jsonfile, 'r').read())
    for id in mps:
        name = mps[id]['name']
        print name
        shortname = mps[id]['shortname']
        if mps[id].get('birthdate'):
            dob = dateutil.parser.parse(mps[id]['birthdate']).date()
        party = mps[id]['party']
        scrape_date = mps[id]['scrape_date']
        if mps[id].get('occupation'):
            if len(mps[id]['occupation']) == 1:
                occupation = mps[id]['occupation'][0]
            elif len(mps[id]['occupation']) > 1:
                occupation = ''
                for p in mps[id]['occupation']:
                    occupation.append(p + '\n')
            else:
                occupation = ''
        else:
            occupation = ''
        jobs = "\n".join(mps[id]['jobs']) if mps[id].get('jobs') else ''
        education = "\n".join(mps[id]['education']) if mps[id].get('education') else ''
        commissions = "\n".join(mps[id]['commissions'])
        mp, mp_created = MP.objects.get_or_create(id = int(id),
                          name = name,
                          shortname = shortname,
                          dob = dob,
                          occupation = occupation,
                          jobs = jobs,
                          education = education,
                          commissions = commissions,
                          )
        # criar mandatos para deputado
        from pprint import pprint
        mandate_dicts = mps[id]['mandates']
        for mandate in mandate_dicts:
            mdict = mandate
            print mp
            m, m_created = Mandate.objects.get_or_create(mp=mp,
                        party = Party.objects.get_or_create(abbrev=mdict['party'])[0],
                        constituency = Constituency.objects.get(name=mdict['constituency']),
                        legislature = Legislature.objects.get_or_create(number=mdict['legislature'])[0],
                        date_begin = dateutil.parser.parse(mdict['start_date']).date(),
                        date_end = dateutil.parser.parse(mdict['end_date']).date() if mdict['end_date'] else None,
                        )


def insert_mp_gender():
    genders = csv.reader(open(os.path.join(DATASET_DIR, GENDERS_FILE)), delimiter='|', quotechar='"')
    for mp_id, gender in genders:
        if MP.objects.filter(id=mp_id):
            mp = MP.objects.get(id=mp_id)
            mp.gender = gender
            mp.save()

    print 'A associar fotos dos deputados...'
    from django.core.files.base import ContentFile
    for mp in MP.objects.all():
        imgfilename = os.path.abspath(os.path.join(PHOTO_DIR, '%d.jpg' % mp.id))
        if os.path.exists(imgfilename):
            file_content = ContentFile(open(imgfilename, 'rb').read())
            mp.photo.save(imgfilename, file_content)
            file_content.close()
        else:
            pass
            # print 'Error: Photo file not found' 
            # print '  Expected path: %s' % imgfilename

def insert_facts(csvfile=os.path.join(DATASET_DIR, FACTS_FILE)):
    print 'A processar factos...'
    facts = csv.reader(open(csvfile), delimiter='|', quotechar='"')
    for id, mp_id, fact_type, value, date_added in facts:
        if FactType.objects.filter(name=fact_type):
            f = FactType.objects.get(name=fact_type)
        else:
            f = FactType.objects.create(name=fact_type)

        if MP.objects.filter(id=mp_id):
            Fact.objects.create(mp = MP.objects.get(id=mp_id),
                                fact_type = f,
                                value = value,
                                )
        else:
            print 'Facto sem deputado correspondente (id %s)' % str(mp_id)
    for mp in MP.objects.all():
        if not mp.has_facts:
            mp.is_active = False
            mp.save()


def insert_mandate(csvfile=os.path.join(DATASET_DIR, CAUCUS_FILE)):
    print 'A processar mandatos...'
    mandate = csv.reader(open(csvfile), delimiter='|', quotechar='"')
    for id, mp_id, legislature, dates, constituency, party, has_activity, has_registointeresses, date_added in mandate:
        if Party.objects.filter(abbrev=party):
            p = Party.objects.get(abbrev=party)
        else:
            p = Party.objects.create(abbrev=party)

        from roman import fromRoman
        legislature_number = fromRoman(legislature)
        if Legislature.objects.filter(number=legislature_number):
            s = Legislature.objects.get(number=legislature_number)
        else:
            s = Legislature.objects.create(number=legislature_number)

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

        if MP.objects.filter(id=mp_id):
            Mandate.objects.create(mp = MP.all_objects.get(id=mp_id),
                            legislature = s,
                            date_begin = date_begin,
                            date_end = date_end,
                            constituency = c,
                            party = p,
                            has_activity = bool(has_activity),
                            has_registointeresses = bool(has_registointeresses),
                            )
        else:
            print "Mandate sem deputado correspondente (%s)" % mp_id


def insert_activities(csvfile=os.path.join(DATASET_DIR, ACTIVITIES_FILE)):
    print 'A processar actividades...'
    mandate = csv.reader(open(csvfile), delimiter='|', quotechar='"')
    for id, mp_id, mandate, type1, type2, number, legislature, content, date_added, external_id in mandate:
        if Activity.objects.filter(id=id):
            continue
        elif MP.objects.filter(id=mp_id):
            Activity.objects.create(mp = MP.objects.get(id=int(mp_id)),
                            mandate = Mandate.objects.get(id=int(mandate)),
                            type1 = type1,
                            type2 = type2,
                            number = number,
                            legislature = legislature,
                            content = content,
                            external_id = external_id,
                             )
        else:
            print "Actividade sem deputado correspondente (%s)" % str(mp_id)
    for mp in MP.objects.all():
        mp.has_activity = bool(mp.activity_set.all())
        mp.save()

def insert_linksets(csvfile=os.path.join(DATASET_DIR, LINKSETS_FILE)):
    print 'A processar links...'
    linkset = csv.reader(open(csvfile), delimiter=';', quotechar='"')
    for id, name, post, email, wikipedia_url, facebook_url, twitter_url, blog_url, website_url, linkedin_url, twitica_url, radio_url, tv_url in linkset:
        # ignorar primeira linha
        if "MPID" in id:
            continue
        wikipedia_url = wikipedia_url.replace('http://', '')
        blog_url = blog_url.replace('http://', '')
        mp = MP.all_objects.get(id=int(id))
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

def insert_shortnames(csvfile=os.path.join(DATASET_DIR, SHORTNAMES_FILE)):
    # usar o ficheiro do Pedro de shortnames
    print 'A associar shortnames...'
    shortnames = csv.reader(open(csvfile), delimiter=',', quotechar='"')
    for mp_id, shortname in shortnames:
        if shortname == 'N/A' or mp_id == 'Column':
            continue
        mp = MP.all_objects.get(id=mp_id)
        mp.shortname = shortname
        mp.save()

def insert_parties(csvfile=os.path.join(DATASET_DIR, PARTIES_FILE)):
    print 'A processar partidos...'
    parties = csv.reader(open(csvfile), delimiter='|', quotechar='"')
    shortparties = []
    for party in parties:
        p = tuple(party[:4])
        shortparties.append(p)
        
    for abbrev, name, tendency, info in shortparties:
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

def insert_governments(csvfile=os.path.join(DATASET_DIR, GOVERNMENT_FILE)):
    import dateutil.parser
    print 'A processar governos...'

    members = csv.reader(open(csvfile), delimiter='|', quotechar='"')
    for gov_number, mp_id, name, post, date_started, date_ended in members:
        if gov_number == 'Governo':
            # ignorar primeira linha
            continue
        gov_number = int(gov_number.replace('GC', ''))
        ds = dateutil.parser.parse(date_started).date()
        de = dateutil.parser.parse(date_ended).date()
        print name

        if Government.objects.filter(number=gov_number):
            gov = Government.objects.get(number=gov_number)
            if ds < gov.date_started:
                gov.date_started = ds
                gov.save()
            if de > gov.date_ended:
                gov.date_ended = de
                gov.save()

        else:
            gov = Government.objects.create(number=gov_number, date_started=ds, date_ended=de)

        if mp_id:
            mp_id = int(mp_id)
            if MP.objects.filter(id=mp_id):
                print 'Creating post'
                GovernmentPost.objects.create(mp=MP.objects.get(id=int(mp_id)),
                                              government=gov,  
                                              name=post,
                                              date_started=ds,
                                              date_ended=de)
            else:
                print 'No MP with given ID (%d)' % mp_id
                GovernmentPost.objects.create(mp=None,
                                              person_name=name,
                                              government=gov,  
                                              name=post,
                                              date_started=ds,
                                              date_ended=de)

def update_mps():
    for mp in MP.all_objects.all():
        mp.update_current_mandate()
        mp.update_current_party()

if __name__ == '__main__':
    check_for_files()
    insert_mps()
    '''
    insert_mp_gender()
    insert_facts()
    insert_mandate()
    insert_activities()
    insert_linksets()
    insert_shortnames()
    insert_parties()
    insert_governments()
    update_mps()
    '''
