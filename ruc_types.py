import random

# Сделать Суперкласс для типов данных...?!

# class Type:
#     type_name = None
#     __min_val, __max_val = (None, None)
#     __values = ()
#     __poss_operations = []
#
#     def get_value():
#         value = random.choice(Type.__values)
#         return value


class RucInt:

    type_name = ['INT', 'int', 'ЦЕЛ', 'цел']
    __min_val, __max_val = (-2 ** 31, 2 ** 31 - 1)
    __values = range(__min_val, __max_val)
    __poss_operations = []

    def get_values_range(self):
        return self.__values

    def get_value(self):
        value = random.choice(RucInt.__values)
        return value



# Ркализовать оставшиеся типы данных

# class RucFloat:
#     type_name = ['FLOAT', 'float', 'ВЕЩ', 'вещ']
#     __min_val, __max_val = (-2 ** 31, 2 ** 31 - 1)
#     __values = range(__min_val, __max_val)
#     __poss_operations = []
#
#     def get_value():
#         value = random.choice(RucInt.__values)
#         return value
