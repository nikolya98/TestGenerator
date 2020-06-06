from analyzer import *


def generate(path, test_name, body):
    '''
    Функция записывает строку body в файл path/test_name.c.
    '''
    # Подумать над расположением файлов...
    test_file = open(f'{path}{test_name}'.replace('.txt', '.c'), 'w', encoding='utf-8')
    test_file.write(body)
    test_file.close()


def no_generate_unit(temps):
    '''
    Функция добавляет комментарий и тело шаблона в tests/no_generate_error/temp_name.c
    в случае, если в блоке generate() допущена ошибка или он не задан.
    '''

    path = 'tests/no_generate_error/'

    for temp in temps:
        comment = '//Блок Generate() отсутствует или некорректно задан!\n'
        body = get_body(temp, 'temp_body')
        body = '/*' + body + '*/'
        res = comment + body
        generate(path, temp, res)



# Проверка функций
temps = get_templates()
cats = analyze(temps) # категории шблонов (словарь)
no_gen = cats['no_generate_unit']
no_generate_unit(no_gen)

# full_temp = cats['full_fledged'] # полноценные шаблоны (список)
# using_body = get_body(full_temp[0], 'using') # блок описания using (строка)
# info = using_analyze(using_body) # словарь, содержащий список объвленных объектов и флаг использования оператора
# where_body = get_body(full_temp[0], 'where') # Строка - содержимое блока where
# print(where_analyze(where_body, info)) # Словарь - описание объектов