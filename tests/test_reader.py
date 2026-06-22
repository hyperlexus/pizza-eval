import pytest
from pizza_eval import pizza_eval_read

# basic conditions
@pytest.mark.parametrize("condition, msg, expected", [
    ("is 'hello'", "hello", True),
    ("is 'hello'", "world", False),
    ("in 'cat'", "the cat sat", True),
    ("start 'pre'", "prefix", True),
    ("end 'fix'", "prefix", True),
])
def test_basic_comparisons(condition, msg, expected):
    assert pizza_eval_read(condition, msg) is expected


# isolated
@pytest.mark.parametrize("condition, msg, expected", [
    ("isolated allah", "allah uakbar", True),
    ("isolated allah", "allahu akbar", False),
    ("isolated allah", "allah ", True),
    ("isolated allah", "ibrahim allah", True),
    ("isolated allah", "wallah", False),
    ("isolated allah", "allah", True)
])
def test_isolated(condition, msg, expected):
    assert pizza_eval_read(condition, msg) == expected


# & | ^
@pytest.mark.parametrize("condition, msg, expected", [
    ("in 'pepperoni' & in 'pizza'", "pepperoni pizza", True),
    ("in 'pepperoni' & in 'pineapple'", "pepperoni pizza", False),
    ("in 'pepperoni' | in 'pineapple'", "pepperoni pizza", True),
    ("in 'pepperoni' ^ in 'pizza'", "pepperoni pizza", False),
])
def test_logical_operators(condition, msg, expected):
    assert pizza_eval_read(condition, msg) is expected


# not
@pytest.mark.parametrize("condition, msg, expected", [
    ("not is 'apple'", "banana", True),
    ("not in 'apple'", "pineapple", False),
])
def test_negation(condition, msg, expected):
    assert pizza_eval_read(condition, msg) is expected
