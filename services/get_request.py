from bs4 import BeautifulSoup
import requests


def get_requests(links):
    questions = []

    for link in links:
        req = requests.get("https://easyoffer.ru/question/" + link)
        soup = BeautifulSoup(req.text, 'lxml')

        title = soup.find_all('h1', class_='mt-5 mb-5 fs-3')
        text = soup.find_all('p', class_='card-text')

        questions.append((title, text))
