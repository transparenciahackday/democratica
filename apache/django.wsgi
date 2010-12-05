#!/usr/bin/env python

import os
import sys

path = '/home/rlafuente/code/transparencia/repo/dptd'
if path not in sys.path:
    sys.path.append(path)
    sys.path.append(os.path.join(path, 'dptd/'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'dptd.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

