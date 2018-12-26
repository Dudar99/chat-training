from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import asyncio
from consumer.models import Message
from consumer.db_services.postgres_db import PostgresDatabaseManager
from consumer.db_services.redis_db import RedisManager
from consumer.app import LOGGER
import time


class Consumer:

    def __init__(self):
        while True:
            try:

                self.consumer = KafkaConsumer('my-topic',
                                              group_id='my-group',
                                              bootstrap_servers=['kafka:9092'])
                break
            except NoBrokersAvailable as e:
                LOGGER.info(e)
                time.sleep(4)
        self.counter = 0

    async def fetch_messages(self):
        for msg in self.consumer:
            self.counter = self.counter + 1
            LOGGER.info(f"topic:{msg.topic} partition: {msg.partition} offset:{msg.offset}"
                        f" key:{msg.key}  value:{msg.value} ")

            await asyncio.sleep(0.01)
            #await self.write_messages_to_db(topic=msg.topic, msg=msg.value, offset=msg.offset) # TODO asyncronous writing to DB

    @staticmethod
    async def write_messages_to_db(topic, msg, offset):
        RedisManager.set_data('kafka_offset', f"{offset}")
        message = Message(topic, msg)
        PostgresDatabaseManager.session_commit(message)
        LOGGER.info("Message stored to DB")

    async def commit_per_second(self, second):
        while True:
            await asyncio.sleep(second)
            self.consumer.commit()
            self.counter = 0
            LOGGER.info(f"commited per {second} second")

    async def commit_per_item(self, count):
        while True:
            if self.counter >= count:
                self.consumer.commit()
                self.counter = 0
                LOGGER.info(f"messages was commited after {count} message appears")
            await asyncio.sleep(0.1)

    @classmethod
    async def listen_and_commit(self, loop, item, second):
        consumer = Consumer()
        LOGGER.info("Consumer was created")
        task_commit_per_second = loop.create_task(consumer.commit_per_second(second))
        LOGGER.info("task fetch messagesc")
        task_fetch_messages = loop.create_task(consumer.fetch_messages())
        task_commit_per_item = loop.create_task(consumer.commit_per_item(item))
        await asyncio.wait([task_fetch_messages, task_commit_per_item, task_commit_per_second])
