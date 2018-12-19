from . import producer_app

from sanic.response import text, json


@producer_app.route('/send_message', methods=['GET', 'POST'])
async def send_message(request):
    producer = Producer().produce
    producer.send('my-topic', {"message": request.json})
    return text({"message": f"successfully send {request.url}"})
