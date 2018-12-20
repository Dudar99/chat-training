from sanic import Sanic

consumer_app = Sanic(__name__)

from consumer.routes import add_routes

add_routes(consumer_app)
