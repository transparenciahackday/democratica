Registering Panels and Autodiscovery
====================================

Only panels that have been registered can be displayed and updated, and since its
all python, only panels that have been imported can be registered.  Registration
is an explicit step and is done programmatically in python.  This code aims to
function in the same way as the django admin site.

Autodiscovery
-------------

By default, anything stored in a module named "panels.py" in the root directory
of an installed app, will be automatically imported.

To ensure that this automatic importing occurs add the following to your :envvar:`ROOT_URLCONF`:

.. code-block:: python

    from djutils import dashboard
    dashboard.autodiscover()

If you're familiar with Django's admin framework, this probably looks similar to:

.. code-block:: python

    from django.contrib import admin
    admin.autodiscover()


Registering panel providers
---------------------------

After declaring your custom panel class, be sure to register it.  If you're
familiar with the workflow of writing ModelAdmin classes and then registering them,
this should seem familiar:

.. code-block:: python

    from djutils.dashboard.provider import PanelProvider
    from djutils.dashboard.registry import registry
    
    
    class MyAwesomePanel(PanelProvider):
        def get_title(self):
            return 'Interesting data'
        
        def get_data(self):
            # this data is actually not interesting at all
            return {
                'value_a': 1,
                'value_b': 3
            }
    
    # register the panel class with the global registry
    registry.register(MyAwesomePanel)

.. note:: If you add a new panel class and do not see it in the dashboard, the
    first thing you should check is that it is being imported and registered.
