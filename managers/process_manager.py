import csv

from parse_manager import ParseManager
from db_manager import DatabaseManager


class ProcessManager:
    """
    Класс, объединяющий процессы парсинга и сохранения данных
    """
    def __init__(self, database: str, user: str, password: str, host: str, main_url: str, secondary_url: str) -> None:
        self.database = database
        self.user = user
        self.password = password
        self.host = host

        self.main_url = main_url
        self.secondary_url = secondary_url

        self.parse_manager = ParseManager(main_url, secondary_url)
        self.db_manager = DatabaseManager(database, user, password, host)

    async def parse_process(self):
        pass

    async def save_process(self):
        pass

    @staticmethod
    def save_to_csv(questions: list, categories: list):
        """
        Сохраняем вопросики в CSV-файл
        :param questions: вопросы
        :param categories: список категорий
        :return: пусто, сохранение инфы
        """
        print('saving questions to a CSV-file...')

        file_name = 'data.csv'

        with open(file_name, 'w', newline='', encoding='UTF-8') as file:
            fieldnames = ['question', 'answer', 'category']

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for ind in range(len(questions)):
                writer.writerow({
                    'question': questions[ind][0],
                    'answer': questions[ind][1],
                    'category': categories[ind]
                })

    async def main_process(self):
        pass
