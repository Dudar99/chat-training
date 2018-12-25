from producer import APP as producer
from consumer import APP as consumer_app
import time
from sys import argv
import asyncio
from consumer.consumer import Consumer

if __name__ == '__main__':
    if 'producer' in argv:
        producer.run(host='127.34.23.31', port=8001)
    if 'consumer' in argv:
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(Consumer.listen_and_commit(loop=loop, item=10, second=10))

        except Exception as e:
            print("some issue2")
        finally:
            loop.close()
