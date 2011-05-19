#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Script para criar os modelos do Django a partir das transcrições do DAR
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
import datetime
from democratica.deputados.models import Session
from democratica.settings import DATASET_DIR

print 'A introduzir datas das legislaturas...'
print 
csvfile = os.path.join(DATASET_DIR, 'legislaturas.csv')
legs = csv.reader(open(csvfile), delimiter='|', quotechar='"')
for leg, year_start, year_end in legs:
    if leg.startswith('Núm'):
        continue
    year_start = int(year_start)
    s = Session.objects.get(number=leg)
    s.date_start = datetime.date(year=year_start, month=1, day=1)
    if year_end:
        year_end = int(year_end)
        s.date_end = datetime.date(year=year_end, month=1, day=1)
    s.save()

