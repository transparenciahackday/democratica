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

if __name__ == '__main__':
    check_for_files()
    insert_linksets()
