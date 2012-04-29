from django.core.handlers.base import BaseHandler
from django.core.handlers.wsgi import WSGIRequest
from django.core.urlresolvers import get_resolver
from django.test import Client, TestCase as _TestCase


# Adapted from Simon Willison's snippet: http://djangosnippets.org/snippets/963/.
try:
    # Use Django 1.3's RequestFactory class.
    from django.test.client import RequestFactory
except ImportError:
    class RequestFactory(Client):
        """
        Class that lets you create mock Request objects for use in testing.
        
        Usage:
        
        rf = RequestFactory()
        get_request = rf.get('/hello/')
        post_request = rf.post('/submit/', {'foo': 'bar'})
        
        This class re-uses the django.test.client.Client interface, docs here:
        http://www.djangoproject.com/documentation/testing/#the-test-client
        
        Once you have a request object you can pass it to any view function, 
        just as if that view had been hooked up using a URLconf.
        """
        def request(self, **request):
            """
            Similar to parent class, but returns the request object as soon as it
            has created it.
            """
            environ = {
                'HTTP_COOKIE': self.cookies,
                'PATH_INFO': '/',
                'QUERY_STRING': '',
                'REQUEST_METHOD': 'GET',
                'SCRIPT_NAME': '',
                'SERVER_NAME': 'testserver',
                'SERVER_PORT': 80,
                'SERVER_PROTOCOL': 'HTTP/1.1',
            }
            environ.update(self.defaults)
            environ.update(request)
            request = WSGIRequest(environ)
            
            handler = BaseHandler()
            handler.load_middleware()
            for middleware_method in handler._request_middleware:
                if middleware_method(request):
                    raise Exception("Couldn't create request object - "
                                    "request middleware returned a response")
            
            return request


class TestCase(_TestCase):
    def assertQuerysetEqual(self, a, b):
        """
        From http://djangosnippets.org/snippets/2013/
        Assert iterable `a` has the same model instances as iterable `b`
        """
        return self.assertEqual(self._sort_by_pk(a), self._sort_by_pk(b))

    def _sort_by_pk(self, list_or_qs):
        annotated = [(item.pk, item) for item in list_or_qs]
        annotated.sort()
        return map(lambda item_tuple: item_tuple[1], annotated)


class RequestFactoryTestCase(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def request(self, req):
        resolver = get_resolver(None)
        func, args, kwargs = resolver.resolve(req.META['PATH_INFO'])
        return func(req, *args, **kwargs)
    
    def get(self, url, **data):
        return self.request(self.request_factory.get(url, data))
    
    def post(self, url, **data):
        return self.request(self.request_factory.post(url, data))
