'''
Routing module
'''
from sanic.response import text, json
from consumer.db_services import RedisManager, ZookeeperManager, CassandraManager
from consumer.db_services import PGManager
from consumer.models import Message
from consumer.config import Configs


async def get_messages_count(request):
    '''
    Function for rowcount selection
    IF there is POSTGRES in config data storage, then Postgres manager will be used for retreiving
    ELSE Cassandra manager will be used
    :param request:
    :return: rowcount
    '''
    if Configs['DATA_STORAGE'] == 'POSTGRES':
        response = json({'row_count': await PGManager.table_row_count(Message)})
    else:
        response = json({'row_count': await CassandraManager.select_count()})
    return response


async def get_last_offset(request):
    '''
        Function for offset selection
        IF there is REDIS in config offset storage, then Redis manager will be used for retreiving
        ELSE Zookeeper manager will be used
        :param request:
        :return: rowcount
        '''
    if Configs['OFFSET_STORAGE'] == 'REDIS':
        response = json({'kafka_offset': await RedisManager.get_value('kafka')})
    else:
        response = json({'kafka_offset': await ZookeeperManager.get()})
    return response


def add_routes(app):
    '''
    Add routes to Sanic application
    :param app: Sanic application
    :return: None
    '''
    app.add_route(get_messages_count, '/count', methods=['GET'])
    app.add_route(get_last_offset, '/offset', methods=['GET'])
