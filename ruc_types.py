import random


class RucInt:

    type_name = ['INT', 'int', 'ЦЕЛ', 'цел']
    __min_val, __max_val = (-2 ** 31, 2 ** 31 - 1)
    __values = range(__min_val, __max_val)
    __poss_operations = []

    def get_value():
        value = random.choice(RucInt.__values)
        return value


print(RucInt.get_value())

