# run unit tests

import importlib
import pandas as pd
import math


test_dir = 'metrics'

x_eg = pd.Series([2, 2, 2, 2, 16])
y_eg = pd.Series([4, 5, 6, -7, 8])


def load_obj(metric):

    metric_module = importlib.import_module('.'.join([test_dir, metric]))

    metric_obj = getattr(metric_module, metric)()

    return metric_obj


def test_bias():

    metric_obj = load_obj('bias')

    assert metric_obj.compute(5, 4) == -1


def test_series_bias():

    metric_obj = load_obj('bias')

    assert metric_obj.compute(x_eg, y_eg) == -1.6


def test_bias_pct():

    metric_obj = load_obj('bias_pct')

    assert metric_obj.compute(5, 4) == -20


def test_series_bias_pct():

    metric_obj = load_obj('bias_pct')

    assert metric_obj.compute(x_eg, y_eg) == -10


def test_mae():

    metric_obj = load_obj('mae')

    assert metric_obj.compute(5, 4) == 1


def test_series_mae():

    metric_obj = load_obj('mae')

    assert metric_obj.compute(x_eg, y_eg) == 5.2


def test_mae_pct():

    metric_obj = load_obj('mae_pct')

    assert metric_obj.compute(5, 4) == 20


def test_series_mae_pct():

    metric_obj = load_obj('mae_pct')

    assert metric_obj.compute(x_eg, y_eg) == 190


def test_series_rmse():

    metric_obj = load_obj('rmse')

    result = metric_obj.compute(x_eg, y_eg)

    assert math.isclose(result, 5.899, rel_tol=1e-4)


def test_series_crmse():

    metric_obj = load_obj('crmse')

    result = metric_obj.compute(x_eg, y_eg)

    assert math.isclose(result, 5.678, rel_tol=1e-4)
