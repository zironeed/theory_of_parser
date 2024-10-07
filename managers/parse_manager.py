import asyncio
import re

import aiohttp
from bs4 import BeautifulSoup


class ParseManager:
    """
    Класс для парсинга данных
    """

    def __init__(self, main_url, secondary_url):
        self.main_url = main_url
        self.secondary_url = secondary_url
        self.semaphore = asyncio.Semaphore(100)

    @staticmethod
    async def fetch(session, url):
        async with session.get(url) as response:
            return await response.text()

    async def get_pagination(self) -> list:
        """
        Получаем количество страниц с вопросами
        :return: ссылки на страницы списков
        """
        async with aiohttp.ClientSession() as session:
            page_numbers = []
            html = await self.fetch(session, self.main_url)
            soup = BeautifulSoup(html, 'lxml')
            pages = soup.find_all('a', class_='page-link')

            for page in range(len(pages)):
                page_numbers.append(re.sub(r'<a[^>]*>(\d+)<\/a>', r'\1', str(pages[page])))

            page_numbers.append(1)

            return page_numbers

    async def get_categories(self, pagination_num: int) -> list:
        """
        Получаем категории вопросов
        :param pagination_num: номер страницы каталога
        :return: список категорий
        """
        pass

    async def get_page_numbers(self, pagination_num: int) -> list:
        """
        Получаем номера страниц вопросов
        :param pagination_num: номер страницы каталога
        :return: необходимые ссылки на страницы
        """
        pass

    async def get_requests(self, link) -> list[tuple]:
        """
        Получаем информацию со страниц
        :param link: url вопроса
        :return: список вопросов
        """
        pass
