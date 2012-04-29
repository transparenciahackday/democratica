try:
    import cPickle as pickle
except ImportError:
    import pickle
import time

from django import template
from django.conf import settings
from django.core.cache import cache
from django.db.models.query import QuerySet
from django.utils.encoding import smart_unicode, smart_str
from django.utils.functional import wraps
from django.utils.hashcompat import sha_constructor


class EmptyObject(object):
    pass


def prep_for_key(obj):
    "get a string representation of an object for hashing"
    return pickle.dumps(obj)

def key_from_args(*args, **kwargs):
    "generate a hash of the given args and kwargs"
    return sha_constructor(prep_for_key((args, kwargs))).hexdigest()

def cached_filter(func, timeout=300):
    """
    Decorator for creating a cached template filter.  Usage::
    
    @register.filter
    @cached_filter
    def expensive_filter(value):
        ... do something expensive
    """
    @wraps(func)
    def inner(*args, **kwargs):
        if settings.DEBUG:
            return func(*args, **kwargs)
        
        # generate a key based on args, similar to memoization
        cache_key = key_from_args(*args, **kwargs)
        
        # attempt to grab result from the cache
        result = cache.get(cache_key, EmptyObject)
        
        if result is EmptyObject:
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout)
        
        return result
    
    inner._decorated_function = func
    return inner


class CachedNode(template.Node):
    """
    Base class for creating cached template Nodes - implements two methods:
    
    get_cache_key(self, context) -> return a unique cache key
    get_content(self, context) -> what you would normally return in render()
    """
    cache_timeout = 60
    
    # whether or not to block when cache is populating
    aggressive = True
    
    # whether to wait on repopulating call or fire off another call to the
    # get_content() method
    use_spin_lock = False
    
    # if using a spin-lock, initial time to sleep, rate of backoff, maximum
    backoff = (0.1, 1.1, 1.0)
    
    def get_stale_time(self, value):
        # set the stale timeout to 75% of the tag's timeout
        stale = self.cache_timeout * .75
        
        # what time it will be when things are stale
        return time.time() + stale

    def cache_content(self, value):
        stale_time = self.get_stale_time(value)
        
        # return a tuple of content and stale time
        return (value, stale_time)
    
    def repopulating_key(self, original_key):
        # a cache key to indicate when the real cache data is being repopulated
        return 'repopulating.%s' % original_key
    
    def is_repopulating(self, original_key):
        # a boolean whether the cache is being repopulated
        return bool(cache.get(self.repopulating_key(original_key)))
        
    def repopulate(self, key, context):
        # set the repopulating_key, setting the timeout to the tag's timeout
        cache.set(self.repopulating_key(key), 1, self.cache_timeout)
        
        # load the content up and cache it, resetting the staleness time
        content = self.get_content(context)
        cache.set(key, self.cache_content(content), self.cache_timeout)
        
        # kill the repopulating key
        cache.delete(self.repopulating_key(key))
        
        return content

    def render(self, context):
        if settings.DEBUG:
            return self.get_content(context)
        
        key = self.get_cache_key(context)
        
        # try to load the data from the cache
        data = cache.get(key, EmptyObject)
        
        if data is not EmptyObject:
            # unpack and check if the data is stale
            content, stale_time = data
            
            if stale_time <= time.time() and not self.is_repopulating(key):
                # repopulate the cache as it will be expiring soon
                content = self.repopulate(key, context)
        else:
            if not self.aggressive and self.is_repopulating(key):
                # return an empty string
                content = ''
            else:
                if self.use_spin_lock:
                    interval, backoff, maximum = self.backoff
                    
                    while self.is_repopulating(key) and interval < maximum:
                        time.sleep(interval)
                        interval *= backoff
                
                from_cache = cache.get(key)
                
                if from_cache:
                    content = from_cache[0]
                else:
                    content = self.repopulate(key, context)
        
        return content

    def get_cache_key(self, context):
        raise NotImplementedError

    def get_content(self, context):
        raise NotImplementedError


class CachedContextNode(CachedNode):
    """
    Rather than rendering a string, add some variables to the template context.
    
    get_content(self, context) -> return dictionary of variables to update
    """
    def render(self, context):
        rendered = super(CachedContextNode, self).render(context)
        if rendered:
            for k, v in rendered.items():
                context[k] = v
        return ''
