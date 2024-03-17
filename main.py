from services.get_and_save import get_page_numbers, get_requests, save_to_csv, get_categories


def main():
    links = get_page_numbers('https://easyoffer.ru/rating/python_developer')
    categories = get_categories('https://easyoffer.ru/rating/python_developer')
    questions = get_requests(links)
    save_to_csv(questions, categories)


if __name__ == '__main__':
    main()
