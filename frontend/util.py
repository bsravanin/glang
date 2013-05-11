#!/usr/bin/python2.7

'Utility module for the Gramola frontend.'

import os


BUILTINS_FILENAME = os.path.abspath('builtins.gr')
# NOTE: this must match the class declaration in builtins.gr
BUILTINS_CLASS_NAME = '__builtins'
CONSTRUCTOR_NAME = '__init__'
# Collection type to number of type parameters
COLLECTION_BASE_TYPES = {
    ((), 'list'): 1,
    ((), 'dict'): 2,
    ((), 'set'): 1,
    }
NULL = 'null'
