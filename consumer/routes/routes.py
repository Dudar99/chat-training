from sanic.response import text, json, html
from consumer.consumer import Consumer
import asyncio


async def get_messages(request):
    consumer = Consumer()
    #
    # loop = asyncio.get_event_loop()
    # try:
    #     # await asyncio.ensure_future(consumer.commit_per_10_second())
    #     # await asyncio.ensure_future(consumer.commit_per_10_item())
    #     loop.run_forever()
    # except Exception:
    #     print("Closing Loop")
    #     loop.close()
    # finally:
    #     print("Closing Loop")
    #     loop.close()
    await consumer.listen()
    
    return text("start listening")


def add_routes(app):
    app.add_route(get_messages, '/', methods=['GET'])
