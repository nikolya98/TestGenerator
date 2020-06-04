import random


##### Классы типов данных #####
class RucInt:
    '''
    Модель целочисленного типа int
    '''

    type_name = ['INT', 'int', 'ЦЕЛ', 'цел']
    __min_val, __max_val = (-2 ** 31, 2 ** 31 - 1)
    __values = range(__min_val, __max_val)
    __poss_operations = []

    def get_values_range():
        return RucInt.__values

    def get_value():
        value = random.choice(RucInt.__values)
        return value


class RucLong():
    '''
    Модель диненого целочисленного типа long
    '''

    type_name = ['LONG', 'long', 'ДЛИН', 'длин']
    __min_val, __max_val = (-2 ** 63, 2 ** 63 - 1)
    __values = range(__min_val, __max_val)
    __poss_operations = []

    def get_values_range():
        return RucLong.__values

    def get_value():
        value = random.choice(RucLong.__values)
        return value


# class RucFloat:
#     '''
#     Модель вещественного типа float
#     '''
#
#     type_name = ['FLOAT', 'float', 'ВЕЩ', 'вещ']
#     __min_val, __max_val = (None, None)
#     __values = range(__min_val, __max_val)
#     __poss_operations = []
#
#     def get_value(self):
#         value = random.choice(RucInt.__values)
#         return value

class RucChar:
    '''
    Модель символьного типа данных char
    '''

    type_name = ['CHAR', 'char', 'ЛИТЕРА', 'литера']
    __min_val, __max_val = (0, 255)
    __values = range(__min_val, __max_val)
    __poss_operations = []

    def get_values_range():
        return list(map(chr, RucChar.__values))

    def get_value():
        value = random.choice(RucChar.__values)
        return chr(value)


##### Классы синтаксических кострукций #####
class Var:
    construct_name = ['var', 'VAR']


##### Классы операций #####


##### Клас сбъекта #####
class Object(RucInt, Var):

    def __init__(self, data_type=None, syntax_type=None, identifier=None, value=None):
        self.data_type = data_type
        self.syntax_type = syntax_type
        self.identifier = identifier
        self.value = value

    # Методы??
