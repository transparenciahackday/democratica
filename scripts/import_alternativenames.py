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
ALTERNATIVENAMES_FILE = 'deputados-nomes-alternativos.csv'

def check_for_files():
    all_files = [ALTERNATIVENAMES_FILE]
    
    for f in all_files:
        path = os.path.join(DATASET_DIR, f)
        if not os.path.exists(path):
            print 'File %s not found! Check this and try again.' % (f)
            sys.exit()

import csv
from democratica.deputados.models import MP

def insert_aka(csvfile=os.path.join(DATASET_DIR, ALTERNATIVENAMES_FILE)):
    print 'A processar nomes alternativos...'
    altnames = csv.reader(open(csvfile), delimiter=',', quotechar='"')
    for id, aka_1, aka_2 in altnames:
        mp = MP.objects.get(id=int(id))
        mp.aka_1 = aka_1
        if aka_2:
            mp.aka_2 = aka_2
        mp.save()

if __name__ == '__main__':
    check_for_files()
    insert_aka()
