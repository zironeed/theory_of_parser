import asyncio
from os import getenv
from time import time
from dotenv import load_dotenv
from services_async import get_info_from_page, save_info


env_path = '.env'
load_dotenv(dotenv_path=env_path)


async def async_main():
    start = time()
    links, categories = [], []
    semaphore = asyncio.Semaphore(100)

    url = getenv('MAIN_URL')
    print('getting pages...')
    pages = await get_info_from_page.get_pagination(url)
    print('done!')

    print('getting categories and links...')
    for page in pages:
        page_url = url + f'?page={page}'
        links.extend(await get_info_from_page.get_page_numbers(page_url))
        categories.extend(await get_info_from_page.get_categories(page_url))
    print('done!')

    print('getting information from pages (about answers)...')
    questions = await asyncio.gather(*[get_info_from_page.get_requests(link, semaphore) for link in links])
    print('done!')

    save_info.save_to_csv(questions, categories)

    print(time()-start)


if __name__ == '__main__':
    asyncio.run(async_main())
