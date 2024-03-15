from bs4 import BeautifulSoup
import requests
import re


def get_page_numbers(url):
    """
    Получаем номера страниц
    :param url: урлы
    :return: необходимые ссылки на страницы
    """
    links = []
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    quotes = soup.find_all('a', class_='link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover')

    for link in quotes:
        page_number = re.search(r'/(\d+)', link.get('href')).group(1)
        links.append(page_number)

    return links


def get_requests(links):
    """
    Получаем информацию со страниц
    :param links: страницы
    :return: список вопросов (список кортежей)
    """
    questions = []

    for link in links:
        req = requests.get("https://easyoffer.ru/question/" + link)
        soup = BeautifulSoup(req.text, 'lxml')

        title = soup.find_all('h1', class_='mt-5 mb-5 fs-3')
        title_text = re.sub('<[^<]+?>', '', str(title[0]))

        text = soup.find_all('p', class_='card-text')
        text_list = [re.sub('<[^<]+?>', '', str(p)) for p in text]
        text_list = [p.replace('\n\n', '') for p in text_list]

        questions.append((title_text, text_list))

    return questions


def save_to_db(questions: list):
    """
    Сохраняем вопросики в БД
    :param questions: вопросы
    :return: пока не придумал
    """
    pass
