from pizza_eval import pizza_eval_write

def test_static_blocks():
    # Testing [author] and [message]
    result = pizza_eval_write("Alice", "Hello", "User [author] said [message]")
    assert result == "User Alice said Hello"

def test_random_block():
    # [random]
    template = "[random\\optionA-1\\optionB-1]"
    result = pizza_eval_write("user", "msg", template)
    assert result in ["optionA", "optionB"]

    # [random\[random\n-p\m-q]-r\o-s]
    template_2 = "[random\\optionA-1\\[random\\optionB-1\\optionC-1]-1]"
    a = [pizza_eval_write("user", "msg", template_2) for i in range(25)]
    assert {"optionA", "optionB", "optionC"} <= set(a)

def test_replace_logic():
    # testing replace
    msg = "die banane"
    template = "[replace\\die\\der]"
    assert pizza_eval_write("user", msg, template) == "der banane"

def test_nested_replace():
    # nested replace[random]
    msg = "go up"
    template = "[replace\\up\\[random\\down-1\\left-0]]"
    assert pizza_eval_write("user", msg, template) == "go down"

def test_nested_random_replace():
    msg = "go up"
    template = "[random\\[replace\\up\\down]-1\\[replace\\up\\left]-1]"
    assert pizza_eval_write("user", msg, template) in ["go down", "go left"]