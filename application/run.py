"""
Module for running producer and consumer applications
"""
from sys import argv
from producer.app import APP as producer_app
from consumer.app import APP as consumer_app


if __name__ == '__main__':
    if 'producer' in argv:
        producer_app.run(host='0.0.0.0', port=5000)
    if 'consumer' in argv:
        consumer_app.run(host='0.0.0.0', port=5001)
