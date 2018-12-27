from consumer.app import REDIS
from consumer.app import LOGGER
import aioredis
from asyncio import get_event_loop
from config import REDIS_SETTINGS


class RedisManager:
    connection: aioredis.Redis = None

    @classmethod
    async def __init(cls):
        cls.connection = await aioredis.create_redis(
            f'redis://{REDIS_SETTINGS["REDIS_URL"]}:{REDIS_SETTINGS["REDIS_PORT"]}', loop=get_event_loop())

    @classmethod
    def set_value(cls, key, value):

    @classmethod
    def get_value(cls, key):
        LOGGER.info(f"value: '{key}' was redaed from redis")
        return REDIS.get(key)

    @classmethod
    async def get(cls, key):
        result = await RedisManager.connection.get(key)
        return result

    @classmethod
    async def set(cls, key, value):
        await  RedisManager.connection.set(key=key, value=value)