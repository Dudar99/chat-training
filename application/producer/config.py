import os

try:
    from local_config import *
except EnvironmentError:
    pass
IS_IN_DOCKER = os.environ.get('DOCKER', False)
print("Producer < - > docker" , IS_IN_DOCKER)
BASEDIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


PRODUCER_LOG_FILE_PATH = os.path.join(BASEDIR, 'logs/producer_log.txt')
