from sanic.response import text, json

from consumer.db_services.redis_db import RedisManager
from consumer.app import APP
from consumer.app import LOGGER
from consumer.db_services import PGManager
from consumer.models import Message


async def get_messages_count(request):
    return json({'row_count': await PGManager.table_row_count(Message)})


async def get_last_offset(request):
    return json({'kafka_offset': await RedisManager.get_value('kafka')})


def add_routes(app):
    app.add_route(get_messages_count, '/count', methods=['GET'])
    app.add_route(get_last_offset, '/offset', methods=['GET'])
