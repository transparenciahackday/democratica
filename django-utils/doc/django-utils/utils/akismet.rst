Akismet
=======

.. py:module:: djutils.utils.akismet

A simple client to use for communicating with the Akismet spam-catching
service.

You can sign up for access to their API here: https://akismet.com/signup/#free

The :class:`AkismetClient` class supports API key verification and checking
arbitrary text for spam.

.. py:class:: AkismetClient(object)

    .. py:method:: __init__(self, key, blog_url)
    
        :param key: the API key for accessing Akismet
        :param blog_url: the URL to the wordpress blog you used to register key (can be '')
    
    .. py:method:: verify_key(self)
        
        returns True/False whether the key provided is valid, defaulting to 
        False in the event of *any* error condition.
    
    .. py:method:: is_spam(self, comment, ip, author='', email='')

        :param comment: the comment text, contact email, whatever you want to check
        :param ip: the IP address the content originated from
        :param author: the name provided by the end user
        :param email: the email address provided by the end user
        
        Determine whether the comment is spam, returns True/False, defaulting to
        False in the event of *any* error condition
