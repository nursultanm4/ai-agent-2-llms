import cachetools
from typing import Optional, Any
from config import settings
from logger import logger


class CacheService:
    """Service for handling in-memory caching with TTL"""
    
    def __init__(self):
        self.cache = cachetools.TTLCache(
            maxsize=settings.CACHE_MAX_SIZE,
            ttl=settings.CACHE_TTL_SECONDS
        )
        logger.info(f"Cache initialized with TTL: {settings.CACHE_TTL_SECONDS}s, Max size: {settings.CACHE_MAX_SIZE}")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        value = self.cache.get(key)
        if value is not None:
            logger.debug(f"Cache hit for key: {key[:50]}...")
        else:
            logger.debug(f"Cache miss for key: {key[:50]}...")
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache"""
        self.cache[key] = value
        logger.debug(f"Cache set for key: {key[:50]}...")
    
    def delete(self, key: str) -> None:
        """Delete value from cache"""
        if key in self.cache:
            del self.cache[key]
            logger.debug(f"Cache deleted for key: {key[:50]}...")
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        return {
            "size": len(self.cache),
            "max_size": settings.CACHE_MAX_SIZE,
            "ttl": settings.CACHE_TTL_SECONDS
        }