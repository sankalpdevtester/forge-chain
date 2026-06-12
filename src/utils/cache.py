from datetime import datetime, timedelta
from typing import Any, Dict

class Cache:
    def __init__(self, ttl: int = 60):  # 1 minute default TTL
        self.cache: Dict[str, Any] = {}
        self.ttl = ttl

    def get(self, key: str) -> Any:
        if key in self.cache:
            value, expires_at = self.cache[key]
            if datetime.now() < expires_at:
                return value
            else:
                del self.cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        expires_at = datetime.now() + timedelta(seconds=self.ttl)
        self.cache[key] = (value, expires_at)

    def delete(self, key: str) -> None:
        if key in self.cache:
            del self.cache[key]

    def clear(self) -> None:
        self.cache.clear()

cache = Cache()

def cached(ttl: int = 60):
    def decorator(func):
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            cached_value = cache.get(key)
            if cached_value is not None:
                return cached_value
            value = func(*args, **kwargs)
            cache.set(key, value, ttl)
            return value
        return wrapper
    return decorator

# Example usage:
# @cached(ttl=30)  # 30 seconds TTL
# def get_blockchain_info():
#     # simulate an expensive operation
#     import time
#     time.sleep(2)
#     return {"blockchain_info": "example"}

# print(get_blockchain_info())  # first call takes 2 seconds
# print(get_blockchain_info())  # subsequent calls return cached value