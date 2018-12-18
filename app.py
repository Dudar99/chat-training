from sanic import Sanic
from sanic.response import json

APP = Sanic()



if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=5000)
