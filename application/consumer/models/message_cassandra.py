'''
Module for Cassandra tables initialization
'''
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from datetime import datetime


class Message_cs(Model):
    '''
    Cassandra message model
    '''
    _table_name = "message"
    id = columns.UUID(primary_key=True)
    message = columns.Text(required=True)
    sent_date = columns.Date(required=True, default=datetime.utcnow())


models_cs = (Message_cs,)
