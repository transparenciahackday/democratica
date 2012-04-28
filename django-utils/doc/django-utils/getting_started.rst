Getting Started
===============


Installation
------------

First, you need to install django-utils.

There are a couple of ways:

Installing with pip
^^^^^^^^^^^^^^^^^^^

::

    pip install djutils
    
    or
    
    pip install -e git+https://github.com/coleifer/django-utils.git#egg=djutils


Installing via git
^^^^^^^^^^^^^^^^^^

::

    git clone https://github.com/coleifer/django-utils.git
    cd django-utils
    python setup.py test
    sudo python setup.py install


Adding to your Django Project
--------------------------------

After installing, adding django-utils to your projects is a snap.  Simply
add it to your projects' INSTALLED_APPs and run 'syncdb'::
    
    # settings.py
    INSTALLED_APPS = [
        ...
        'djutils'
    ]
