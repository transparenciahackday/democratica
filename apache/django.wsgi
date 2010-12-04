#!/usr/bin/env python

import os
import sys

ROOT_PATH = '/home/rlafuente/Dropbox/hacklaviva/transparencia/'
PROJECT_NAME = 'dptd'

if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)
    sys.path.append(os.path.join(ROOT_PATH, PROJECT_NAME + '/'))
os.environ['DJANGO_SETTINGS_MODULE'] = PROJECT_NAME + '.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

