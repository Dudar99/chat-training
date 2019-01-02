"""
Module for kafka producer description
"""

import asyncio
from aiokafka import AIOKafkaProducer
import json
from producer.app import LOGGER
from producer.config import Configs
import time


class Producer():
    """
    Producer class description
    """
    def __init__(self):
        """
        try to establish connection with Kafka
        """
        while True:
            try:
                self.producer = AIOKafkaProducer(
                    loop=asyncio.get_event_loop(),
                    bootstrap_servers=f"{Configs['KAFKA_ADDRESS']}:{Configs['KAFKA_PORT']}",
                    value_serializer=lambda m: json.dumps(m).encode('utf-8'))
                break
            except Exception as err:
                time.sleep(2)
                LOGGER.error(err)

    async def send_one(self, message):
        """
        Method which allow t osend message
        :param message: string
        :return: None
        """
        await self.producer.start()
        try:
            # Produce message
            await self.producer.send_and_wait("my-topic", message)
        finally:
            # Wait for all pending messages to be delivered or expire.
            await self.producer.stop()
