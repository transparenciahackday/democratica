Queue
=====

.. py:module:: djutils.queue

A simple task queue and consumer to make processing tasks out-of-band painless.
Ideal for sending email, checking items for spam, generating thumbnails, etc.

The :mod:`Queue` module is divided up into several components, but for
almost all use-cases, you will only use the :func:`queue_command` decorator
found in :mod:`djutils.queue.decorators`


Executing tasks out-of-process
------------------------------

.. py:module:: djutils.queue.decorators

For the simple case, you need only write a function, decorate it with the
:func:`queue_command` decorator and call it as you normally would.  Instead
of executing immediately and potentially blocking, the function will be
enqueued and return immediately afterwards.

::
    
    ### app/commands.py
    
    from djutils.queue.decorators import queue_command

    @queue_command
    def churn_data(model_instance, some_data, another_value):
        # this function will do some expensive processing, and so
        # should happen outside the request/response cycle.
        
        important_results = model_instance.process_data(some_value, another_value)
        model_instance.propogate_results(important_results)

Here's how you might call your function::

    ### app/views.py ###
    
    from django.http import HttpResponse
    
    from app.commands import churn_data

    def data_processing_view(request, some_val, another_val):
        # assume we load up an object based on some parameter passed in
        # to the view.  also, the view gives us a payload of data.  we
        # want the object to churn that data in the background using the
        # function above:
        churn_data(my_object, request.POST['payload'], another_val)
        return HttpResponse('Churning in background task added to queue')

Whenever the view gets called, the function will be enqueued for execution.
Meanwhile the :class:`QueueConsumer` will pick it up and execute it in a separate
process.

When the consumer picks up the message, it will churn your data!

.. warning:: You can pass anything in to the decorated function *as long as it is pickle-able*.

.. warning:: Your decorated functions must be loaded into memory by the consumer -
    to ensure that this happens it is good practice to put all :func:`queue_command`
    decorated functions in a module named :mod:`commands.py` so the autodiscovery
    bits will pick them up.


Executing tasks on a schedule
-----------------------------

Sometimes it may be necessary to run a certain bit of code every so often,
irrespective of some triggering event.  If you've used the linux crontab before,
then you're already familiar with the idea.

djutils provides two functions to help write periodic commands::

    from djutils.queue.decorators import periodic_command, crontab
    
    @periodic_command(crontab(hour='0', minute='0'))
    def send_daily_digest():
        # send out a daily email at midnight
    
    @periodic_command(crontab(day_of_week='0', hour='5,17', minute='0'))
    def send_sunday_editions():
        # send out an email every sunday, once at 5am, once at 5pm

Remember to put any periodic commands you write in a file named **commands.py**
to ensure that they're picked up by the consumer.

.. warning:: functions decorated with @periodic_command should not accept
    any parameters

.. note:: Tasks can be run with a minimum resolution of 1 minute.

.. note:: The :func:`periodic_command` decorator is a bit different than the :func:`queue_command`
    decorator.  Rather than causing the function be enqueued upon execution, it will
    execute normally and not be enqueued.  The purpose of the decorator is to
    create a :class:`PeriodicQueueCommand` and register it with the global invoker.  The
    invoker then handles running any :class:`PeriodicQueueCommand` instances according
    to schedule.

.. py:function:: queue_command(func)

    function decorator that causes the decorated function to be enqueued for
    execution when called
    
    Usage::
    
        from djutils.queue.decorators import queue_command
        
        @queue_command
        def run_this_out_of_process(some_val, another_val)
            # whenever called, will be run by the consumer instead of in-process

.. py:function:: periodic_command(validate_datetime)

    Decorator to execute a function on a specific schedule.  This is a bit
    different than :func:queue_command in that it does *not* cause items to
    be enqueued when called, but rather causes a :class:`PeriodicQueueCommand` to be
    registered with the global invoker.
    
    Since the command is called at a given schedule, it cannot be "triggered"
    by a run-time event.  As such, there should never be any need for 
    parameters, since nothing can vary between executions.
    
    The :param:`validate_datetime` parameter
    
    Usage::
    
        from djutils.queue.decorators import crontab, periodic_command
        
        @periodic_command(crontab(day='1', hour='0', minute='0'))
        def run_at_first_of_month():
            # run this function at midnight on the first of the month


.. py:function:: crontab(month='*', day='*', day_of_week='*', hour='*', minute='*')

    Convert a "crontab"-style set of parameters into a test function that will
    return True when the given datetime matches the parameters set forth in
    the crontab.
    
    Acceptable inputs:
    
    - \* = every distinct value
    - \*/n = run every "n" times, i.e. hours='*/4' == 0, 4, 8, 12, 16, 20
    - m-n = run every time m..n
    - m,n = run on m and n


Autodiscovery
-------------

The :mod:`djutils.queue.registry` stores references to all :class:`QueueCommand`
classes (this includes any function decorated with :func:`queue_command`).  The
consumer needs to "discover" your commands in order to process them, so it is
recommended that you put all your code that needs to be processed via the Queue
in files named :mod:`commands.py`, much like django's admin processes files
named :mod:`admin.py`.

To manually discover commands, execute::

    >>> from djutils import queue; queue.autodiscover()


Consuming Messages
------------------

.. py:module:: djutils.management.commands.queue_consumer

The :mod:`djutils.management.commands.queue_consumer` management command consumes
messages from the queue and delegates the work to an arbitrary number of worker
threads.  The consumer runs in the foreground.

To run the consumer, you will need to ensure that two environment variables
are properly set:

    * PYTHONPATH: a list of directories in which to find python packages
    * DJANGO_SETTINGS_MODULE: the location of the settings file your django project uses

Then it is as simple as::

    django-admin.py queue_consumer


Useful consumer switches
^^^^^^^^^^^^^^^^^^^^^^^^

"-t" or "--threads"
    controls how many worker threads to use.  If your tasks are
    CPU bound you probably won't see much benefit from multiple threads due to
    the GIL, but if you plan on doing I/O in your tasks multi-threading can give
    you a big boost!

"-n" or "--no-periodic"
    turns off the periodic task scheduler.  If you have no
    periodic tasks feel free to turn this off.  Also, if you plan on running multiple
    consumers, only one should be enqueueing periodic tasks.

"-l" or "--logfile"
    specifies where to store logfile


Example assuming you use virtualenv
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    # assume your cwd is the root dir of virtualenv
    export DJANGO_SETTINGS_MODULE=mysite.settings
    django-admin.py queue_consumer -l ./logs/queue.log


Example running as root
^^^^^^^^^^^^^^^^^^^^^^^

::

    sudo su
    export PYTHONPATH=/path/to/site/:/path/to/djutils/:$PYTHONPATH
    export DJANGO_SETTINGS_MODULE=mysite.settings
    django-admin.py queue_consumer --logfile=/var/log/site-queue.log --threads=4


Sample supervisord script
^^^^^^^^^^^^^^^^^^^^^^^^^

My person preference is to run the queue with a process manager like `supervisor <http://supervisord.org/>`_.
Here's what my script looks like::

    [program:queue_spiders]
    environment=PYTHONPATH="/home/code/envs/spiders/:$PYTHONPATH"
    directory=/home/code/envs/spiders/
    command=/home/code/envs/spiders/bin/django-admin.py queue_consumer --settings=spiders.settings -l logs/queue.log --verbosity=2 -t 2
    user=code
    autostart=true
    autorestart=true


What happens if one of my tasks blows up?
-----------------------------------------

The consumer will maintain as many worker threads as you specify.  If an error
occurs while processing a message, the following occurs:

* the error and traceback are logged, along with the thread id of the worker
* that worker is taken out of the pool
* a new worker is started up to replace it

The message itself, though, is gone forever.  If you want to receive an error
email whenever a task dies, I'd recommend checking out the `new django logging
handlers <https://docs.djangoproject.com/en/dev/topics/logging/>`_ -- you can
configure the `djutils.queue.logger` to use the mail_admins handler for loglevel
of ERROR.


Backends
--------

.. py:module:: djutils.queue.backends.base

Currently I've only written two backends, the :class:`djutils.queue.backends.database.DatabaseQueue`
which stores messages in the db using django's ORM and the `djutils.queue.backends.redis_backend.RedisQueue`
whish uses `redis <http://redis.io>`_ to store messages.  I plan on adding additional
backends, but if you'd like to write your own there are just a few methods that
need to be implemented.


.. py:class:: class BaseQueue(object)

    .. py:method:: __init__(self, name, connection)

        Initialize the Queue - this happens once when the module is loaded

    .. py:method:: write(self, data)

        Push 'data' onto the queue
    
    .. py:method:: read(self)

        Pop data from the queue.  An empty queue should not raise an Exception!
    
    .. py:method:: flush(self)

        Delete everything from the queue

    .. py:method:: __len__(self)
    
        Number of items in the queue


.. py:module:: djutils.queue.backends.database

.. py:class:: class DatabaseQueue(BaseQueue)

    ::

        QUEUE_CLASS = 'djutils.queue.backends.database.DatabaseQueue'
        QUEUE_CONNECTION = '' # <-- no connection needed as it uses django's ORM

.. py:module:: djutils.queue.backends.redis_backend

.. py:class:: class RedisQueue(BaseQueue)

    ::

        QUEUE_CLASS = 'djutils.queue.backends.redis_backend.RedisQueue'
        QUEUE_CONNECTION = '10.0.0.75:6379:0' # host, port, database-number

.. py:class:: class RedisBlockingQueue(RedisQueue)

    An experimental queue that uses Redis' blocking right pop operation to
    pull messages from the queue rather than polling for updates.  Should work
    identical to RedisQueue in all other regards, including configuration.
