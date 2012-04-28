#!/usr/bin/env python
import sys
from os.path import dirname, abspath

from django.conf import settings

if len(sys.argv) > 1 and 'postgres' in sys.argv:
    sys.argv.remove('postgres')
    db_engine = 'postgresql_psycopg2'
    db_name = 'test_main'
    db_test_name = ''
else:
    db_engine = 'sqlite3'
    db_test_name = 'testing.db' # use a non-memory db for access across threads
    db_name = ''

if not settings.configured:
    settings.configure(
        DATABASES = {
            'default': {
                'NAME': db_name,
                'TEST_NAME': db_test_name,
                'ENGINE': db_engine,
            }
        },
        INSTALLED_APPS = [
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'djutils',
            'djutils.tests',
            'djutils.dashboard',
        ],
        SITE_ID = 1,
        CACHE_BACKEND = 'djutils.tests.cache_backend://',
        TEMPLATE_CONTEXT_PROCESSORS = ('djutils.context_processors.settings',),
        IGNORE_THIS = 'testing',
        QUEUE_CLASS = 'djutils.queue.backends.database.DatabaseQueue',
        QUEUE_NAME = 'testqueue',
        ROOT_URLCONF = 'djutils.dashboard.tests.urls',
        DASHBOARD_NO_SECURITY = True,
    )

from django.test.simple import run_tests


def runtests(*test_args):
    if not test_args:
        test_args = ['djutils', 'dashboard']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    failures = run_tests(test_args, verbosity=1, interactive=True)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
