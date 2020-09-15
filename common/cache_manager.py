import asyncio
import hashlib
from functools import wraps

import aioredis
import ujson

from config import Config


def ensure_connection(coro):
    @wraps(coro)
    async def _ensure_connection(cls, *args, **kwargs):
        if cls.is_closed():
            async with cls.get_connection_lock():
                if cls.is_closed():
                    await cls.connect()
        return await coro(cls, *args, **kwargs)

    return _ensure_connection


class RedisCacheManager:
    KEY_PREFIX = "ghibli_cache"

    connection = None
    __connection_lock = None

    @classmethod
    def build_key(cls, **kwargs):
        serialized_kwargs = ujson.dumps(kwargs, sort_keys=True).encode("utf8")
        hashed_key = hashlib.sha256()
        hashed_key.update(serialized_kwargs)
        return f"{cls.KEY_PREFIX}_{hashed_key.hexdigest()}"

    @classmethod
    def get_connection_lock(cls):
        if cls.__connection_lock is None:
            loop = asyncio.get_event_loop()
            cls.__connection_lock = asyncio.Lock(loop=loop)
        return cls.__connection_lock

    @classmethod
    def is_closed(cls):
        return not cls.connection or cls.connection.closed

    @classmethod
    async def connect(cls):
        cls.connection = await aioredis.create_redis_pool((Config.REDIS_HOST, Config.REDIS_PORT), maxsize=3)

    @classmethod
    async def close(cls):
        if cls.connection and not cls.connection.closed:
            cls.connection.close()
            await cls.connection.wait_closed()

    @classmethod
    @ensure_connection
    async def retrieve_cached_data(cls, **kwargs):
        key = cls.build_key(**kwargs)
        cached_data = await cls.connection.get(key)
        return cached_data

    @classmethod
    @ensure_connection
    async def cache_data(cls, cache_ttl=None, **kwargs):
        data = kwargs.pop("data")
        key = cls.build_key(**kwargs)
        pipeline = cls.connection.pipeline()
        pipeline.set(key, data)
        if cache_ttl:
            pipeline.expire(key, cache_ttl)
        await pipeline.execute()
