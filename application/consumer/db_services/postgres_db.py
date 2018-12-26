from consumer.models import Message
from consumer.app import SESSION_PG
from consumer.app import LOGGER

class CreateTable:
    def __init__(self):
        Message.create_db()
        LOGGER.info("Postgres db was created")


class PostgresDatabaseManager:
    @classmethod
    def session_commit(cls, data):
        session = SESSION_PG()
        session.add(data)
        LOGGER.info(f"Values where inserted into PG database")
        session.commit()
        session.close()
