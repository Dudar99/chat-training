from sanic import Sanic
from config import PRODUCER_LOG_FILE_PATH
from logger_conf import make_logger
import asyncio

APP = Sanic(__name__)
LOOP = asyncio.get_event_loop()

LOGGER = make_logger(PRODUCER_LOG_FILE_PATH, 'producer_logger')

from producer.routes import add_routes

add_routes(APP)

LOGGER.info("OK Google")