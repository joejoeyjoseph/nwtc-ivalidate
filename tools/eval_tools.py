# tools for codebase

import importlib


# Load the module t class with the name s
def get_module_class(t, s):

    m = importlib.import_module('.'.join([t, s]))

    return getattr(m, s)


# Apply a series of transformative modules
def apply_trans(ts, modlist):

    for m in modlist:

        ts = m.apply(ts)

    return ts
