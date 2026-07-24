from datetime import datetime, timedelta
from typing import Any, Dict

class Cache:
    def __init__(self, ttl: int = 60):  # 1 minute default TTL
        self.cache: Dict[str, Any] = {}
        self.ttl = ttl

    def get(self, key: str) -> Any:
        if key in self.cache:
            value, expiry = self.cache[key]
            if datetime.now() < expiry:
                return value
            else:
                del self.cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        expiry = datetime.now() + timedelta(seconds=self.ttl)
        self.cache[key] = (value, expiry)

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
            value = cache.get(key)
            if value is not None:
                return value
            else:
                value = func(*args, **kwargs)
                cache.set(key, value)
                return value
        return wrapper
    return decorator

# Example usage:
@cached(ttl=30)  # 30 seconds TTL
def get_blockchain_info() -> Dict:
    # Simulate an expensive operation
    import time
    time.sleep(2)
    return {"blocks": 100, "transactions": 500}

# Test the cache
print(get_blockchain_info())  # Takes 2 seconds
print(get_blockchain_info())  # Returns immediately from cache