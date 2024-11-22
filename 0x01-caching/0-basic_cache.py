#!/usr/bin/env python3
"""Basic caching module.
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """Basic cache class.
    """
    def put(self, key, item):
        """Stores an item in the cache.
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """Retrieves an item from the cache.
        """
        return self.cache_data.get(key) if key is not None else None
