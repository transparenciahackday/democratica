#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Script para criar os modelos de Eleições
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

import csv
import dateutil.parser
from democratica import settings
from democratica.elections.models import Election

print 'A importar datas de eleições...'
f = os.path.join(settings.DATASET_DIR, 'eleicoes-datas.csv')
lines = csv.reader(open(f), delimiter='|', quotechar='"')
for el_type, date in lines:
    d = dateutil.parser.parse(date, dayfirst=True)
    if Election.objects.filter(date=d):
        e = Election.objects.get(date=d)
        e.type = el_type
        e.date = d
        e.save()
    else:
        e = Election.objects.create(date=d, type=el_type)
    print el_type, d
