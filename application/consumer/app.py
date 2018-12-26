from cassandra.policies import DCAwareRoundRobinPolicy
from sanic import Sanic
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE, CONSUMER_LOG_FILE_PATH
import redis
from config import REDIS_SETTINGS
from logger_conf import make_logger
from cassandra.cluster import Cluster
import time

APP = Sanic(__name__)
LOGGER = make_logger(CONSUMER_LOG_FILE_PATH)
print("Logger id consumer", id(LOGGER))
ENGINE = create_engine(
    f"postgresql://{DATABASE['DB_NAME']}:{DATABASE['POSTGRES_USER']}"
    f"@{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['DB_NAME']}")

SESSION_PG = sessionmaker(bind=ENGINE)
REDIS = redis.Redis(host=REDIS_SETTINGS['REDIS_URL'], port=REDIS_SETTINGS['REDIS_PORT'], db=0)
CS_KEY_SPACE = 'chat'

CLUSTER = Cluster(["cassandra"])

KEY_SPACE = 'chat'


CASSANDRA_SESSION = CLUSTER.connect()

from consumer.routes import add_routes

add_routes(APP)
