Cache
=====

.. py:module:: djutils.cache

.. py:function:: cached_filter(func, timeout=300)

    Decorator for creating a cached template filter.
    
    Usage::
    
        @register.filter
        @cached_filter
        def expensive_filter(value):
            ... do something expensive

.. py:class:: CachedNode(template.Node)

    Base class for creating cached template Nodes.  This class is designed to
    not dogpile in the event a cache key expires.  Suppose the data takes 3
    seconds to calculate and you get 100 requests/s, that's ~300 hits.  This
    class provides several ways to avoid this problem, either by blocking until
    the cache has been repopulated or by return an empty result.
    
    To avoid dogpiling the time the cached data expires is stored along with
    the cached data and if it is nearing expiration, a *single* call is made
    that will repopulate the data (hopefully before it expires).
    
    There are a number of ways you can configure the operation of this class:
    
    .. py:attribute:: cache_timeout = 60
    
        The default time to store data in the cache
    
    .. py:attribute:: aggressive = True
    
        Whether or not to block when cache is populating
    
    .. py:attribute:: use_spin_lock = False
    
        Whether to wait on repopulating call or fire off another call to the
        get_content method
    
    .. py:attribute:: backoff = (0.1, 1.1, 1.0)
    
        If using a spin-lock, initial time to sleep, rate of backoff, maximum
    
    .. py:method:: get_cache_key(self, context)
        
        return a unique cache key based on the available context
    
    .. py:method:: get_content(self, context)
    
        return any content -- what you would normally return in render()

.. py:class:: CachedContextNode(CachedNode)

    Similar to :class:`CachedNode` except that the :func:`get_content` method
    returns a dictionary of keys to update in the template context (as opposed
    to a block of text to render)
