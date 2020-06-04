import os
import re


def get_templates(path):
    '''
    Функция возвращает список с названиями файлов .txt, содержащих шаблоны на макроязыке
    '''

    files = os.listdir(path)
    temps = [f for f in files if f.endswith('.txt')]
    return temps


# Переместить в другое место???
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


def generate_error():
    pass


def search_pattern(temps, pattern):
    '''
    Функция ищет pattern в файле с шаблоном на макроязыке
    м возвращет список файлов с pattern
    '''

    temps_with_pattern = []

    for temp in temps:
        with open(f'{path}{temp}', 'r', encoding='utf-8') as tmp:
            text = tmp.readlines()
            text_to_str = ''.join(text)
            if re.search(pattern, text_to_str, re.IGNORECASE):
                temps_with_pattern.append(f'{temp}')

    return temps_with_pattern


path = 'templates/'
temps = get_templates(path)


def no_generate_error(temp):

    test = open(f'tests/test_{temp.replace(".txt", "")}.c', 'w+', encoding='utf-8')
    test.write(f'В шаблоне {temp} отсутствует или некорректно оформлен блок "Generate()"!')


def analyze(temps):
    '''
    Функция проверяет наоичие определённых блоков (using, where, generate) в шаблоне
    и в зависимости от результата выполняет соответствующие действия
    '''

    # Для шаблонов, не содержащих блока generate выводим ошибку
    # Блок generate является обязвтельным!!!
    temps_with_generate_unit = search_pattern(temps, pattern=r'^generate\([\s\S]+\)')
    temps_with_no_generate_unit = [temp for temp in temps if temp not in temps_with_generate_unit]
    for temp in temps_with_no_generate_unit:
        no_generate_error(temp)

    # Среди шаблонов, содержищих блок generate ищем шаблоны с блоком using
    # Блок using опциональный, и в зависимости от его наличия либо ищем блок where,
    # либо генерируем тест без создания объектов и каких-либо замен...
    temps_with_ad_unit = search_pattern(temps_with_generate_unit, pattern=r'^using\([\s\S]+\)')
    temps_with_description_unit = search_pattern(temps_with_ad_unit, pattern=r'^where\([\s\S]+\)') # Содержат where()
    temps_with_no_description_unit = [temp for temp in temps_with_ad_unit if temp not in temps_with_description_unit]
    for temp in temps_with_ad_unit:
        if temp in temps_with_description_unit:
            pass # Действие, если есть блок Where
        else:
            pass # Действие, если блок Where отсутствует

