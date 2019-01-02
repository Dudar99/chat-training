'''
Module for zookeeper database manager
'''
import aiozk
import asyncio
from consumer.app import LOGGER, Configs


class ZookeeperManager:
    """
    Class that manage data in zookeeper
    """
    connection = None

    @classmethod
    async def connect(cls):
        '''
        Method which allow to establish connection with zookeeper
        :return: None
        '''
        ZookeeperManager.connection = aiozk.ZKClient(f"{Configs['ZOOKEEPER_HOST']}:{Configs['ZOOKEEPER_PORT']}",
                                                     loop=asyncio.get_event_loop())
        await ZookeeperManager.connection.start()
        try:
            await ZookeeperManager.connection.ensure_path('/offset')
            LOGGER.info("Connection with zookeeper established")
        except Exception as err:
            LOGGER.error(f'Problem with  path for ZK || {err}')
            await ZookeeperManager.connection.create('/offset', data=b'null', ephemeral=True)

    @classmethod
    async def close(cls):
        '''
        Method that close connection with zookeeper
        :return:
        '''
        await ZookeeperManager.connection.close()
        LOGGER.info("Connection with zookeeper closed")

    @classmethod
    async def set(cls, data):
        '''
        Insert data to zookeeper path
        :param data: string
        :return: None
        '''
        await ZookeeperManager.connection.set_data('/offset', str(data).encode('utf-8'))

    @classmethod
    async def get(cls):
        '''
        Retrieve last value from zookeeper path
        :return: None
        '''
        result = await ZookeeperManager.connection.get_data('offset')
        return result
