import asyncio
import uuid
from cassandra.cqlengine.management import sync_table

from consumer.models import models
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection

cluster = Cluster(["cassandra"])

session = cluster.connect()


class CassandraManager:
    """
    Class that manages data in cassandra
    """
    connection: connection = None

    @classmethod
    async def _init_tables(cls):
        while True:
            try:
                cls.connection = await connection.setup(hosts=["cassandra"], default_keyspace="chat_1")
                break
            except Exception as e:
                print(f"try to reconect to cassandra{e}")
                await asyncio.sleep(4)
        async for model in models:
            try:
                await sync_table(model)
                print(f"Table {model.info} was created")
            except Exception as e:
                print("Cassandra cant create this tabvle already exist")

    @classmethod
    def create_keyspace(cls):
        session.execute("""
                            CREATE KEYSPACE IF NOT EXISTS %s
                            WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
                            """ % 'chat_1')

    @classmethod
    def create(cls):
        print("setting keyspace...")
        session = cluster.connect()
        session.set_keyspace('chat_1')
        print("creating table...")
        session.execute("""
                            CREATE TABLE IF NOT EXISTS messages (
                                id text,
                                message text,
                            PRIMARY KEY (id)
                          )
                            """)

    @classmethod
    async def insert(cls, id, message):
        session.set_keyspace('chat_1')
        try:
            session.execute_async("INSERT INTO messages (id, message) VALUES (%s, %s)",
                                  (id, message)).result()
        except Exception as e:
            print(e)

    @classmethod
    async def select_count(cls):
        session.set_keyspace('chat_1')
        res = session.execute_async("SELECT COUNT(*)  FROM messages").result()

        return res[0][0]
