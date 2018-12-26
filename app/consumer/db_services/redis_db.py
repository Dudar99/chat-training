from consumer import REDIS


class RedisManager:

    @classmethod
    def set_data(cls, key, value):
        REDIS.set(key, value)

    @classmethod
    def get_last_record(cls, key):
        return REDIS.get(key)

