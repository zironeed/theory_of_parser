import asyncio

from services.get_and_save import get_page_numbers, get_requests, save_to_csv, get_categories
from services_async import get_info
from time import time


def main():
    start = time()
    links = get_page_numbers('https://easyoffer.ru/rating/python_developer')
    categories = get_categories('https://easyoffer.ru/rating/python_developer')
    questions = get_requests(links)
    save_to_csv(questions, categories)
    print(time()-start)


async def async_main():
    start = time()
    links = await get_info.get_page_numbers('https://easyoffer.ru/rating/python_developer')
    categories = await get_info.get_categories('https://easyoffer.ru/rating/python_developer')

    tasks = [asyncio.create_task(get_info.get_requests(link)) for link in links]

    print('getting information from pages...')
    questions = await asyncio.gather(*tasks)
    print('done!')

    save_to_csv(questions, categories)
    print(time()-start)


if __name__ == '__main__':
    asyncio.run(async_main())

    # main() - 48.5 sec
    # asyncio.run(async_main()) - 4.3 sec
    # балдеж
