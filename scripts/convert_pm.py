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

from democratica.deputados.models import MP
from democratica.dar.models import Entry

print 'A converter intervenções do PM...'
print 
mp = MP.objects.get(id=285)
print mp
for entry in Entry.objects.filter(speaker__contains='rimeiro'):
    entry.mp = mp
    entry.save()

