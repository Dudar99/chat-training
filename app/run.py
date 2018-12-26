from producer import APP as producer_app
from consumer import APP as consumer_app
import time
from sys import argv
import asyncio
from consumer.consumer import Consumer
from producer.producer import Producer

if __name__ == '__main__':
    if 'producer' in argv:
        producer_app.run(host='0.0.0.0', port=5000)
    if 'consumer' in argv:
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(Consumer.listen_and_commit(loop=loop, item=10, second=10))

        except Exception as e:
            print("some issue2")
        finally:
            loop.close()
