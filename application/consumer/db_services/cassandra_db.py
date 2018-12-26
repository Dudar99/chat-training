from consumer.app import SESSION_CS
from consumer.models import  Message_cs

class CassandraManager:
    """
    Class that manages data in cassandra2
    """

    @classmethod
    def create(cls):
        Message_cs.create_db()

    @classmethod
    def insert(cls, message):
        msg = Message_cs.create( message=message)

    @classmethod
    def get_count(cls):
        return Message_cs.objects.count()


CassandraManager.get_count()