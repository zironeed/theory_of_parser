import aiohttp
from bs4 import BeautifulSoup
import csv
import re


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def get_categories(url):
    """
    Получаем категории вопросов
    :param url: урл
    :return: список категорий
    """
    print('getting categories...')

    categories = []

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'lxml')
        cats = soup.find_all('td', class_='d-none d-sm-table-cell')

        for category in cats:
            cat = re.sub(r'<[^>]*>', '', str(category))
            categories.append(cat)

    print('done!')
    return categories


async def get_page_numbers(url):
    """
    Получаем номера страниц
    :param url: урл
    :return: необходимые ссылки на страницы
    """
    print('getting links to pages...')

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

    print('done!')
    return links


async def get_requests(link):
    """
    Получаем информацию со страниц
    :param link: страницы
    :return: список вопросов (список кортежей)
    """

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, "https://easyoffer.ru/question/" + link)
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


def save_to_csv(questions: list, categories: list):
    """
    Сохраняем вопросики в CSV-файл
    :param questions: вопросы
    :param categories: список категорий
    :return: пусто
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

    print('done!')
