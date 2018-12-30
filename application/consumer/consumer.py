import uuid

from aiokafka import AIOKafkaConsumer
import asyncio
from consumer.app import LOGGER
from consumer.config import Configs


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
        if Configs['DATA_STORAGE'] == 'POSTGRES':
            from consumer.db_services import PGManager
            await PGManager.insert_into_table(msg=msg)
        else:
            from consumer.db_services import CassandraManager
            await CassandraManager.insert(id=str(uuid.uuid4()), message=msg.decode('utf-8'))
        LOGGER.info("Message stored to DB")
        if Configs['OFFSET_STORAGE'] == 'REDIS':
            from consumer.db_services import RedisManager
            await RedisManager.set_value('kafka', f"{offset}")
        else:
            from consumer.db_services import ZookeeperManager
            await ZookeeperManager.set(offset)
        LOGGER.info(f"offset {offset} was saved")

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
