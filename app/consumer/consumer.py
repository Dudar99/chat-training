from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import asyncio
from consumer.models import Message
from consumer.db_services.postgres_db import PostgresDatabaseManager
from consumer.db_services.redis_db import RedisManager
import time

class Consumer:

    def __init__(self):
        self.consumer = KafkaConsumer('my-topic',
                                      group_id='my-group',
                                      bootstrap_servers=['kafka:9092'],
                                      )
        self.counter = 0

    async def fetch_messages(self):
        for msg in self.consumer:
            self.counter = self.counter + 1
            print(f"topic:{msg.topic} partition: {msg.partition} offset:{msg.offset}"
                  f" key:{msg.key}  value:{msg.value} ")
            print('offset :', msg.offset)
            await asyncio.sleep(0.1)
            await self.write_messages_to_db(topic=msg.topic, msg=msg.value, offset=msg.offset)

    @staticmethod
    async def write_messages_to_db(topic, msg, offset):
        RedisManager.set_data('kafka_offset', f"{offset}")
        message = Message(topic, msg)
        PostgresDatabaseManager.session_commit(message)

    async def commit_per_second(self, second):
        while True:
            await asyncio.sleep(second)
            self.consumer.commit()
            self.counter = 0
            print(f"Was commited per {second}")

    async def commit_per_item(self, count):
        while True:
            if self.counter >= count:
                self.consumer.commit()
                self.counter = 0
                print(f"messages was commited after {count} message appears")
            await asyncio.sleep(0.01)

    @classmethod
    async def listen_and_commit(self, loop, item, second):



        try:
            consumer = Consumer()
            print('Consumer started')
            task_commit_per_second = loop.create_task(consumer.commit_per_second(second))
            task_fetch_messages = loop.create_task(consumer.fetch_messages())
            task_commit_per_item = loop.create_task(consumer.commit_per_item(item))
            await asyncio.wait([task_commit_per_item, task_commit_per_second, task_fetch_messages])
        except Exception as e:
            print("some problems",e)
