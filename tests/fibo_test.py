import pytest
from main.fibo import fibo


def test_fibo_start():
    assert fibo(0) == 1
    assert fibo(1) == 1


def test_fibo_2():
    assert fibo(2) == 2


def test_fibo_3():
    assert fibo(3) == 3


## parametrization
# @pytest = decorator (fnctn that extends initial fnctn w/o changing the code)
@pytest.mark.parametrize("n, F_n", [(4, 5), (5, 8), (6, 13)])
def test_fibo_n(n, F_n):
    assert fibo(n) == F_n


def test_fibo_negative():
    with pytest.raises(ValueError):
        fibo(-1)


def test_fibo_float():
    with pytest.raises(TypeError):
        fibo(3.14)


## kind of "marked" as slow and therefore not tested with pytest
## when pytest -m "not slow" fibo_test.py is being used
@pytest.mark.slow
def test_fibo_huge():
    assert fibo(35) == 14930352
