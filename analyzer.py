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


def description_analyze(body, object_name, field_name):
    '''
    Функция фуенкция возвращает строку с описанием объекта
    '''

    # if '$' in object_name:
    #     object_name = object_name.replace('$', r'\\\$')
    #     print(object_name)

    pattern = f'\\{object_name}.{field_name}[\s\S]+?;'
    description_march = re.search(pattern, body, re.IGNORECASE)
    description = description_march.group()
    pattern_accuracy = r'>[\s\S]+?;'
    description_accuracy_march = re.search(pattern_accuracy, description)
    description_accuracy = description_accuracy_march.group()

    if field_name.lower() == 'type' or 'syntaxtype':
        res_pattern = r'[a-zA-Z]+'
        res_description = re.findall(res_pattern, description_accuracy[1:-1], re.IGNORECASE)

    if field_name.lower() == 'id':
        res_pattern = r'[a-zA-Z_]'
        res_description = re.findall(res_pattern, description_accuracy[1:-1], re.IGNORECASE)

    if field_name.lower() == 'value':
        res_pattern = r'.*'
        res_description = re.search(res_pattern, description_accuracy[1:-1], re.IGNORECASE)
        res_description = res_description.group().lstrip()

    return res_description


def where_analyze(body, info):
    '''
    Функция анализирует содержимое блока where и ...
    '''

    objects = info['objects']

    objects_info = {}
    information = {}

    for object in objects:
        information['Type'] = description_analyze(body, object, 'Type')
        information['SyntaxType'] = description_analyze(body, object, 'SyntaxType')
        information['ID'] = description_analyze(body, object, 'id')
        information['Value'] = description_analyze(body, object, 'value')
        objects_info[f'{object}'] = information

    # if operator:
    #     pass

    return  objects_info


PATH = 'templates/'
temps = get_templates()


cats = analyze(temps) # категории шблонов (словарь)

full_temp = cats['full_fledged'] # полноценные шаблоны (список)
using_body = get_body(full_temp[0], 'using') # блок описания using (строка)
info = using_analyze(using_body) # словарь, содержащий список объвленных объектов и флаг использования оператора

where_body = get_body(full_temp[0], 'where')


# print(where_analyze(where_body, info))
# print(description_analyze(where_body, '$A', 'Type'))