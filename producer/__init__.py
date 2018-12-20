from sanic import Sanic

producer_app = Sanic(__name__)

from producer.routes import add_routes
add_routes(producer_app)

