from kafka import KafkaProducer
import json
from kafka.errors import KafkaError


class Producer():
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                                      value_serializer=lambda m: json.dumps(m).encode('ascii'), retries=1)

    def send_messages(self, topic, *messages):
        for message in messages:
            future = self.producer.send(topic, {topic: message})
            try:
                future.get(timeout=1)
            except KafkaError:
                # Decide what to do if produce request failed...
                print(KafkaError.args)
                pass
        self.producer.flush()
