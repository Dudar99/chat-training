from sanic import Sanic


producer_app = Sanic()



if __name__ == '__main__':
    producer_app.run(port=8001)
