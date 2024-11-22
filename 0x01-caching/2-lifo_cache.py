#!/usr/bin/env python3
"""LIFO caching module.
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """LIFO cache class.
    """
    def __init__(self):
        """Initialize the cache.
        """
        super().__init__()
        self.stack = []

    def put(self, key, item):
        """Store an item in the cache.
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS and key not in self.cache_data:
                discarded_key = self.stack.pop()
                del self.cache_data[discarded_key]
                print(f"DISCARD: {discarded_key}")
            
            self.cache_data[key] = item
            if key in self.stack:
                self.stack.remove(key)
            self.stack.append(key)

    def get(self, key):
        """Retrieve an item from the cache.
        """
        return self.cache_data.get(key) if key is not None else None
