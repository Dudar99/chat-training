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
        ZookeeperManager.connection = aiozk.ZKClient(f"{Configs['ZOOKEEPER_HOST']}:{Configs['ZOOKEEPER_PORT']}",
                                                     loop=asyncio.get_event_loop())
        await ZookeeperManager.connection.start()
        try:
            await ZookeeperManager.connection.ensure_path('/offset')
            LOGGER.info("Connection with zookeeper established")
        except Exception as e:
            LOGGER.error('Problem with  path for ZK')
            await ZookeeperManager.connection.create('/offset', data=b'null', ephemeral=True)

    @classmethod
    async def close(cls):
        await ZookeeperManager.connection.close()
        LOGGER.info("Connection with zookeeper closed")

    @classmethod
    async def set(cls, data):
        await ZookeeperManager.connection.set_data('/offset', str(data).encode('utf-8'))

    @classmethod
    async def get(cls):
        result = await ZookeeperManager.connection.get_data('offset')
        return result
