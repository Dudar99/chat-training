"""
Module for app configuration
"""
import os

IS_IN_DOCKER = os.environ.get('DOCKER', False)

BASEDIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

CONSUMER_LOG_FILE_PATH = os.path.join(BASEDIR, "logs/consumer_logs.txt")

Configs = {
    'POSTGRES_USER': os.environ.get('POSTGRES_USER') or 'project',
    'POSTGRES_PASSWORD': os.environ.get('POSTGRES_PASSWORD') or 'project',
    'POSTGRES_DATABASE': os.environ.get('POSTGRES_DATABASE') or 'project',
    'POSTGRES_PORT': os.environ.get('POSTGRES_PORT') or 5432,
    'KAFKA_PORT': os.environ.get('KAFKA_PORT') or 9092,
    'ZOOKEEPER_PORT': os.environ.get('ZOOKEEPER_PORT') or 2181,
    'REDIS_PORT': os.environ.get('REDIS_PORT') or 6379,
    'OFFSET_STORAGE': os.environ.get('OFFSET_STORAGE') or 'ZOOKEEPER',
    'DATA_STORAGE': os.environ.get('DATA_STORAGE') or 'CASSANDRA',
    'REDIS_HOST': os.environ.get('REDIS_HOST') or 'redis',
    'CASSANDRA_HOST': os.environ.get('CASSANDRA_HOST') or 'localhost',
    'POSTGRES_ADDRESS': os.environ.get('POSTGRES_ADDRESS') or 'localhost',
    'KAFKA_ADDRESS': os.environ.get('KAFKA_SERVERS') or 'localhost',

}

if not IS_IN_DOCKER:
    Configs.update({
        'POSTGRES_ADDRESS': os.environ.get('POSTGRES_ADDRESS') or 'localhost',
        'KAFKA_ADDRESS': os.environ.get('KAFKA_SERVERS') or 'localhost',
        'ZOOKEEPER_HOST': os.environ.get('ZOOKEEPER_HOST') or 'localhost',
        'REDIS_HOST': os.environ.get('ZOOKEEPER_HOST') or 'localhost',
        'CASSANDRA_HOST': os.environ.get('CASSANDRA_HOST') or 'localhost',

    })
else:
    Configs.update({
        'POSTGRES_ADDRESS': os.environ.get('POSTGRES_ADDRESS') or 'postgres',
        'KAFKA_ADDRESS': os.environ.get('KAFKA_SERVERS') or 'kafka',
        'ZOOKEEPER_HOST': os.environ.get('ZOOKEEPER_HOST') or 'zookeeper',
        'REDIS_HOST': os.environ.get('REDIS_HOST') or 'redis',
        'CASSANDRA_HOST': os.environ.get('CASSANDRA_HOST') or 'cassandra',
    })
