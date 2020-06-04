import os
import re


def get_tamplates(path):
    '''
    Функция возвращает список с названиями файлов .txt, содержащих шаблоны на макроязыке
    '''

    files = os.listdir(path)
    temps = [f for f in files if f.endswith('.txt')]
    return temps


# Переместить в другое место
def generate():
    '''
    Функция построчно читает шаблоны .txt, расположенный в path
    и осуществляет запись в tests/test_name.c'
    '''

    for temp in temps:
        with open(f'{path}{temp}', 'r', encoding='utf-8') as tmp:
            line = tmp.readline()
            test = open(f'tests/test_{temp.replace(".txt", "")}.c', 'w+', encoding='utf-8')

            while line:
                test.write(line)
                line = tmp.readline()

            test.close()


def search_pattern(temps, pattern):
    '''
    Функция ищет pattern в файле с шаблоном на макроязыке
    м возвращет список файлов с pattern
    '''

    temps_with_pattern = []

    for temp in temps:
        with open(f'{path}{temp}', 'r', encoding='utf-8') as tmp:
            line = tmp.readline()
            while line:
                if re.match(pattern, line, re.IGNORECASE):
                    temps_with_pattern.append(f'{temp}')
                    break
                line = tmp.readline()

    return temps_with_pattern


path = 'templates/'
temps = get_tamplates(path)
temps_with_ad_unit = search_pattern(temps, pattern=r'^using\([\s\S]+\)')
temps_with_description_unit = search_pattern(temps, pattern=r'^where\(')
temps_with_generate_unit = search_pattern(temps, pattern=r'^generate\(')


