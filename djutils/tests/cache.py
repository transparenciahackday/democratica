import time
import threading

from django.conf import settings
from django.core.cache import cache

from djutils.cache import key_from_args, cached_filter, CachedNode
from djutils.test import TestCase
from djutils.tests.cache_backend import CacheClass


class CacheUtilsTestCase(TestCase):
    def setUp(self):
        cache.clear()
    
    def test_cache_works(self):
        from django.core.cache import cache
        self.assertTrue(type(cache) is CacheClass)
    
    def test_key_from_args_collisions(self):
        self.assertNotEqual(key_from_args('test'), key_from_args('Test'))
        self.assertNotEqual(key_from_args('testtest'), key_from_args('test', 'test'))
        self.assertNotEqual(key_from_args('test\x01test'), key_from_args('test', 'test'))
        self.assertNotEqual(key_from_args('a', b='b', c='c'), key_from_args('a', 'c', b='b'))
    
    def test_key_from_args(self):
        self.assertEqual(key_from_args('test', 'one', 'two'), key_from_args('test', 'one', 'two'))
        self.assertEqual(key_from_args('a', b='b', c='c'), key_from_args('a', c='c', b='b'))
    
    def test_cached_filter(self):
        key_default = key_from_args('testing',)
        
        @cached_filter
        def test_filter(value, param=None):
            return (value, param)
        
        res = test_filter('testing')
        self.assertTrue(key_default in cache._cache)
        
        self.assertEqual(cache._cache[key_default], ('testing', None))
        
        cache._cache[key_default] = 'from cache'
        res = test_filter('testing')
        
        self.assertEqual(res, 'from cache')
        
        res = test_filter('testing', None)
        self.assertEqual(res, ('testing', None))
        
        res = test_filter('')
        self.assertEqual(res, ('', None))
    
    def test_cached_node(self):
        class TestSafeCachedNode(CachedNode):
            def get_cache_key(self, context):
                return key_from_args(**context)
            
            def get_content(self, context):
                return context
        
        test_node = TestSafeCachedNode()
        
        context = {'a': 'A'}
        key = test_node.get_cache_key(context)
        repopulating = test_node.repopulating_key(key)
        
        # check that object is cached under the expected key
        res = test_node.render({'a': 'A'})
        self.assertTrue(key in cache._cache)
        
        # check that the correct data is stored in cache
        cached_context, stale = cache._cache[key]
        self.assertEqual(cached_context, context)
        
        # manually alter the cached data to check if it is served
        cache._cache[key] = ({'b': 'B'}, stale)
        
        # ensure that the cached data is served
        res = test_node.render(context)
        self.assertEqual(res, {'b': 'B'})
        
        # forcing repopulation results in new data
        cache._cache[key] = ({'b': 'B'}, 0)
        res = test_node.render(context)
        self.assertEqual(res, context)
        
        # we will get old results if data is stale and another request is 
        # currently repopulating cache
        cache.set(repopulating, 1)
        cache._cache[key] = ({'c': 'C'}, 0)
        
        self.assertTrue(test_node.is_repopulating(key))
        
        res = test_node.render(context)
        self.assertEqual(res, {'c': 'C'})
        
        # simulate our data expiring while another (possibly the first?) request
        # initiates a call to get_content()
        cache.delete(key)
        
        # because the node is aggressive and doesn't use a spin lock, it will
        # force another call to get_content
        res = test_node.render(context)
        self.assertEqual(res, context)
        
        # the cache will be marked as no longer repopulating
        self.assertFalse(test_node.is_repopulating(key))
        
        # so make it think its repopulating again and remove the key
        cache.set(repopulating, 1)
        cache.delete(key)
        
        # check that when aggressive is off, an empty string is returned if
        # another thread is already repopulating and the data is gone
        test_node.aggressive = False
        
        res = test_node.render(context)
        self.assertEqual(res, '')
        
        # lastly, mark as aggressive and use a spin lock
        test_node.aggressive = True
        test_node.use_spin_lock = True
        test_node.backoff = (0.1, 2.0, 0.5) # starting w/ .1s, double timeout up to .5s
        
        # waste some time in a separate thread and repopulate the cache there
        def waste_time():
            time.sleep(.08)
            cache.delete(repopulating)
            cache._cache[key] = ({'D': 'd'}, 0)
        
        # start the thread
        time_waster = threading.Thread(target=waste_time)
        time_waster.start()
        
        # this is janky, but check that the spin lock spins for just one loop
        start = time.time()
        res = test_node.render(context)
        end = time.time()
        
        # self.assertTrue(.1 < end - start < .15)
        self.assertEqual(res, {'D': 'd'})
