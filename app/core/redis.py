# app/core/redis.py
import redis
import json
from typing import Optional, Any
from datetime import datetime

redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

def get_cache(key: str) -> Optional[dict]:
    """Get data from cache"""
    data = redis_client.get(key)
    return json.loads(data) if data else None

# --- NEW HELPER FUNCTION ---
def _json_serializer(obj: Any) -> Any:
    """Helper function to convert non-serializable objects."""
    if isinstance(obj, datetime):
        # Convert datetime to ISO format string
        return obj.isoformat()
    # Raise TypeError for any other non-serializable type
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def set_cache(key: str, value: dict | list, ttl: int = 300):
    """Set data in cache with TTL (default 5 minutes). Handles datetime objects."""
    # Use the custom 'default' handler in json.dumps
    serialized_value = json.dumps(value, default=_json_serializer)
    redis_client.setex(key, ttl, serialized_value)

def delete_cache(key: str):
    """Remove a specific key from cache"""
    redis_client.delete(key)

def delete_cache_pattern(pattern: str):
    """
    Remove all keys from cache matching a pattern.
    USE WITH CAUTION. This can be slow on large databases.
    """
    keys = []
    cursor = '0'
    while cursor != 0:
        cursor, found_keys = redis_client.scan(cursor=cursor, match=pattern, count=100)
        keys.extend(found_keys)
    
    if keys:
        redis_client.delete(*keys)
    return len(keys)