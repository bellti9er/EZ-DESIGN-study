from typing import Any

from singleton import SingletonMeta


class CacheStorage(metaclass=SingletonMeta):
    def __init__(self):
        self.cache_storage = {}

    def get(self, key: str):
        return self.cache_storage.get(key)

    def set(self, key: str, value: Any):
        self.cache_storage[key] = value
