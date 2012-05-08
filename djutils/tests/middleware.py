from djutils.middleware import SubdomainMiddleware
from djutils.test import RequestFactoryTestCase


class SubdomainMiddlewareTestCase(RequestFactoryTestCase):
    def test_subdomain_middleware(self):
        middleware = SubdomainMiddleware()
        
        request = self.request_factory.get('/')
        request.META['HTTP_HOST'] = 'http://example.com'
        middleware.process_request(request)
        self.assertEqual(request.subdomain, None)
        
        request = self.request_factory.get('/')
        request.META['HTTP_HOST'] = 'http://test.example.com'
        middleware.process_request(request)
        self.assertEqual(request.subdomain, 'test')
        
        request = self.request_factory.get('/')
        request.META['HTTP_HOST'] = 'http://final.test.example.com'
        middleware.process_request(request)
        self.assertEqual(request.subdomain, 'final.test')
