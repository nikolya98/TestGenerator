import random
from ruc_types import RucInt
from syntax_types import Var
from funcs import *


class Object(RucInt, Var):

    def __init__(self, data_type=None, syntax_type=None, identifier=None, value=None):
        self.data_type = data_type
        self.syntax_type = syntax_type
        self.identifier = identifier
        self.value = value
