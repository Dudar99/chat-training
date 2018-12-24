from kafka import KafkaConsumer
import asyncio
from consumer.models import Message
from consumer.db_services.postgres_db import PostgresDatabaseManager
from consumer.db_services.redis_db import RedisManager


# To consume latest messages and auto-commit offsets
class Consumer:

    def __init__(self):
        self.consumer = KafkaConsumer('my-topic',
                                      group_id='my-group',
                                      bootstrap_servers=['localhost:9092'])
        self.counter = 0

    async def listen(self):
        for msg in self.consumer:
            self.counter = self.counter + 1
            print(f"topic:{msg.topic} partition: {msg.partition} offset:{msg.offset}"
                  f" key:{msg.key}  value:{msg.value} ")
            print('offset :', msg.offset)

            RedisManager.set_data('kafka_offset', f"{msg.offset}")
            message = Message(msg.topic, msg.value)
            PostgresDatabaseManager.session_commit(message)

            if self.counter >= 10:
                self.consumer.commit()
                self.counter = 0
                print("Was commited")  # TODO make logger

    async def commit_per_second(self, second):
        while True:
            await asyncio.sleep(second)
            self.counter = 0
            print(self.counter)
            self.consumer.commit()
            print("Was commited ")

    async def commit_per_10_item(self):
        while True:
            if self.counter > 10:
                self.consumer.commit()
                self.counter = 0
                print("messages was commited after 10th message appears")
            await asyncio.sleep(1)
