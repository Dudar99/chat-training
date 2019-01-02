import os

IS_IN_DOCKER = os.environ.get('DOCKER', False)

BASEDIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

PRODUCER_LOG_FILE_PATH = os.path.join(BASEDIR, 'logs/producer_log.txt')

Configs = {
    'KAFKA_PORT': os.environ.get('KAFKA_PORT') or 9092,
    'KAFKA_ADDRESS': os.environ.get('KAFKA_SERVERS') or 'localhost',
}
