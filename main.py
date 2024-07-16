import asyncio
from time import time

from services.get_and_save import get_page_numbers, get_requests, save_to_csv, get_categories   # sync

from services_async import get_info_from_page, save_info    # async


def main():
    start = time()

    url = 'https://easyoffer.ru/rating/python_developer'

    links = get_page_numbers(url)
    categories = get_categories(url)

    questions = get_requests(links)

    save_to_csv(questions, categories)

    print(time()-start)


async def async_main():
    start = time()

    url = 'https://easyoffer.ru/rating/python_developer'

    links = await get_info_from_page.get_page_numbers(url)
    categories = await get_info_from_page.get_categories(url)
    pages = await get_info_from_page.get_pagination(url)

    print('getting information from pages (about answers)...')
    tasks = [asyncio.create_task(get_info_from_page.get_requests(link)) for link in links]
    questions = await asyncio.gather(*tasks)
    print('done!')

    save_info.save_to_csv(questions, categories)

    print(time()-start)


if __name__ == '__main__':
    if int(input("0 - sync, 1 - async\n")):
        asyncio.run(async_main())    # ~ 4.3-5.6  sec
    else:
        main()    # - 48.5 sec
    # балдеж
