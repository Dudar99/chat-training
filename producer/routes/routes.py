from producer import producer_app
from producer.producer import Producer
from sanic.response import text, json, html, redirect


async def send_message(request):
    producer = Producer()
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
    app.add_route(send_message, '/send_message', methods=['GET', 'POST'])