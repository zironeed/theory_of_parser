import asyncio
from time import time

from services.get_and_save import get_page_numbers, get_requests, save_to_csv, get_categories   # sync

from services_async import get_info_from_page, save_info                                        # async


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
    links, categories = [], []

    url = 'https://easyoffer.ru/rating/python_developer'
    pages = await get_info_from_page.get_pagination(url)

    for page in pages:
        url += f'?page={page}'
        links.append(await get_info_from_page.get_page_numbers(url))
        categories.append(await get_info_from_page.get_categories(url))


    print('getting information from pages (about answers)...')
    questions = await asyncio.gather(*[get_info_from_page.get_requests(link) for link in links])
    print('done!')

    save_info.save_to_csv(questions, categories)

    print(time()-start)


if __name__ == '__main__':
    if int(input("0 - sync, 1 - async\n")):
        asyncio.run(async_main())
    else:
        main()
