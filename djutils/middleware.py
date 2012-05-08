import re
import urlparse

from django.conf import settings


class IgnoreCsrfMiddleware(object):
    """
    CSRF middleware can EABOD - this cripples it
    """
    def process_request(self, request):
        request.csrf_processing_done = True


class SubdomainMiddleware:
    """
    Store the subdomain on the request object
    """
    def process_request(self, request):
        if 'HTTP_HOST' in request.META:
            host = request.META['HTTP_HOST']
            split_url = urlparse.urlsplit(host)
            tld_bits = split_url.netloc.rsplit('.', 2)
            request.subdomain = len(tld_bits) == 3 and tld_bits[0] or None


class ProxyIPMiddleware(object):
    """
    Fix REMOTE_ADDR header when using a proxy
    """
    def process_request(self, request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            request.META['REMOTE_ADDR'] = request.META['HTTP_X_FORWARDED_FOR']
