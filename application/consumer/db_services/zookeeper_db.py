import aiozk
import asyncio


class ZookeeperManager:
    """
    Class that manage data in zookeeper
    """
    connection = None

    @classmethod
    async def connect(cls):
        ZookeeperManager.connection = aiozk.ZKClient('zookeeper:2181', loop=asyncio.get_event_loop())
        await ZookeeperManager.connection.start()
        try:
            await ZookeeperManager.connection.ensure_path('/offset')
        except Exception as e:
            print('Problem with  path for ZK')
            await ZookeeperManager.connection.create('/offset', data=b'null', ephemeral=True)

    @classmethod
    async def close(cls):
        await ZookeeperManager.connection.close()

    @classmethod
    async def set(cls, data):
        await ZookeeperManager.connection.set_data('/offset', str(data).encode('utf-8'))

    @classmethod
    async def get(cls):
        result = await ZookeeperManager.connection.get_data('offset')
        return result
