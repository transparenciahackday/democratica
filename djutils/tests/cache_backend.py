from django.core.cache.backends.base import BaseCache


class CacheClass(BaseCache):
    """
    A simple cache backend for testing purposes
    """
    def __init__(self, *args, **kwargs):
        self._cache = {}

    def get(self, key, default=None):
        self.validate_key(key)
        return self._cache.get(key, default)

    def set(self, key, value, timeout=None):
        self.validate_key(key)
        self._cache[key] = value

    def delete(self, key, *args, **kwargs):
        self.validate_key(key)
        if key in self._cache:
            del(self._cache[key])
    
    def incr(self, key):
        self._cache.setdefault(key, 0)
        self._cache[key] += 1
    
    def clear(self):
        self._cache = {}
