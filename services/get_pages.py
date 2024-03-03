from bs4 import BeautifulSoup
import requests
import re


def get_page_numbers(url):
    links = []
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    quotes = soup.find_all('a', class_='link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0 link-underline-opacity-75-hover')

    for link in quotes:
        page_number = re.search(r'/(\d+)', link.get('href')).group(1)
        links.append(page_number)

    return links
