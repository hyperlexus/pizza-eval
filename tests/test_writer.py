from pizza_eval import pizza_eval_write

def test_static_blocks():
    # Testing [author] and [message]
    result = pizza_eval_write("Alice", "Hello", "User [author] said [message]")
    assert result == "User Alice said Hello"

def test_random_block():
    # Testing [random] weighted choices
    # We test that the result is one of the expected options
    template = "[random\\optionA-1\\optionB-1]"
    result = pizza_eval_write("user", "msg", template)
    assert result in ["optionA", "optionB"]

def test_replace_logic():
    # Testing [replace\\target\\replacement]
    # Note: replace results in the original message with substitutions
    msg = "I like apples"
    template = "[replace\\apples\\bananas]"
    assert pizza_eval_write("user", msg, template) == "I like bananas"

def test_nested_replace():
    # Testing that replace blocks can handle random blocks inside them
    msg = "Go up"
    template = "[replace\\up\\[random\\down-1\\left-0]]"
    assert pizza_eval_write("user", msg, template) == "Go down"
