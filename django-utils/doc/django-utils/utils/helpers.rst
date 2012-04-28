Helpers
=======

.. py:module:: djutils.utils.helpers

This module contains a few helper functions that are frequently copy/pasted
between projects.  Kind of a mixed bag.

.. py:function:: load_class(path)

    dynamically load a class given a string of the format "package.Class"
    
    ::
    
        BackendClass = load_class('djutils.queue.backends.database.DatabaseBackend')

.. py:function:: generic_autodiscover(module_name)

    I have copy/pasted this code too many times...Dynamically autodiscover a
    particular module_name in a django project's INSTALLED_APPS directories,
    a-la django admin's autodiscover() method.
    
    Usage::
    
        generic_autodiscover('commands') # find all commands.py and load 'em
