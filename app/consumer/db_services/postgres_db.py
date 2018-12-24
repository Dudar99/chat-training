from consumer.models import Message
from consumer import SESSION


class CreateTable:
    def __init__(self):
        Message.create_db()


class PostgresDatabaseManager:
    @classmethod
    def session_commit(cls, data):
        session = SESSION()
        session.add(data)
        session.commit()
        session.close()
