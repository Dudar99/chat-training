from sanic.response import text, json

from consumer.db_services import RedisManager, ZookeeperManager, CassandraManager
from consumer.db_services import PGManager
from consumer.models import Message
from consumer.config import Configs


async def get_messages_count(request):
    if Configs['DATA_STORAGE'] == 'POSTGRES':
        response = json({'row_count': await PGManager.table_row_count(Message)}), 200
    else:
        response = json({'row_count': await CassandraManager.select_count()}), 200
    return response


async def get_last_offset(request):
    if Configs['OFFSET_STORAGE'] == 'REDIS':
        response = json({'kafka_offset': await RedisManager.get_value('kafka')}), 200
    else:
        response = json({'kafka_offset': await ZookeeperManager.get()}), 200
    return response


def add_routes(app):
    app.add_route(get_messages_count, '/count', methods=['GET'])
    app.add_route(get_last_offset, '/offset', methods=['GET'])
