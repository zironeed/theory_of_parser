from services.get_and_save import get_page_numbers, get_requests, save_to_csv


def main():
    links = get_page_numbers('https://easyoffer.ru/rating/python_developer')
    questions = get_requests(links)
    save_to_csv(questions)


if __name__ == '__main__':
    main()
