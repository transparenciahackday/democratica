Middleware
==========

.. py:module:: djutils.middleware

.. py:class:: IgnoreCsrfMiddleware

    cripple django's CSRF middleware while leaving it installed (required for
    certain contrib apps)

.. py:class:: SubdomainMiddleware

    a request middleware that adds the subdomain to the request if the
    HOST header is present
