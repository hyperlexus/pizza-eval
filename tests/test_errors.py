import pytest
from pizza_eval import pizza_eval_read, PizzaError, pizza_eval_write


@pytest.mark.parametrize("code, condition, message", [
    (0, "", "xd"),  # nothing passed
    (1, "is 'unclosed", "xd"),  # odd number of single quotes
    (2, "'is xd'", "xd"),  # quote as first character
    (3, "it 'is'", "is"),  # no simple type check contained
    (5, "is 'is' xd", "xd"),
    (5, "is 'a & is' b", "b"),
    (5, "is a bomboclaat", "a bomboclaat"),
    (6, "is ''test", "test"),

    (100, "is 'a' &", "xd"),
    (101, "is 'a' & 'b'", "xd"),
    (101, "is a&isa", "b"),
    # (102, "is 'a & is' b", "b"),  102 can't technically be reached but why delete it, just in case
    (103, "is a & is ", "a"),
    # (104) can also not be reached but you never know
    (105, "is 'a & is 'b", "b"),

    # 200 errors can't be tested as they shouldn't happen and signal an internal error

    (-1, "is '('", "("),  # tests that parentheses in quotes are ignored, would raise 301 otherwise
    (301, "in 4 & (in 6", "6"),
    (302, "in 4 & in 6)", "6"),
    (303, "in 4()", "4"),
])
def test_pizza_read_dynamic(code, condition, message):
    if code == -1:
        result = pizza_eval_read(condition, message)
        assert result or not result
        return
    with pytest.raises(PizzaError) as excinfo:
        pizza_eval_read(condition, message)
    assert excinfo.value.code == code

@pytest.mark.parametrize("code, write_result, message", [
    # note that if the expression doesn't contain any [ quotes then nothing is checked as nothing has to be done.
    # (1000) shouldn't happen
    (1001, "blud", "bomboclaat '[]blud"),  # unclosed single quote
    (1002, "blud", "b["),
    (1003, "", "blud")
])
def test_pizza_write_dynamic(code, message, write_result):
    if code == -1:
        result = pizza_eval_write("test_author", message, write_result)
        assert result or not result
        return
    with pytest.raises(PizzaError) as excinfo:
        pizza_eval_write("test_author", write_result, message)
    assert excinfo.value.code == code
