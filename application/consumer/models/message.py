from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from datetime import datetime

Base = declarative_base()

metadata = sa.MetaData()

Message = sa.Table('Message', metadata,
                   sa.Column('id', sa.Integer, autoincrement=True, primary_key=True),
                   sa.Column('message', sa.String(255)),
                   sa.Column('created_date', sa.Date, default=datetime.utcnow()))
models = (Message,)
__all__ = [models, Message]
