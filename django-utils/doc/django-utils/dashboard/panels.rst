Panel-writing guide
===================

Panels are the heart of the dashboard app.  They work like any other plugin
framework in django (the admin site, for instance) by providing a base class
which you must extend and then register.

Example
-------

An example from :mod:`djutils.dashboard.contrib.panels`:

.. code-block:: python

    from djutils.dashboard.provider import PanelProvider
    from djutils.dashboard.registry import registry
    
    class CPUInfo(PanelProvider):
        def get_title(self):
            return 'CPU Usage'
        
        def get_data(self):
            fh = open('/proc/loadavg', 'r')
            contents = fh.read()
            fh.close()
            
            # grab the second value
            first = contents.split()[0]
            
            return {'loadavg': first}
    
    # make sure that, when the queue updates all the panels, ours is included
    registry.register(CPUInfo)

As you can see, there are two methods that must be overridden:

* :py:meth:`get_title`
* :py:meth:`get_data`

As far as writing custom panels, anything goes.  No parameters are provided to 
the :py:meth:`get_data` method, so your
panel should be able to get whatever data it needs without any sort of intervention.
Since it's all python, you can use libraries to query the status of external
services like Redis or Memcached.  You can read files from the disk to extract
information on CPU load.  You can also access django models.  Here's a panel
which would display logins across the site:

.. code-block:: python

    import datetime
    from django.contrib.auth.models import User
    
    from djutils.dashboard.provider import PanelProvider
    from djutils.dashboard.registry import registry
    
    class LoginPanel(PanelProvider):
        def get_title(self):
            return 'Site logins'
        
        def get_data(self):
            last_minute = datetime.datetime.now() - datetime.timedelta(seconds=60)
            return {
                'logins': User.objects.filter(last_login__gt=last_minute).count()
            }
    
    registry.register(LoginPanel)

Multiple labels and points can be returned by the :py:meth:`get_data` method and will be
plotted on the same graph using a different colored line.
