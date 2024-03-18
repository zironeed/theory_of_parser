from bs4 import BeautifulSoup
import csv
import requests
import re


def get_categories(url):
    """
    Получаем категории вопросов
    :param url: урл
    :return: список категорий
    """
    print('getting categories...')

    categories = []
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    cats = soup.find_all('td', class_='d-none d-sm-table-cell')

    for category in cats:
        cat = re.sub(r'<[^>]*>', '', str(category))
        categories.append(cat)

    print('done!')
    return categories


def get_page_numbers(url):
    """
    Получаем номера страниц
    :param url: урл
    :return: необходимые ссылки на страницы
    """
    print('getting links to pages...')

    links = []
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    quotes = soup.find_all('a', class_='link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover')

    for link in quotes:
        page_number = re.search(r'/(\d+)', link.get('href')).group(1)
        links.append(page_number)

    print('done!')
    return links


def get_requests(links):
    """
    Получаем информацию со страниц
    :param links: страницы
    :return: список вопросов (список кортежей)
    """
    print('getting information from pages...')

    questions = []

    for link in links:
        req = requests.get("https://easyoffer.ru/question/" + link)
        soup = BeautifulSoup(req.text, 'lxml')

        title = soup.find_all('h1', class_='mt-5 mb-5 fs-3')
        title_text = re.sub('<[^<]+?>', '', str(title[0]))

        text = soup.find_all('div', class_='card-body')
        text_list = [re.sub('<[^<]+?>', '', str(p)) for p in text]

        if text_list != []: text_list = text_list[0].split('\n')[1:-2]
        text_str = ' '.join(text_list)
        for i in ['\xa0', '\r', '\u202F']:
            text_str = text_str.replace(i, ' ')

        questions.append((title_text, text_str))

    print('done!')
    return questions


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
