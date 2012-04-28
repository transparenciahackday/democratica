Test
====

.. py:module:: djutils.test

A handful of utilities for testing.


.. py:class:: RequestFactory(Client)

    Class that lets you create mock Request objects for use in testing.
    
    Adapted from Simon Willison's snippet: http://djangosnippets.org/snippets/963/
    
    Usage::
    
        rf = RequestFactory()
        get_request = rf.get('/hello/')
        post_request = rf.post('/submit/', {'foo': 'bar'})
    
    This class re-uses the django.test.client.Client interface, docs here:
    http://www.djangoproject.com/documentation/testing/#the-test-client
    
    Once you have a request object you can pass it to any view function, 
    just as if that view had been hooked up using a URLconf.

.. py:class:: RequestFactoryTestCase(TestCase)

    Class that uses the RequestFactory to make requests.
    
    .. py:method:: get(self, url, **data)
    
        makes a request to the given url passing in arbitrary data
    
    .. py:method:: post(self, url, **data)
    
        makes a POST request to the given url passing in arbitrary data
