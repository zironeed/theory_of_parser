from bs4 import BeautifulSoup
import requests
import re

from services.get_pages import get_page_numbers
from services.get_request import get_requests


def main():
    links = get_page_numbers('https://easyoffer.ru/rating/python_developer')
    get_requests(links)


if __name__ == '__main__':
    main()
