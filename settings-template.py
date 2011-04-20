# -*- coding: utf-8 -*-

# Configuração do demo.cratica
# Em apenas dois passos, o demo.cratica estará configurado para o teu computador.

# 1. Localização dos directórios
# É só mudar os directórios aqui em baixo, relativamente ao directório democratica/.

# Localização do repositório dos datasets
PATH_DATASETS = '../datasets'

# Localização do repositório dos scripts do Transparência
PATH_REPO_TRANSPARENCIA = '../transparencia-porto'

# 2. Configuração da base de dados

# Tipo da base de dados
# Pode ser 'mysql', 'postgresql_psycopg2' ou 'sqlite3'
DB_TYPE = 'mysql'

# Nome da BD
DB_NAME = 'democratica'
# Nome do utilizador da BD
DB_USER = 'user'
# Palavra-passe do utilizador da BD
DB_PASSWORD = 'pass'

# Hostname da BD (vazio = localhost)
DB_HOST = ''
# Porta da BD (vazio = valor por omissão da BD)
DB_PORT = ''

# Já não é preciso mudar mais nada a seguir! ##
#
# Corre o script para inicializar a base de dados:
#   ./reset.sh
#
# Vai demorar um pouco; se tiveres erros, confirma que os directórios
# acima indicados estão correctos! Senão, vem avisar-nos desse bug.
#
# Agora corre o comando
#   python manage.py runserver
#
# E no teu browser, acede ao endereço
#   http://127.0.0.1:8000
#
# E se tudo estiver correcto, verás a página de abertura do demo.cratica.

#########################################################################

DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os

BASE_DIR = os.path.dirname(__file__)

DATASET_DIR = os.path.join(BASE_DIR, PATH_DATASETS)
PHOTO_DIR = os.path.join(DATASET_DIR, 'fotos_deputados/')
TRANSCRIPTS_DIR = os.path.join(DATASET_DIR, 'transcricoes/csv/')
FEMALE_NAMES_FILE = os.path.join(PATH_REPO_TRANSPARENCIA, 'php-utils/nomes_f_unicode.txt')
STOPWORD_FILE = os.path.join(BASE_DIR, 'core/stopwords.txt')

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

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = 'http://localhost:8000/media/'
ADMIN_MEDIA_PREFIX = '/admin-media/'
SECRET_KEY = 'u=+o$bugq9iiq0@3=-y#5ahm%r6pxo=3*qvqp7in0w1donajl8'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'democratica.urls'
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates/'))

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.databrowse',
    'democratica.core',
    'democratica.deputados',
    'democratica.dar',
    'django_extensions',
)

