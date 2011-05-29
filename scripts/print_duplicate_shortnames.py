#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Mostrar quais os shortnames dos deputados que temos em duplicado. Normalmente o
parser lê o deputados-nomes.csv (está no repositório
transparencia-porto/datasets) e, caso não tenha shortname, calcula com o
primeiro e último. Este script serve pra completarmos o deputados-nomes.csv .

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

print 'Deputados com o mesmo shortname:'
print 

mps = MP.all_objects.all()
shortnames = frozenset(MP.all_objects.all().values_list('shortname', flat=True))

for n in shortnames:
    if mps.filter(shortname=n).count() > 1:
        print n
        for name in mps.filter(shortname=n).values_list('name', flat=True):
            print '   ' + name

