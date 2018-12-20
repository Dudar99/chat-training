from kafka import KafkaConsumer
import asyncio


# To consume latest messages and auto-commit offsets
class Consumer:

    def __init__(self):
        self.consumer = KafkaConsumer('my-topic',
                                      group_id='my-group',
                                      bootstrap_servers=['localhost:9092'])
        self.counter = 0


    async def listen(self):  # TODO write to DB
        for message in self.consumer:
            self.counter = self.counter + 1
            print(f"topic:{message.topic} partition: {message.partition} offset:{message.offset}"
                  f" key:{message.key}  value:{message.value} ")
            print(f'counter{self.counter}')

    async def commit_per_10_second(self):
        while True:
            await asyncio.sleep(10)
            self.consumer.commit()
            self.counter = 0
            print("messages was commited after 10 sec.")

    async def commit_per_10_item(self):
        while True:
            if self.counter > 10:
                self.consumer.commit()
                self.counter = 0
                print("messages was commited after 10th message appears")
            await asyncio.sleep(1)
