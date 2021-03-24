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


def append_results(results, base, c, conf):

    results.append({'truth name': base['name'],
                    'model name': c['name'],
                    'path': c['path'],
                    'location': conf['location'],
                    'var': c['var']}
                   )

    return results
