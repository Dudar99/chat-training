from sanic.response import text, json
from consumer.consumer import Consumer
from consumer.models import Message
from consumer import SESSION
from consumer.db_services.redis_db import RedisManager
import asyncio


async def get_messages():
    consumer = Consumer()
    ioloop = asyncio.get_event_loop()
    tasks = [
        ioloop.create_task(consumer.listen()),
        ioloop.create_task(consumer.commit_per_second(2))
    ]
    ioloop.run_until_complete(asyncio.wait(tasks))

    ioloop.close()

    return text("start listening")


async def get_messages_count(request):
    session = SESSION()
    return json({'count': session.query(Message.id).count()})


async def get_last_offset(request):
    return json({'kafka_offset': RedisManager.get_last_record('kafka_offset')})


def add_routes(app):
    # app.add_route(get_messages, '/listen', methods=['GET'])
    app.add_route(get_messages_count, '/count', methods=['GET'])
    app.add_route(get_last_offset, '/offset', methods=['GET'])
