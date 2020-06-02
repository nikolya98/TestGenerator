import os


def generate(path):
    # Функция построчно читает шаблоны .txt из path
    # И осуществляет запись в tests/test_name.c
    if not path:
        path = 'templates/'

    files = os.listdir(path)
    temps = [f for f in files if f.endswith('.txt')]

    for temp in temps:
        with open(f'{path}{temp}', 'r', encoding='utf-8') as tmp:
            line = tmp.readline()
            test = open(f'tests/test_{temp.replace(".txt", "")}.c', 'w+', encoding='utf-8')

            while line:
                test.write(line)
                line = tmp.readline()

            test.close()


