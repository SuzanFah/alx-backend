#!/usr/bin/env python3
"""MRU caching module.
"""
from base_caching import BaseCaching
from collections import OrderedDict


class MRUCache(BaseCaching):
    """MRU cache class.
    """
    def __init__(self):
        """Initialize the cache.
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Store an item in the cache.
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS and key not in self.cache_data:
                mru_key, _ = self.cache_data.popitem(last=True)
                print(f"DISCARD: {mru_key}")
            
            if key in self.cache_data:
                self.cache_data.pop(key)
            self.cache_data[key] = item

    def get(self, key):
        """Retrieve an item from the cache.
        """
        if key is not None and key in self.cache_data:
            value = self.cache_data.pop(key)
            self.cache_data[key] = value
            return value
        return None
