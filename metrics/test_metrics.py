# run unit tests

import importlib
import pandas as pd

test_dir = 'metrics'

def test_bias(): 

    metric = 'bias'

    metric_module = importlib.import_module(".".join([test_dir, metric]))

    metric_obj = getattr(metric_module, metric)()

    assert metric_obj.compute(5, 4) == -1

def test_series_bias(): 

    metric = 'bias'

    metric_module = importlib.import_module(".".join([test_dir, metric]))

    metric_obj = getattr(metric_module, metric)()

    # assert metric_obj.compute(5, 4) == -1

    x = pd.Series([0, 0, 0])
    y = pd.Series([1, 2, 3])

    assert metric_obj.compute(x, y) == 2