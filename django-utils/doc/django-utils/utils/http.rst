HTTP Helpers
============

.. py:module:: djutils.utils.http

A couple of utility functions for working with HTTP requests and responses.

.. note:: requires httplib2

.. py:function:: fetch_url(url, parameters=None, http_method="GET", follow_redirects=True, timeout=4, user_agent='python-httplib2')
    
    Fetch the data at the given URL, with optional parameters.
    
    :param url: the URL to fetch
    :param parameters: a dictionary of parameters to include in request
    :param http_method: the type of HTTP request to make, default is GET
    :param follow_redirects: whether to follow 30x redirects
    :param timeout: set the socket timeout, which if reached will throw a socketerror
    :param user_agent: user agent string to send in headers

.. py:function:: json_response(context_dictionary)

    Serialize the context_dictionary as JSON and return a HttpResponse.  If
    the `DEBUG` setting is True, the mime_type is 'text/javascript', otherwise
    'application/json' will be used.
