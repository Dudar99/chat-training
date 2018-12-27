# from consumer.app import LOGGER
import aioredis
from asyncio import get_event_loop
from config import REDIS_SETTINGS
import asyncio


class RedisManager:
    connection: aioredis.Redis = None

    @classmethod
    async def _init(cls):
        try:
            cls.connection = await aioredis.create_redis('redis://redis:6379', loop=get_event_loop())
        except Exception as e :
            # LOGGER.info(f"Redis cannot connect || {e} ")
            print("L")
    @classmethod
    async def get_value(cls, key):
        result = await cls.connection.get(key)
        # LOGGER.info(f"Value: '{result}' was red from redis")
        return result

    @classmethod
    async def set_value(cls, key, value):
        value = await  cls.connection.set(key=key, value=value)
        # LOGGER.info(f"Value: '{value}' was written to redis")

    @classmethod
    async def close(cls):
        cls.connection.close()
        await cls.connection.wait_closed()

