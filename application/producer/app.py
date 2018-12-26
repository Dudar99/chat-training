from sanic import Sanic
from config import PRODUCER_LOG_FILE_PATH
from logger_conf import make_logger

APP = Sanic(__name__)

LOGGER = make_logger(PRODUCER_LOG_FILE_PATH)
print("Logger id producer",id(LOGGER))
from producer.routes import add_routes

add_routes(APP)
