from consumer.app import LOGGER, Configs
import aioredis
from asyncio import get_event_loop


class RedisManager:
    connection: aioredis.Redis = None

    @classmethod
    async def _init(cls):
        try:
            cls.connection = await aioredis.create_redis(f'redis://{Configs["REDIS_HOST"]}:{Configs["REDIS_PORT"]}',
                                                         loop=get_event_loop())
        except Exception as e:
            LOGGER.info(f"Redis cannot connect || {e} ")

    @classmethod
    async def get_value(cls, key):
        result = await cls.connection.get(key)
        LOGGER.info(f"Value: '{result}' was red from redis")
        return result

    @classmethod
    async def set_value(cls, key, value):
        value = await  cls.connection.set(key=key, value=value)
        LOGGER.info(f"Value: '{value}' was written to redis")

    @classmethod
    async def close(cls):
        cls.connection.close()
        await cls.connection.wait_closed()
