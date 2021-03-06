"""
Module for Cassandra database manager
"""
import asyncio
from cassandra.cqlengine.management import sync_table

from consumer.models import models_cs
from cassandra.cqlengine import connection
from consumer.app import LOGGER, Configs
from consumer.app import SESSION



class CassandraManager:
    """
    Class that manages data in cassandra
    """
    connection: connection = None

    @classmethod
    async def _init_tables(cls):
        """
        Method that create all tables from cassandra models
        :return: None
        """
        while True:
            try:
                cls.connection = await connection.setup(hosts=[Configs['CASSANDRA_HOST']], default_keyspace="chat_1")
                LOGGER.info("Connected with Cassandra")
                break
            except Exception as e:
                LOGGER.error(f"Cassandra: {e}\n :try to reconnect in 4 second...")
                await asyncio.sleep(20)
        async for model in models_cs:
            try:
                await sync_table(model)
                LOGGER.info(f"Table {model.info} was created")
            except Exception as e:
                LOGGER.error(f"Table { model.info} already exist")

    @classmethod
    def create_keyspace(cls):
        """
        Method which create key space if it does not exist
        :return:
        """
        SESSION.execute("""
                            CREATE KEYSPACE IF NOT EXISTS %s
                            WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
                            """ % 'chat_1')

    @classmethod
    def create(cls):
        """
        Method which allow to create table
        :return:
        """
        LOGGER.info("Key space setting and creating table")
        SESSION.execute("""
                            CREATE TABLE IF NOT EXISTS messages (
                                id text,
                                message text,
                            PRIMARY KEY (id)
                          )
                            """)

    @classmethod
    async def insert(cls, id, message):
        """
        With this method you can insert data into cassandra table
        :param id:
        :param message:
        :return:
        """
        try:
            SESSION.execute_async("INSERT INTO messages (id, message) VALUES (%s, %s)",
                                  (id, message)).result()
            LOGGER.info(f"Message {message} was inserted into table Message")
        except Exception as e:
            LOGGER.error(f"{e}")

    @classmethod
    async def select_count(cls):
        """
        :return: count of rof in Message table
        """
        res = SESSION.execute_async("SELECT COUNT(*)  FROM messages").result()
        return res[0][0]
