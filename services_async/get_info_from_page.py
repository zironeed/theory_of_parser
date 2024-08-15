from os import getenv
import aiohttp
from bs4 import BeautifulSoup
import re


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def get_pagination(url):
    """
    Получаем количество страниц с вопросами
    :param url: урл
    :return: ссылки на следующие страницы
    """
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'lxml')
        pages = soup.find_all('a', class_='page-link')

        for page in range(len(pages)):
            pages[page] = re.sub(r'<a[^>]*>(\d+)<\/a>', r'\1', str(pages[page]))

        pages.append(1)

        return pages


async def get_categories(url):
    """
    Получаем категории вопросов
    :param url: урл
    :return: список категорий
    """

    categories = []

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'lxml')
        cats = soup.find_all('td', class_='d-none d-sm-table-cell')

        for category in cats:
            cat = re.sub(r'<[^>]*>', '', str(category))
            categories.append(cat)

    return categories


async def get_page_numbers(url):
    """
    Получаем номера страниц вопросов
    :param url: урл
    :return: необходимые ссылки на страницы
    """

    links = []

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'lxml')
        quotes = soup.find_all('a',
                               class_='link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 '
                               'link-underline-opacity-75-hover')

        for link in quotes:
            page_number = re.search(r'/(\d+)', link.get('href')).group(1)
            links.append(page_number)

    return links


async def get_requests(link, sem):
    """
    Получаем информацию со страниц
    :param link: страницы
    :return: список вопросов (список кортежей)
    """
    async with sem:
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, getenv('SECONDARY_URL') + link)
            soup = BeautifulSoup(html, 'lxml')

            title = soup.find_all('h1', class_='mt-5 mb-5 fs-3')
            title_text = re.sub('<[^<]+?>', '', str(title[0]))

            text = soup.find_all('div', class_='card-body')
            text_list = [re.sub('<[^<]+?>', '', str(p)) for p in text]

        if text_list:
            text_list = text_list[0].split('\n')[1:-2]
        text_str = ' '.join(text_list)
        for i in ['\xa0', '\r', '\u202F']:
            text_str = text_str.replace(i, ' ')

    return title_text, text_str
