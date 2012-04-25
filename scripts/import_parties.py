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
    all_files = [PARTIES_FILE]
    
    for f in all_files:
        path = os.path.join(DATASET_DIR, f)
        if not os.path.exists(path):
            print 'File %s not found! Check this and try again.' % (f)
            sys.exit()

import csv, json
import datetime, time

from democratica.deputados.models import *

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

if __name__ == '__main__':
    check_for_files()
    insert_parties()
