import csv


def save_to_csv(questions: list, categories: list):
    """
    Сохраняем вопросики в CSV-файл
    :param questions: вопросы
    :param categories: список категорий
    :return: пусто
    """
    print('saving questions to a CSV-file...')

    file_name = 'data.csv'

    with open(file_name, 'w', newline='', encoding='UTF-8') as file:
        fieldnames = ['question', 'answer', 'category']

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for ind in range(len(questions)):
            writer.writerow({
                'question': questions[ind][0],
                'answer': questions[ind][1],
                'category': categories[ind]
            })

    print('done!')