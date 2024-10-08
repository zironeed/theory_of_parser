import asyncio
from os import getenv
from dotenv import load_dotenv

from managers.parse_manager import ParseManager
from services_async import get_info_from_page, save_info
from managers.db_manager import DatabaseManager


env_path = '.env'
load_dotenv(dotenv_path=env_path)


async def async_main():
    db_manager = DatabaseManager(
        database=getenv('DB_NAME'),
        user=getenv('DB_USER'),
        password=getenv('DB_PASSWORD'),
        host=getenv('DB_HOST')
    )

    parse_manager = ParseManager(
        main_url=getenv('MAIN_URL'),
        secondary_url=getenv('SECONDARY_URL')
    )

    links, categories = [], []
    semaphore = asyncio.Semaphore(100)

    url = getenv('MAIN_URL')
    print('getting pages...')
    pages = await get_info_from_page.get_pagination(url)
    print('getting pages - done!')

    print('getting categories and links...')
    for page in pages:
        page_url = url + f'?page={page}'
        links.extend(await get_info_from_page.get_page_numbers(page_url))
        categories.extend(await get_info_from_page.get_categories(page_url))
    print('getting categories and links - done!')

    print('getting information from pages (about answers)...')
    questions = await asyncio.gather(*[get_info_from_page.get_requests(link, semaphore) for link in links])
    print('getting information from pages (about answers) - done!')

    save_info.save_to_csv(questions, categories)

    print('working with database...')
    await db_manager.setup_database()
    await db_manager.save_to_sql('data.csv')
    print('working with database - done!')


if __name__ == '__main__':
    asyncio.run(async_main())
