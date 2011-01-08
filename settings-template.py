# Configuração do demo.cratica
#
# É só mudar os directórios aqui em baixo:
# BASE_DIR: a raiz do projecto (directório dptd/)
# DATASET_DIR: onde estão os datasets
# TRANSCRIPTS_DIR: onde estão os CSV das transcrições
# 
# E logo a seguir, é mudar a configuração da base de dados, de acordo com o teu sistema
# Em princípio, só deves precisar de mudar o nome da base de dados, o user e a pass.

BASE_DIR = '/home/rlafuente/code/transparencia/repo/dptd/'
DATASET_DIR = '../../../datasets/'
TRANSCRIPTS_DIR = '../../../darscraper/csv'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dptd',                       # Or path to database file if using sqlite3.
        'USER': 'username',                   # Not used with sqlite3.
        'PASSWORD': 'password',               # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


## Já não é preciso mudar mais nada ##

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'Europe/Lisbon'
LANGUAGE_CODE = 'pt-PT'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = 'http://localhost:8000/media/'
ADMIN_MEDIA_PREFIX = '/admin-media/'
SECRET_KEY = 'u=+o$bugq9iiq0@3=-y#5ahm%r6pxo=3*qvqp7in0w1donajl8'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'dptd.urls'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates/')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.databrowse',
    'dptd.core',
    'dptd.deputados',
    'dptd.dar'
)

STOPWORD_FILE = os.path.join(BASE_DIR, 'core/stopwords.txt')
