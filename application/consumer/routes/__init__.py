'''
Module for router __init__
'''
from .routes import add_routes
from consumer.app import APP

from consumer.db_services import (PGManager,
                                  RedisManager,
                                  CassandraManager,
                                  ZookeeperManager)
from consumer.app import LOGGER, Configs


@APP.listener('before_server_start')
async def setup(app, loop):
    '''

    :param app: application
    :param loop: loop of events
    :return:
    '''
    if Configs['DATA_STORAGE'] == 'POSTGRES':
        try:
            await PGManager.init_tables()
            LOGGER.info("PG database was created")
        except Exception as e:
            LOGGER.info(e)
    else:
        CassandraManager.create_keyspace()
        CassandraManager.create()
        LOGGER.info("Cassandra database was created")
    if Configs['OFFSET_STORAGE'] == 'REDIS':
        await RedisManager._init()
        LOGGER.info("Redis was connected")
    else:
        await ZookeeperManager.connect()
        LOGGER.info("Zookeeper was connected")


@APP.listener('after_server_start')
async def notify_server_started(app, loop):
    from consumer.consumer import Consumer
    LOGGER.info(f'Server successfully started!')
    await Consumer._listen()
