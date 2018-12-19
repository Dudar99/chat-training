
from kafka import KafkaProducer
import json as jsn
from sanic.response import text, json


class Producer():
    def __init__(self):
        self.produce = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                     value_serializer=lambda m: jsn.dumps(m).encode('ascii'), retries=5)
        # # Asynchronous by default
        # for _ in range(10):
        #     future = producer.send('my-topic', {'fg': _})
        #     # Block for 'synchronous' sends
        #     try:
        #         record_metadata = future.get(timeout=10)
        #     except KafkaError:
        #         # Decide what to do if produce request failed...
        #         print(KafkaError.args)
        #         pass



