from app import APP
from sanic.response import json

@APP.route
async def producer(request):
    return json({"hello": "world"})