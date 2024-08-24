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

    async def create_database(self):
        """
        Создание базы данных, если она не существует
        :return: None
        """

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
