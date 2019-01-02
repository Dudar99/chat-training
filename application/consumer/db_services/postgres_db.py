'''
Module for Postgres database manager
'''
from aiopg.sa import create_engine
from consumer.config import Configs
from consumer.models import models_pg
# from consumer.app import LOGGER
from consumer.models import Message


class PGManager:
    '''
    Class that manage data in Postgres
    '''
    @classmethod
    async def create_engine(cls):
        '''
        Methos which create new PG engine
        :return:  new Engine
        '''
        return await create_engine(
            user=Configs['POSTGRES_USER'],
            database=Configs['POSTGRES_DATABASE'],
            host=Configs['POSTGRES_ADDRESS'],
            password=Configs['POSTGRES_PASSWORD']
        )

    @classmethod
    async def init_tables(cls):
        '''
        Method which create all tables from sql alchemy models
        :return: None
        '''
        from sqlalchemy.sql.ddl import CreateTable
        engine = await cls.create_engine()
        async with engine.acquire() as conn:
            for model in models_pg:
                try:
                    await conn.execute(CreateTable(model))
                except Exception as e:
                    continue

    @classmethod
    async def insert_into_table(cls, msg):
        '''
        Insert message into table
        :param msg: string
        :return: None
        '''
        engine = await PGManager.create_engine()
        async with engine.acquire() as conn:
            await conn.execute(Message.insert().values(message=msg))

    @classmethod
    async def table_row_count(cls, table):
        '''

        :param table: from what you want to retrieve row count
        :return: amount of rows
        '''
        engine = await PGManager.create_engine()
        async with engine.acquire() as conn:
            async with conn.execute(table.select()) as cur:
                return cur.rowcount
