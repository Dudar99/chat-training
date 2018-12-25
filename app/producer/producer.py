from kafka import KafkaProducer
import json
from kafka.errors import KafkaError


class Producer():
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                      value_serializer=lambda m: json.dumps(m).encode('ascii'), retries=2)
        # # Asynchronous by default
        # for _ in range(10):
        #     future = self.producer.send('my-topic', {'fg': _})
        #     # Block for 'synchronous' sends
        #

    def send_messages(self, topic, *messages):
        for message in messages:
            future = self.producer.send(topic, {topic: message})
            try:
                future.get(timeout=10)
            except KafkaError:
                # Decide what to do if produce request failed...
                print(KafkaError.args)
                pass
        self.producer.flush()
