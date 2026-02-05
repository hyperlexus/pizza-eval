from pizza_eval import pizza_eval_read

def test_basic_comparisons():
    # is, in, start, end
    assert pizza_eval_read("is 'hello'", "hello") is True
    assert pizza_eval_read("is 'hello'", "world") is False
    assert pizza_eval_read("in 'cat'", "the cat sat") is True
    assert pizza_eval_read("start 'pre'", "prefix") is True
    assert pizza_eval_read("end 'fix'", "prefix") is True

def test_logical_operators():
    # & | ^
    msg = "pepperoni pizza"
    assert pizza_eval_read("in 'pepperoni' & in 'pizza'", msg) is True
    assert pizza_eval_read("in 'pepperoni' & in 'pineapple'", msg) is False
    assert pizza_eval_read("in 'pepperoni' | in 'pineapple'", msg) is True
    assert pizza_eval_read("in 'pepperoni' ^ in 'pizza'", msg) is False  # xor

def test_negation():
    # not
    assert pizza_eval_read("not is 'apple'", "banana") is True
    assert pizza_eval_read("not in 'apple'", "pineapple") is False
