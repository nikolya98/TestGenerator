import os
import random


def get_identifier():
    '''
    Функция для генерации идентификатора объекта, если он не был задан в шаблоне.
    Возвращает символ из диапазона a-z.
    '''

    identifier = chr(random.choice(range(97, 123)))
    return identifier


def object_verify(obj, d_type, syn_type):
    '''
    Функция проверяет корректность созданного объекта.
    '''

    # Проверяем корректность указанного типа данных
    if not obj.data_type:
        print('При генерации будут перебираться все типы данных')
        # Добавить соответствующее действие, вызов функции
    elif obj.data_type not in d_type.type_name:
        print('Указан некорректный тип данных')
        # Добавить соответствующее действие, вызов функции
    else:
        print('OK')
        # Добавить соответствующее действие, вызов функции

    # Проверяем корректность выбранной синтаксической кострукции
    if not obj.syntax_type:
        print('При генерации будут перебираться все синтаксические кострукции')
        # Добавить соответствующее действие, вызов функции
    elif obj.syntax_type not in syn_type.construct_name:
        print('Указан некорректный тип синтаксической кострукции')
        # Добавить соответствующее действие, вызов функции
    else:
        print('OK')
        # Добавить соответствующее действие, вызов функции

    # Проверяем идентификатор для генерации
    if not obj.identifier:
        print('Идентификатор для подстановки не задан, генерируем из интервала a-z')
        obj.identifier = get_identifier()
        # Добавить проверку: свободен ли идетификатор
    else:
        print('OK')
        # Добавить проверку корректности идентификатора???

    # Проверяем значение
    if not obj.value:
        print('Значение не указано, генерируем случайным образом')
        obj.value = d_type.get_value(d_type) # Реализовать отд. функцией или методом класса???
    elif obj.value not in d_type.get_values_range(d_type):
        print('Некорректное значение!!!')
    else:
        print('ОК')
        # Проверяем попадет ли заданное значение в диапазон значений типа данных объекта


def generate(path='templates/'):
    '''
    Функция построчно читает шаблоны .txt, расположенный в path
    и осуществляет запись в tests/test_name.c'
    '''

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