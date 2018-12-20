from producer import producer_app
from consumer import consumer_app
from sys import argv


if __name__ == "__main__":
    if 'producer' in argv:
        producer_app.run(port=8001)
    if 'consumer' in argv:
        consumer_app.run(port=8003)

