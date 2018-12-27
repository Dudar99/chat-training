import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model
from datetime import datetime


class Message(Model):
    """
    Cassandra model message
    """
    __table_name__ = 'message'
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    date = columns.DateTime(default=datetime.utcnow())
    message = columns.Text(required=True)

    @classmethod
    def create_db(cls):
        sync_table(Message)
