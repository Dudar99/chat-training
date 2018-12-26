from consumer.app import REDIS
from consumer.app import LOGGER


class RedisManager:

    @classmethod
    def set_data(cls, key, value):
        LOGGER.info(f"value: '{value}' was inserted to redis")
        REDIS.set(key, value)

    @classmethod
    def get_last_record(cls, key):
        LOGGER.info(f"value: '{key}' was redaed from redis")
        return REDIS.get(key)
