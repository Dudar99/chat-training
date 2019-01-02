"""
Module for creating sanic app
"""
from sanic import Sanic
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from consumer.config import CONSUMER_LOG_FILE_PATH
import redis
from consumer.config import Configs
from logger_conf import make_logger
from cassandra.cluster import Cluster


APP = Sanic(__name__)
LOGGER = make_logger(CONSUMER_LOG_FILE_PATH, 'consumer_logger')

ENGINE = create_engine(
    f"postgresql://{Configs['POSTGRES_DATABASE']}:{Configs['POSTGRES_USER']}"
    f"@{Configs['POSTGRES_DATABASE']}:{Configs['ZOOKEEPER_PORT']}/{Configs['POSTGRES_DATABASE']}")

SESSION_PG = sessionmaker(bind=ENGINE)
REDIS = redis.Redis(host=Configs['REDIS_HOST'], port=Configs['REDIS_PORT'], db=0)
CS_KEY_SPACE = 'chat'


CLASTER = Cluster([Configs['CASSANDRA_HOST']])
SESSION = CLASTER.connect()
# SESSION.set_keyspace('chat_1')


from consumer.routes import add_routes
add_routes(APP)
