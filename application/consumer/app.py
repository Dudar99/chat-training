from sanic import Sanic
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE, CONSUMER_LOG_FILE_PATH
import redis
from config import REDIS_SETTINGS
from logger_conf import make_logger
from consumer.db_services import (PGManager,
                                  RedisManager,
                                  CassandraManager,
                                  ZookeeperManager)

APP = Sanic(__name__)
LOGGER = make_logger(CONSUMER_LOG_FILE_PATH,'consumer_logger')

ENGINE = create_engine(
    f"postgresql://{DATABASE['DB_NAME']}:{DATABASE['POSTGRES_USER']}"
    f"@{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['DB_NAME']}")

SESSION_PG = sessionmaker(bind=ENGINE)
REDIS = redis.Redis(host=REDIS_SETTINGS['REDIS_URL'], port=REDIS_SETTINGS['REDIS_PORT'], db=0)
CS_KEY_SPACE = 'chat'


#
#
# CLUSTER = Cluster(["cassandra"])
#
# KEY_SPACE = 'chat'
#
#
# CASSANDRA_SESSION = CLUSTER.connect()

@APP.listener('before_server_start')
async def setup(app, loop):
    try:
        await PGManager.init_tables()
        LOGGER.info("PG database was created")
    except Exception as e:
        LOGGER.info(e)
    await RedisManager._init()
    LOGGER.info("Redis was connected")
    await ZookeeperManager.connect()

    CassandraManager.create_keyspace()
    CassandraManager.create()


@APP.listener('after_server_start')
async def notify_server_started(app, loop):
    from consumer.consumer import Consumer
    LOGGER.info(f'Server successfully started!')
    await Consumer._listen()


from consumer.routes import add_routes

add_routes(APP)
