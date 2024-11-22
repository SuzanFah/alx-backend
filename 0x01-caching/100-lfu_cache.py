#!/usr/bin/env python3
"""LFU caching module.
"""
from base_caching import BaseCaching
from collections import defaultdict


class LFUCache(BaseCaching):
    """LFU cache class.
    """
    def __init__(self):
        """Initialize the cache.
        """
        super().__init__()
        self.frequency = defaultdict(int)
        self.usage_order = []

    def put(self, key, item):
        """Store an item in the cache.
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS and key not in self.cache_data:
                min_freq = min(self.frequency.values())
                lfu_keys = [k for k, v in self.frequency.items() if v == min_freq]
                
                if len(lfu_keys) == 1:
                    lfu_key = lfu_keys[0]
                else:
                    # Use LRU as tiebreaker
                    for k in self.usage_order:
                        if k in lfu_keys:
                            lfu_key = k
                            break
                
                del self.cache_data[lfu_key]
                del self.frequency[lfu_key]
                self.usage_order.remove(lfu_key)
                print(f"DISCARD: {lfu_key}")
            
            self.cache_data[key] = item
            self.frequency[key] += 1
            if key in self.usage_order:
                self.usage_order.remove(key)
            self.usage_order.append(key)

    def get(self, key):
        """Retrieve an item from the cache.
        """
        if key is not None and key in self.cache_data:
            self.frequency[key] += 1
            self.usage_order.remove(key)
            self.usage_order.append(key)
            return self.cache_data[key]
        return None
