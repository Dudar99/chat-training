from sanic.response import text, json

from consumer.db_services import RedisManager, ZookeeperManager, CassandraManager
from consumer.db_services import PGManager
from consumer.models import Message


async def get_messages_count(request):
    return json({'row_count': await PGManager.table_row_count(Message)})


async def get_last_offset(request):
    return json({'kafka_offset': await RedisManager.get_value('kafka')})


async def get_last_offset_zk(request):
    return json({'kafka_offset': await ZookeeperManager.get()})


async def get_messages_count_cs(request):
    return json({"cassandra_row_count": await CassandraManager.select_count()})


def add_routes(app):
    app.add_route(get_last_offset_zk, '/offset_zk', methods=['GET'])
    app.add_route(get_messages_count_cs, '/count_cs', methods=['GET'])
    app.add_route(get_messages_count, '/count', methods=['GET'])
    app.add_route(get_last_offset, '/offset', methods=['GET'])
