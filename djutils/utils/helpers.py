import sys
import threading

from django.utils.importlib import import_module


def load_class(path):
    """
    dynamically load a class given a string of the format
    
    package.Class
    """
    package, klass = path.rsplit('.', 1)
    module = import_module(package)
    return getattr(module, klass)


def generic_autodiscover(module_name):
    """
    I have copy/pasted this code too many times...Dynamically autodiscover a
    particular module_name in a django project's INSTALLED_APPS directories,
    a-la django admin's autodiscover() method.
    
    Usage:
        generic_autodiscover('commands') <-- find all commands.py and load 'em
    """
    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        try:
            import_module(app)
            app_path = sys.modules[app].__path__
        except AttributeError:
            continue
        try:
            imp.find_module(module_name, app_path)
        except ImportError:
            continue
        import_module('%s.%s' % (app, module_name))
        app_path = sys.modules['%s.%s' % (app, module_name)]


class ObjectDict(dict):
    def __getattr__(self, attname):
        try:
            return self[attname]
        except KeyError:
            raise AttributeError('%s has no attribute named "%s"' % (self, attname))
