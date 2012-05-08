import datetime

from django.conf import settings as django_settings


def settings(request):
    """Access the settings in the templates"""
    return {'settings': django_settings}

def now(request):
    return {'now': datetime.datetime.now()}
