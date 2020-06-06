import os
import re


def get_templates():
    '''
    Функция возвращает список с названиями файлов .txt, содержащих шаблоны на макроязыке
    path - путь к файлам.
    '''

    files = os.listdir(PATH)
    temps = [f for f in files if f.endswith('.txt')]
    return temps


def search_pattern(temps, pattern):
    '''
    Функция ищет pattern в файлах с шаблоном на макроязыке
    м возвращет список файлов с pattern.

    temps - список с названиями файлов
    pattern - шаблон поиска для регулярных выражений
    '''

    temps_with_pattern = []

    for temp in temps:
        with open(f'{PATH}{temp}', 'r', encoding='utf-8') as tmp:
            text = tmp.readlines()
            text_to_str = ''.join(text)
            if re.search(pattern, text_to_str, re.IGNORECASE):
                temps_with_pattern.append(f'{temp}')

    return temps_with_pattern


def analyze(temps):
    '''
    Функция проверяет наоичие определённых блоков (using, where, generate) в шаблоне
    и возвращает кортеж со списками фалов следующего вида:
    ([нет блока Generate()], [нет блока using()], [нет блока Where()], [полноценные шаблоны])
    '''

    template_categories = {}
    # Ищем файлы без блока generate
    temps_with_generate_unit = search_pattern(temps, pattern=r'generate\([\s\S^)]+?\)')
    temps_with_no_generate_unit = [temp for temp in temps if temp not in temps_with_generate_unit]
    template_categories['no_generate_unit'] = temps_with_no_generate_unit
    # Ищем файлы без блока using
    temps_with_ad_unit = search_pattern(temps_with_generate_unit, pattern=r'using\([\s\S^)]+?\)')
    temps_with_no_ad_unit = [temp for temp in temps_with_generate_unit if temp not in temps_with_ad_unit]
    template_categories['no_using_unit'] = temps_with_no_ad_unit
    # Ищем файлы без блока where
    temps_with_description_unit = search_pattern(temps_with_ad_unit, pattern=r'where\([\s\S^)]+?\)')
    temps_with_no_description_unit = [temp for temp in temps_with_ad_unit if temp not in temps_with_description_unit]
    template_categories['no_where_unit'] = temps_with_no_description_unit
    # Добавляем полноценные шаблоны
    template_categories['full_fledged'] = temps_with_description_unit
    return template_categories


def get_body(temp, area):
    '''
    Функция возвращает содержимое указанного блока в виде строки.
    '''

    if area.lower() == 'using':
        pattern = r'using\([\s\S^)]+?\)'
        cute_start = 6

    if area.lower() == 'where':
        pattern = r'where\([\s\S^)]+?\)'
        cute_start = 6

    if area.lower() == 'generate':
        pattern = r'generate\([\s\S^)]+?\)'
        cute_start = 9

    with open(f'{PATH}{temp}', 'r', encoding='utf-8') as tmp:
        text = tmp.readlines()
        text_to_str = ''.join(text)
        search_body = re.search(pattern, text_to_str, re.IGNORECASE)
        body = search_body.group()
        body = body[cute_start: -1]
    return body


def using_analyze(body):
    '''
    Функция анализирует содержимое блока using
    и возвращает словарь со списком объектов и True,
    если в блоке using используется * (обозначет оператор).
    '''

    used_entities = {}
    used_entities['objects'] = re.findall(r'\$[a-zA-Z]+', body)
    used_entities['operator'] = '!op' in body
    return used_entities


def description_analyze(body, object_name):
    '''
    Функция фуенкция возвращает словарь с описанием свойств (атрибутов) объекта.
    '''

    information = {}

    if '$' in object_name:
        object_name = object_name.replace('$', '\$')
        field_names = ['Type', 'SyntaxType', 'id', 'value']

    if object_name == '!op':
        object_name = object_name.replace('!', '\!')
        field_names = ['Vals']

    for field_name in field_names:
        pattern = f'{object_name}.{field_name}[\s\S]*?;'
        description_march = re.search(pattern, body, re.IGNORECASE)
        if not description_march:
            information[f'{field_name}'] = []
            continue
        description = description_march.group()
        pattern_accuracy = r'>[\s\S]*?;'
        description_accuracy_march = re.search(pattern_accuracy, description)
        if not description_accuracy_march:
            information[f'{field_name}'] = []
            continue
        description_accuracy = description_accuracy_march.group()

        if field_name.lower() == 'vals':
            # Изменить регулярное выражение!!!
            res_pattern = r'[\S^,]+'
            res_description = re.findall(res_pattern, description_accuracy[1:-1], re.IGNORECASE)
            # if res_description:
            #     res_description = res_description.group()
            #     if ',' in res_description:
            #         res_description = res_description.replace(' ', '')
            #         res_description = res_description.split(',')
            information[f'{field_name}'] = res_description

        if field_name.lower() == 'type' or field_name.lower() == 'syntaxtype':
            res_pattern = r'[a-zA-Z]+'
            res_description = re.findall(res_pattern, description_accuracy[1:-1], re.IGNORECASE)
            information[f'{field_name}'] = res_description

        if field_name.lower() == 'id':
            res_pattern = r'[a-zA-Z_]'
            res_description = re.findall(res_pattern, description_accuracy[1:-1], re.IGNORECASE)
            information[f'{field_name}'] = res_description

        if field_name.lower() == 'value':
            if '"' in description_accuracy:
                res_pattern = r'"[\s\S^"]+"'
            else:
                res_pattern = r'[\.\d]+'
            res_description = re.search(res_pattern, description_accuracy[1:-1], re.IGNORECASE)
            if res_description:
                res_description = res_description.group().lstrip()
            information[f'{field_name}'] = res_description
    return information


def where_analyze(body, info):
    '''
    Функция анализирует содержимое блока where и возвращает словарь с описанием объектов.
    Структура словаря {'Объект': {'Свойство': [Значения]}}

    Пример:
    {'$A': {'Type': ['char'], 'SyntaxType': ['var'], 'id': ['a'], 'value': '"4.5"'},
    '$B': {'Type': ['int'], 'SyntaxType': ['var'], 'id': ['b'], 'value': '5'},
    '!op': {'Vals': ['+', '-']}}
    '''

    objects = info['objects']
    operator = info['operator']

    objects_info = {}

    for object in objects:
        information = description_analyze(body, object)
        objects_info[f'{object}'] = information

    if operator:
        information = description_analyze(body, '!op')
        objects_info['!op'] = information

    return  objects_info


PATH = 'templates/'

# Проверка функций
temps = get_templates()
cats = analyze(temps) # категории шблонов (словарь)
full_temp = cats['full_fledged'] # полноценные шаблоны (список)
using_body = get_body(full_temp[0], 'using') # блок описания using (строка)
info = using_analyze(using_body) # словарь, содержащий список объвленных объектов и флаг использования оператора
where_body = get_body(full_temp[0], 'where') # Строка - содержимое блока where
print(where_analyze(where_body, info)) # Словарь - описание объектов