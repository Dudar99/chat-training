
from kafka import KafkaProducer
import json
from kafka.errors import KafkaError
from producer.app import LOGGER

class Producer():
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                                      value_serializer=lambda m: json.dumps(m).encode('ascii'), retries=1)

    def send_messages(self, topic, *messages):
        for message in messages:
            future = self.producer.send(topic, {topic: message})
            LOGGER.info(f"Message {message} was sent")
            try:
                future.get(timeout=1)
            except KafkaError as err:
                LOGGER.error(f"{err}")
                pass
            self.producer.flush()
