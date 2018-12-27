from sanic.response import text, json

from consumer.db_services.redis_db import RedisManager
from consumer.app import APP
from consumer.app import LOGGER
from consumer.db_services import PGManager



# async def get_messages_count(request):
#     session = SESSION_PG()
#     return json({'count': session.query(Message.id).count()})


async def get_last_offset(request):
    return json({'kafka_offset': RedisManager.get_last_record('kafka_offset')})


def add_routes(app):
    # application.add_route(get_messages, '/listen', methods=['GET'])
    # app.add_route(get_messages_count, '/count', methods=['GET'])
    app.add_route(get_last_offset, '/offset', methods=['GET'])


@APP.listener('before_server_start')
async def setup(app, loop):
    try:
        await PGManager.init_tables()
    except Exception as e:
        LOGGER.info(e)
    LOGGER.info("Databases were created")
    # CassandraDatabaseManager.create_keyspace()
    # CassandraDatabaseManager.create()
    # CassandraDatabaseManager2.create()
    # ZK.start()


@APP.listener('after_server_start')
async def notify_server_started(app, loop):
    from consumer.consumer import Consumer
    LOGGER.info(f'Server successfully started!')
    await Consumer._listen()