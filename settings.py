# -*- coding: utf-8 -*-

from localsettings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
if DEBUG:
    TEMPLATE_STRING_IF_INVALID = 'LOOKUP FAILED'

import os

BASE_DIR = os.path.dirname(__file__)

PATH_DATASETS = os.path.abspath(PATH_DATASETS)
PATH_REPO_TRANSPARENCIA = os.path.abspath(PATH_REPO_TRANSPARENCIA)
 
DATASET_DIR = PATH_DATASETS
PHOTO_DIR = os.path.join(DATASET_DIR, 'fotos_deputados/')
TRANSCRIPTS_DIR = os.path.join(DATASET_DIR, 'transcricoes/csv/')
FEMALE_NAMES_FILE = os.path.join(os.path.abspath(PATH_REPO_TRANSPARENCIA), 'scripts/php-utils/nomes_f_unicode.txt')
STOPWORD_FILE = os.path.join(BASE_DIR, 'core/stopwords.txt')

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.%s' % DB_TYPE, 
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

ADMINS = ( ('Ricardo Lafuente', 'bollecs@sollec.org'),)
MANAGERS = ADMINS

TIME_ZONE = 'Europe/Lisbon'
LANGUAGE_CODE = 'pt-PT'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(BASE_DIR, '/media/')
ADMIN_MEDIA_PREFIX = 'http:/localhost:8000/admin-media/'
SECRET_KEY = 'u=+o$bugq9iiq0@3=-y#5ahm%r6pxo=3*qvqp7in0w1donajl8'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.request',
                               'django.contrib.messages.context_processors.messages',
                               'django.contrib.auth.context_processors.auth')

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'democratica.urls'
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates/'))

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'democratica.core',
    'democratica.deputados',
    'democratica.dar',
    'democratica.elections',
    'django_extensions',
    'haystack',
    'south',
    'debug_toolbar',
    'kombu.transport.django',  
    'djcelery',
    'reversion',
    'tastypie',
)  
  
STATIC_URL = '/media/'

# Celery
BROKER_URL = "django://" # tell kombu to use the Django database as the message queue  
CELERY_IMPORTS = ("dar.tasks",)
import djcelery  
djcelery.setup_loader() 
# Haystack 2.0 stuff, but we're using 1.2.7
'''
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.xapian_backend.XapianEngine',
        'PATH': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'xapian_index'),
        },
    }
'''
HAYSTACK_SITECONF = 'democratica.search_sites'
HAYSTACK_SEARCH_ENGINE = 'xapian'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 100
# HAYSTACK_CUSTOM_HIGHLIGHTER = 'democratica.dar.utils.MyHighlighter'

DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False} 

GRAPPELLI_INDEX_DASHBOARD = 'democratica.dashboard.CustomIndexDashboard'
