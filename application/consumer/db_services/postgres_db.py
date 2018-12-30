from aiopg.sa import create_engine
from consumer.config import Configs
from consumer.models import models_pg
# from consumer.app import LOGGER
from consumer.models import Message

class PGManager:

    @classmethod
    async def create_engine(cls):
        return await create_engine(
            user=Configs['POSTGRES_USER'],
            database=Configs['POSTGRES_DATABASE'],
            host=Configs['POSTGRES_ADDRESS'],
            password=Configs['POSTGRES_PASSWORD']
        )

    @classmethod
    async def init_tables(cls):
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
        engine = await PGManager.create_engine()
        async with engine.acquire() as conn:
            await conn.execute(Message.insert().values(message=msg))

    @classmethod
    async def table_row_count(cls, table):
        engine = await PGManager.create_engine()
        async with engine.acquire() as conn:
            async with conn.execute(table.select()) as cur:
                return cur.rowcount
