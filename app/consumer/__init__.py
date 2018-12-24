from sanic import Sanic
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE
import redis
from config import REDIS_SETTINGS
APP = Sanic(__name__)

ENGINE = create_engine(
    f"postgresql://{DATABASE['DB_NAME']}:{DATABASE['POSTGRES_USER']}"
    f"@{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['DB_NAME']}")

SESSION = sessionmaker(bind=ENGINE)
REDIS = redis.Redis(host=REDIS_SETTINGS['REDIS_URL'], port=REDIS_SETTINGS['REDIS_PORT'], db=0)

from consumer.routes import add_routes

add_routes(APP)
