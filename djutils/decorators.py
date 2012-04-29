import atexit
import Queue
import re
import time
import threading

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseForbidden, HttpResponseRedirect, Http404
from django.utils.functional import wraps

from djutils.cache import key_from_args


class EmptyObject(object):
    pass

def cached_for_model(cache_timeout=300):
    """
    Model method decorator that caches the return value for the given time.
    
    Usage::
    
        class MyModel(models.Model):
            ...
            
            @cached_for_model(60)
            def get_expensive_data(self, some_arg):
                # do expensive calculations here
                return data
    """
    def decorator(func):
        def cache_key_for_function(instance, *args, **kwargs):
            klass = type(instance)._meta.module_name
            hashed = key_from_args((args, kwargs))
            return 'djutils.%s.cached.%s.%s.%s.%s' % (
                settings.SITE_ID, klass, func.__name__, instance.pk, hashed
            )
        
        @wraps(func)
        def inner(self, *args, **kwargs):
            key = cache_key_for_function(self, *args, **kwargs)
            
            result = cache.get(key, EmptyObject)
            
            if result is EmptyObject or settings.DEBUG:
                result = func(self, *args, **kwargs)
                cache.set(key, result, cache_timeout)
            
            return result
        return inner
    return decorator

def throttle(methods_or_func, limit=3, duration=900):
    """
    Throttle the given function, returning 403s if limit exceeded
    
    Example::
    
        # limit to 5 POST or PUT requests per 5 minutes:
        
        @throttle(['POST', 'PUT'], 5, 300)
        def my_view(request, ...):
            # do some stuff
    
    
        # limit to 3 POST requests per 15 minutes:
    
        @throttle
        def my_other_view(request, ...):
            # ..self.
    """
    if callable(methods_or_func):
        methods = ('POST',)
    else:
        methods = methods_or_func
    
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if request.method in methods:
                remote_addr = request.META.get('HTTP_X_FORWARDED_FOR') or \
                              request.META.get('REMOTE_ADDR')
                
                if remote_addr:
                    key = re.sub(r'[^0-9\.]', '', remote_addr)
                    cached = cache.get(key)
                    
                    if cached == limit:
                        return HttpResponseForbidden('Try slowing down a little.')
                    elif not cached:
                        cache.set(key, 1, duration)
                    else:
                        cache.incr(key)
            
            return func(request, *args, **kwargs)
        return inner
    
    if callable(methods_or_func):
        return decorator(methods_or_func)
    
    return decorator

def staff_required(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404('Must be a staff user to access this url')
        return func(request, *args, **kwargs)
    return inner

def memoize(func):
    func._memoize_cache = {}
    @wraps(func)
    def inner(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        if key not in func._memoize_cache:
            func._memoize_cache[key] = func(*args, **kwargs)
        return func._memoize_cache[key]
    return inner

def worker_thread():
    while 1:
        func, args, kwargs = queue.get()
        try:
            func(*args, **kwargs)
        except:
            pass # <-- log error here
        finally:
            queue.task_done()

def async(func):
    """
    Execute the function asynchronously in a separate thread
    """
    @wraps(func)
    def inner(*args, **kwargs):
        queue.put((func, args, kwargs))
    return inner

queue = Queue.Queue()

for i in range(getattr(settings, 'DJANGO_UTILS_WORKER_THREADS', 1)):
    thread = threading.Thread(target=worker_thread)
    thread.daemon = True
    thread.start()

def cleanup():
    queue.join()

atexit.register(cleanup)
