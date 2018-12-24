from sanic import Sanic

APP = Sanic(__name__)

from producer.routes import add_routes

add_routes(APP)
