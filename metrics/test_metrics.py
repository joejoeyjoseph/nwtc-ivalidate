# run unit tests

from bias import bias

print('hi')

bias.compute(5, 4)

def test_compute(): 

    assert bias.compute(5, 4) == 0