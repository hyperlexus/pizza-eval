import pytest
from pizza_eval import pizza_eval_read, PizzaError

def dynamic_test(code, condition, message):
    with pytest.raises(PizzaError) as excinfo:
        pizza_eval_read(condition, message)
    assert excinfo.value.code == code

def test_0():
    dynamic_test(0, "", "xd")

def test_1():
    dynamic_test(1, "is 'unclosed", "xd")

def test_2():
    dynamic_test(2, )
