from producer import APP as producer
from consumer import APP as consumer_app
import time
from sys import argv

if __name__ == '__main__':
    if 'producer' in argv:
        producer.run()
    if 'consumer' in argv:

        from consumer.consumer import Consumer
        import asyncio
        print('Consumer started')
        consumer = Consumer()
        loop = asyncio.get_event_loop()
        # loop.run_until_complete(asyncio.gather(
        #     consumer_app.run(port=8001),
        #     consumer.listen(),
        #     consumer.commit_per_second(1)
        # ))
        loop.create_task(consumer.listen())
        loop.create_task(consumer.commit_per_second(2))

        loop.run_forever()
        loop.close()


    # except Exception:
    #     print('issue')
    #     time.sleep(2)
# consumer.run(port=8001 )
