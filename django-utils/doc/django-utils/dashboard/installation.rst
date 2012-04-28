Installation
============

First install the source code:
------------------------------

`pip install djutils`


Configure settings.py
---------------------

Add the following to your :envvar:`INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        # required
        'djutils', # makes the djutils task queue available
        'djutils.dashboard', # makes the dashboard available
        
        # optional
        'djutils.dashboard.contrib', # some default panels, like CPU avg
    ]

Add to the root urlconf
-----------------------

Like the admin site, it's a convention to add any autodiscovery code in the urls.
Since the dashboard app needs to go through all your apps looking for panels,
its probably a good idea to explicitly autodiscover them.

.. code-block:: python

    from djutils import dashboard
    dashboard.autodiscover()
    
    urlpatterns = patterns('',
        ...
        (r'^dashboard/', include('djutils.dashboard.urls')),
    )

Start the task queue
--------------------

Most importantly, you need to run the queue consumer provided with django-utils

`django-admin.py queue_consumer`

The dashboard app provides the necessary tasks to handle updating all the panels
and aggregating the hourly and daily data.

Check the :mod:`djutils.management.commands.queue_consumer` docs
for more information on running the consumer, including how to run it with
a process manager like `supervisord <http://supervisord.org>`_.

Static and External media
-------------------------

The project depends on two javascript libraries:

* dashboard.js, which is bundled with the project and can be found in the static/ folder
* flot.js, a 3rd party app available `here <http://code.google.com/p/flot/>`_

A note on using the contrib panels
----------------------------------

If you end up using the contrib panels, there are a couple of settings you'll
need to configure to get access to certain panels:

* redis panels, add `DASHBOARD_REDIS_CONNECTION = 'host:port'`
* memcached panels, add `DASHBOARD_MEMCACHED_CONNECTION = 'host:port'`
* postgresql panels, use the postgresql_psycopg2 database backend
