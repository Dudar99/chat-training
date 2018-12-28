import uuid

from aiokafka import AIOKafkaConsumer
import asyncio
from consumer.db_services import PGManager
from consumer.db_services import (RedisManager,
                                  ZookeeperManager,
                                  CassandraManager)
from consumer.app import LOGGER


class Consumer:
    consumer: AIOKafkaConsumer = None
    counter: int = 0

    @classmethod
    async def __init(cls, second_commit, item_commit):
        cls.consumer = AIOKafkaConsumer('my-topic',
                                        group_id="chat_1",
                                        bootstrap_servers=["kafka:9092"],
                                        loop=asyncio.get_event_loop(),
                                        enable_auto_commit=False,
                                        consumer_timeout_ms=3000
                                        )
        while True:
            try:
                await cls.consumer.start()
                LOGGER.info("Connection with Kafka broker successfully established")
                cls._commit_task = asyncio.ensure_future(cls.commit_per_second(second_commit))
                cls._commit_task = asyncio.ensure_future(cls.commit_per_item(item_commit))
                break
            except Exception as e:
                LOGGER.error("Couldn't connect to Kafka broker because of %s, try again in 3 seconds", e)
                await asyncio.sleep(3)

        cls.counter = 0

    @classmethod
    async def _listen(cls):

        await cls.__init(second_commit=10, item_commit=3)
        async for msg in cls.consumer:
            cls.counter += 1
            LOGGER.info(f"topic:{msg.topic} partition: {msg.partition} offset:{msg.offset}"
                        f" key:{msg.key}  value:{msg.value} ")

            await cls.write_messages_to_db('mt-topic', msg=msg.value, offset=msg.offset)
            if cls.counter > 10:
                await cls.consumer.commit()
                cls.counter = 0
                LOGGER.info(f"Consumer received {cls.counter}th message, commit has been performed")

    @classmethod
    async def write_messages_to_db(cls, topic, msg, offset):
        await RedisManager.set_value('kafka', f"{offset}")
        LOGGER.info(f"offset {offset} was inserted to redis")
        await ZookeeperManager.set('kafka')
        LOGGER.info(f"offset {offset} was inserted to ZK")
        await PGManager.insert_into_table(msg=msg)
        LOGGER.info("Message stored to DB")
        await CassandraManager.insert(id=str(uuid.uuid4()), message=msg.decode('utf-8'))
        LOGGER.info("Message stored to DB_cs")


    @classmethod
    async def commit_per_second(cls, second):
        while True:
            await asyncio.sleep(second)
            cls.consumer.commit()
            cls.counter = 0
            LOGGER.info(f"commited per {second} second")

    @classmethod
    async def commit_per_item(cls, count):
        while True:
            if cls.counter >= count:
                cls.consumer.commit()
                cls.counter = 0
                LOGGER.info(f"messages was commited after {count} message appears")
            await asyncio.sleep(0.1)
