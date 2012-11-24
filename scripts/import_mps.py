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
        c, created = Constituency.objects.get_or_create(name=name)
        c.article = article
        c.save()
    # importar dados dos deputados
    mps = json.loads(open(jsonfile, 'r').read())
    for id in mps:
        name = mps[id]['name']
        shortname = mps[id]['shortname']
        if mps[id].get('birthdate'):
            dob = dateutil.parser.parse(mps[id]['birthdate']).date()
        else:
            dob = None
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

        mp, mp_created = MP.objects.get_or_create(id = int(id))
        mp.name = name
        mp.shortname = shortname
        mp.dob = dob
        mp.occupation = occupation
        mp.jobs = jobs
        mp.education = education
        mp.commissions = commissions
        mp.save()

        if mp_created: print mp.shortname
        # criar mandatos para deputado
        from pprint import pprint
        mandate_dicts = mps[id]['mandates']
        for mandate in mandate_dicts:
            mdict = mandate
            m, m_created = Mandate.objects.get_or_create(mp=mp, 
                    legislature = Legislature.objects.get_or_create(number=mdict['legislature'])[0], 
                    constituency = Constituency.objects.get(name=mdict['constituency']), 
                    party = Party.objects.get_or_create(abbrev=mdict['party'])[0],)
            m.date_begin = dateutil.parser.parse(mdict['start_date']).date()
            m.date_end = dateutil.parser.parse(mdict['end_date']).date() if mdict['end_date'] else None
            m.save()
                        
        mp.update_current_mandate()
        mp.update_current_party()

if __name__ == '__main__':
    check_for_files()
    insert_mps()
