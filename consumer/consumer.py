from kafka import KafkaConsumer
from sanic import Sanic
import json

consumer_app = Sanic()


@consumer_app.route('/home')
async def producer(request):
    return json({"gift": "lol"})


class Consumer():
    def __init__(self):
        consumer = KafkaConsumer('my-topic',
                                 group_id='my-group',
                                 bootstrap_servers=['127.0.0.1:9092'],
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=True,
                                 auto_commit_interval_ms=500,
                                 consumer_timeout_ms=5000)

        for message in consumer:
            print("Consumed Msg -> '%s' on Topic -> '%s' with Offset -> %d" %
                  (message.value.decode('utf-8'), message.topic, message.offset))
        consumer.close()
