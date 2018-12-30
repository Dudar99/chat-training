from producer.producer import Producer
from sanic.response import html, redirect
from kafka.errors import NoBrokersAvailable
import time
from producer.app import LOGGER


async def send_message(request):
    LOGGER.info(f"Try to establish connection with broker")
    while True:
        try:
            producer = Producer()
            break
        except NoBrokersAvailable:
            time.sleep(5)

    message_data = request.form.get('message')

    producer.send_messages('my-topic', message_data)
    return redirect('/')


def get_home_page(request):
    return html(''' <form action="/send_message" method="post">
                      Enter message: <input type="text" name="message"><br>
                      <input type="submit" value="Submit">
                    </form> ''')


def add_routes(app):
    app.add_route(get_home_page, '/', methods=['GET'])
    app.add_route(send_message, '/send_message', methods=['POST'])