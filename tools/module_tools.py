# get module class

import importlib


# Load the module t class with the name s
def get_module_class(t, s):

    m = importlib.import_module('.'.join([t, s]))

    return getattr(m, s)
