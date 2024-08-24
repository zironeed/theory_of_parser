import asyncio
import aiofiles
import asyncpg
import aiocsv
from os import getenv


class DatabaseManager:
    """
    Класс для взаимодействия с базой данных и данными в ней
    """

    def __init__(self):
        self.database = getenv('DB_NAME')
        self.user = getenv('DB_USER')
        self.password = getenv('DB_PASSWORD')
        self.host = getenv('DB_HOST')

    async def get_connect(self):
        return await asyncpg.connect(database=self.database, host=self.host, user=self.user, password=self.password)

    async def create_database(self):
        """
        Создание базы данных, если она не существует
        :return: None
        """
        conn = await self.get_connect()
        try:
            await conn.execute(f'CREATE DATABASE {self.database}')
        except asyncpg.DuplicateDatabaseError:
            print(f'Database {self.database} already exists')
        finally:
            conn.close()

    async def create_table(self):
        """
        Создание таблицы, если она не существует
        :return: None
        """
        pass

    async def save_to_sql(self):
        """
        Сохранение данных из CSV-файлы в БД
        :return:
        """
        pass

    async def setup_database(self):
        """
        Совмещение функций по созданию базы данных и таблицы
        :return:
        """
        pass
