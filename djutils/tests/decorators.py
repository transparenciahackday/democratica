import Queue
import time
import threading

from django.core.cache import cache
from django.db import models
from django.http import HttpResponseForbidden

from djutils.decorators import async, memoize, throttle, cached_for_model
from djutils.test import RequestFactoryTestCase, TestCase
from djutils.tests.models import Simple


class ThrottleDecoratorTestCase(RequestFactoryTestCase):
    def test_throttle_decorator(self):
        get_request = self.request_factory.get('/')
        post_request = self.request_factory.post('/')
        
        get_request.META['REMOTE_ADDR'] = '127.0.0.1'
        post_request.META['REMOTE_ADDR'] = '127.0.0.1'
        
        # test first with no args
        @throttle
        def test_view(request, some_field):
            return some_field
        
        ten_gets = [test_view(get_request, 'test') for i in range(10)]
        self.assertEqual(['test'] * 10, ten_gets)
        
        ten_posts = [test_view(post_request, 'test') for i in range(10)]
        self.assertNotEqual(['test'] * 10, ten_posts)
        
        first_three, denied = ten_posts[:3], ten_posts[3:]
        self.assertEqual(['test'] * 3, first_three)
        self.assertTrue(all(isinstance(r, HttpResponseForbidden) for r in denied))
        
        cache.delete('127.0.0.1')
        
        # test throttle with some args now
        @throttle(('GET', 'POST'), 5)
        def test_view(request, some_field):
            return some_field
        
        ten_gets = [test_view(get_request, 'test') for i in range(10)]
        self.assertNotEqual(['test'] * 10, ten_gets)
        
        first_five, denied = ten_gets[:5], ten_gets[5:]
        self.assertEqual(['test'] * 5, first_five)
        self.assertTrue(all(isinstance(r, HttpResponseForbidden) for r in denied))
        
        cache.delete('127.0.0.1')
        
        ten_posts = [test_view(post_request, 'test') for i in range(10)]
        self.assertNotEqual(['test'] * 10, ten_posts)
        
        first_five, denied = ten_posts[:5], ten_posts[5:]
        self.assertEqual(['test'] * 5, first_five)
        self.assertTrue(all(isinstance(r, HttpResponseForbidden) for r in denied))


class DelayTestCase(TestCase):
    def test_delay_decorator(self):
        values_queue = Queue.Queue()
        write_lock = threading.Lock()
        
        @async
        def add_value(q, value):
            write_lock.acquire()
            values_queue.put(value)
            write_lock.release()
        
        write_lock.acquire()
        add_value(values_queue, 'test')
        self.assertEqual(values_queue.qsize(), 0)
        
        write_lock.release()
        time.sleep(.05) # <- give the worker a moment
        self.assertEqual(values_queue.qsize(), 1)
        
        self.assertEqual(values_queue.get(), 'test')


class MemoizeTestCase(TestCase):
    def test_memoize_decorator(self):
        @memoize
        def test_func(a):
            return a
        
        self.assertEqual(test_func('test'), 'test')
        
        test_func._memoize_cache[(('test',), ())] = 'from cache'
        
        self.assertEqual(test_func('test'), 'from cache')
        self.assertEqual(test_func('Test'), 'Test')


class CachedForModelTestCase(TestCase):
    def setUp(self):
        cache._cache = {}
    
    def test_cached_for_model_decorator(self):
        instance = Simple.objects.create(slug='test')
        
        self.assertEqual(instance.get_cached_data('some arg'), 'test')
        
        instance.slug = 'new'
        
        self.assertEqual(instance.get_cached_data('some arg'), 'test')
        self.assertEqual(instance.get_cached_data('another arg'), 'new')
        self.assertEqual(instance.get_cached_data('some arg'), 'test')
