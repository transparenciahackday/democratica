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
#FACTS_FILE = 'deputados-factos.csv'
#CAUCUS_FILE = 'deputados-legislaturas.csv'
ACTIVITIES_FILE = 'deputados-actividades.csv'
LINKSETS_FILE = 'deputados-links.csv'
PARTIES_FILE = 'partidos.csv'
#SHORTNAMES_FILE = 'deputados-nomes.csv'
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

if __name__ == '__main__':
    check_for_files()
    insert_activities()
