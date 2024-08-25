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
        conn = await self.get_connect()
        try:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS questions(
                    id SERIAL PRIMARY KEY,
                    category VARCHAR(100),
                    question TEXT,
                    answer TEXT
                )
            """)
        except asyncpg.DuplicateTableError:
            print('Table already exists')
        finally:
            conn.close()

    async def save_to_sql(self, csv_file):
        """
        Сохранение данных из CSV-файла в БД
        :return: None
        """
        conn = await self.get_connect()

        try:
            async with aiofiles.open(csv_file, 'r', encoding='utf-8') as file:
                rows = [row async for row in aiocsv.AsyncDictReader(file)]

            async with conn.transaction():
                for row in rows:
                    conn.execute(f"""
                    INSERT INTO questions (category, question, answer)
                    VALUES {row['category']} {row['question']} {row['answer']}
                    """)
        finally:
            conn.close()

    async def setup_database(self):
        """
        Совмещение функций по созданию базы данных и таблицы
        :return: None
        """
        await self.create_database()
        await self.create_table()
