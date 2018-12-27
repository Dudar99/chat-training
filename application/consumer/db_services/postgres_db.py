from aiopg.sa import create_engine
from config import DATABASE
from consumer.models import models
from consumer.app import LOGGER
from consumer.models import Message

class PGManager:

    @classmethod
    async def create_engine(cls):
        return await create_engine(
            user=DATABASE['POSTGRES_USER'],
            database=DATABASE['DB_NAME'],
            host=DATABASE['HOST'],
            password=DATABASE['POSTGRES_PASSWORD']
        )

    @classmethod
    async def init_tables(cls):
        from sqlalchemy.sql.ddl import CreateTable
        engine = await cls.create_engine()
        async with engine.acquire() as conn:
            for model in models:
                try:
                    await conn.execute(CreateTable(model))
                    LOGGER.info(f'Table {model.name} was created')
                except Exception as e:
                    LOGGER.info(f'Error occured when creating {model.name}: {e}')

    @classmethod
    async def insert_into_table(cls, msg):
        engine = await PGManager.create_engine()
        async with engine.acquire() as conn:
            await conn.execute(Message.insert().values(message=msg))
