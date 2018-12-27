import redis
import os
try:
    from local_config import *
except EnvironmentError:
    pass
IS_IN_DOCKER = os.environ.get('DOCKER', False)


BASEDIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
DATABASE = {
    'POSTGRES_USER': LOCAL_POSTGRES_DB_SETTINGS['POSTGRES_USER'],
    'POSTGRES_PASSWORD': LOCAL_POSTGRES_DB_SETTINGS['POSTGRES_PASSWORD'],
    'HOST': LOCAL_POSTGRES_DB_SETTINGS['HOST'],
    'PORT': LOCAL_POSTGRES_DB_SETTINGS['PORT'],
    'DB_NAME': LOCAL_POSTGRES_DB_SETTINGS['DB_NAME']
}
REDIS_SETTINGS = {
    "REDIS_URL": LOCAL_REDIS_DB_SETTINGS['REDIS_URI'],
    "REDIS_PORT": LOCAL_REDIS_DB_SETTINGS['REDIS_PORT']
}
CONSUMER_LOG_FILE_PATH = "logs/consumer_log.txt"

PRODUCER_LOG_FILE_PATH = 'logs/producer_log.txt'
