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
        """
        Загрузка данных со страницы
        :param session: aiohttp сессия
        :param url: url-адрес страницы
        :return: текст страницы
        """
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
        categories = []

        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, pagination_num)
            soup = BeautifulSoup(html, 'lxml')
            cats = soup.find_all('td', class_='d-none d-sm-table-cell')

            for category in cats:
                cat = re.sub(r'<[^>]*>', '', str(category))
                categories.append(cat)

        return categories

    async def get_page_numbers(self, pagination_num: int) -> list:
        """
        Получаем номера страниц вопросов
        :param pagination_num: номер страницы каталога
        :return: необходимые ссылки на страницы
        """
        links = []

        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, pagination_num)
            soup = BeautifulSoup(html, 'lxml')
            quotes = soup.find_all('a',
                                   class_='link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 '
                                          'link-underline-opacity-75-hover')

            for link in quotes:
                page_number = re.search(r'/(\d+)', link.get('href')).group(1)
                links.append(page_number)

        return links

    async def get_requests(self, link) -> list[tuple]:
        """
        Получаем информацию со страниц
        :param link: url вопроса
        :return: список вопросов
        """
        pass
