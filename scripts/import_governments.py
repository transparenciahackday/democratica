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

def insert_governments(csvfile=os.path.join(DATASET_DIR, GOVERNMENT_FILE)):
    import dateutil.parser
    print 'A processar cargos em governos...'

    members = csv.reader(open(csvfile), delimiter='|', quotechar='"')
    for gov_number, mp_id, name, post, date_started, date_ended in members:
        if gov_number == 'Governo':
            # ignorar primeira linha
            continue
        gov_number = int(gov_number.replace('GC', ''))
        gov, created = Government.objects.get_or_create(number=gov_number)
        ds = dateutil.parser.parse(date_started).date()
        de = dateutil.parser.parse(date_ended).date()
        if created:
            gov.date_started = ds
            gov.date_ended = de
            gov.save()

        if GovernmentPost.objects.filter(government=gov, name=post, date_started=ds, date_ended=de):
            p = GovernmentPost.objects.filter(government=gov, name=post, date_started=ds, date_ended=de)[0]
        else:
            p = GovernmentPost.objects.create(government=gov, name=post, date_started=ds, date_ended=de)
        if mp_id:
            mp_id = int(mp_id)
            if MP.objects.filter(id=mp_id):
                p.mp = MP.objects.get(id=int(mp_id))
        else:
                p.person_name = name
        p.save()

if __name__ == '__main__':
    check_for_files()
    insert_governments()
