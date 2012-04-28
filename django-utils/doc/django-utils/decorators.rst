Decorators
==========

.. py:module:: djutils.decorators

A handful of general-purpose decorators.

.. py:function:: cached_for_model(cache_timeout=300)

    Model method decorator that caches the return value for the given time.
    Similar to :func:`memoize` but uses the cache and is designed for use
    on model instances
    
    Usage::
    
        class MyModel(models.Model):
            ...
            
            @cached_for_model(60)
            def get_expensive_data(self, some_arg):
                # do expensive calculations here
                return data

.. py:function:: throttle(methods_or_func, limit=3, duration=900)

    Throttle the given function, returning 403s if limit exceeded
    
    Example::
    
        # limit to 5 POST or PUT requests per 5 minutes:
        
        @throttle(['POST', 'PUT'], 5, 300)
        def my_view(request, ...):
            # do some stuff
    
    
        # limit to 3 POST requests per 15 minutes:
    
        @throttle
        def my_other_view(request, ...):
            # do some other stuff

.. py:function:: memoize(func)

    avoid repeating the calculation of results for previously-processed inputs

    Example::
    
        @memoize
        def calculate_big_number(input1, input2):
            # do some complicated stuff
            return result

.. py:function:: async(func)

    Execute the function asynchronously in a separate thread
    
    Example::
    
        @async
        def send_email(to, subj, body):
            # this will be executed in a separate thread
            mail([to], subj, body)
