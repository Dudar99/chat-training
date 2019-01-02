import asyncio
from aiokafka import AIOKafkaProducer
import json
from producer.app import LOGGER
import time

class Producer():
    def __init__(self):
        while True:
            try:
                self.producer = AIOKafkaProducer(
                    loop=asyncio.get_event_loop(), bootstrap_servers='kafka:9092',
                    value_serializer=lambda m: json.dumps(m).encode('utf-8'))
                break
            except Exception as err:
                time.sleep(2)
                LOGGER.error(err)

    async def send_one(self, message):

        await self.producer.start()
        try:
            # Produce message
            await self.producer.send_and_wait("my-topic", message)
        finally:
            # Wait for all pending messages to be delivered or expire.
            await self.producer.stop()
