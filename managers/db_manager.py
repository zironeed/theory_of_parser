import aiofiles
import aiocsv
import asyncpg


class DatabaseManager:
    """
    Класс для взаимодействия с базой данных и таблицей
    """

    def __init__(self, database: str, user: str, password: str, host: str) -> None:
        self.database = database
        self.user = user
        self.password = password
        self.host = host

    async def get_connect(self) -> None:
        """
        Подключение к базе данных
        """
        return await asyncpg.connect(database=self.database, host=self.host, user=self.user, password=self.password)

    async def create_database(self) -> None:
        """
        Создание базы данных/проверка на существование БД
        """
        conn = await self.get_connect()
        try:
            await conn.execute(f'CREATE DATABASE {self.database}')
        except asyncpg.DuplicateDatabaseError:
            print(f'Database {self.database} already exists')
        finally:
            await conn.close()

    async def create_table(self) -> None:
        """
        Создание таблицы/проверка на существование таблицы в БД
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
            await conn.close()

    async def save_to_sql(self, csv_file: str) -> None:
        """
        Сохранение данных из CSV-файла в таблицу БД
        """
        conn = await self.get_connect()

        try:
            async with aiofiles.open(csv_file, 'r', encoding='utf-8') as file:
                rows = [row async for row in aiocsv.AsyncDictReader(file)]

            async with conn.transaction():
                for row in rows:
                    await conn.execute(f"""
                    INSERT INTO questions (category, question, answer)
                    VALUES ($1, $2, $3)
                    """, row['category'], row['question'], row['answer'])
        finally:
            await conn.close()

    async def setup_database(self) -> None:
        """
        Совмещение методов создания базы данных и таблицы
        """
        await self.create_database()
        await self.create_table()

    async def start(self, csv_file: str) -> None:
        """
        Запуск БД менеджера
        :param csv_file: csv-файл с данными
        """

        await self.setup_database()
        await self.save_to_sql(csv_file)
