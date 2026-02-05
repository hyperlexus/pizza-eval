from .errors import PizzaError


def logical_xor(a, b):
    return (a or b) and not (a and b)


# condition validator 3000
def remove_text_inside_gaensefuesschen(expression):  # for contains_a_check
    out = ""
    inside_gaensefuesschen = False
    for char in expression:
        if char == "'":
            out += char
            inside_gaensefuesschen = not inside_gaensefuesschen
            continue
        if not inside_gaensefuesschen:
            out += char
    return out


def is_parenthese_lvl_fine(condition):
    insideGaensefuesschen = False
    parantheseLvl = 0
    for char in condition:
        if char == "'":
            insideGaensefuesschen = not insideGaensefuesschen
        if insideGaensefuesschen:
            continue
        if char == "(":
            parantheseLvl += 1
        elif char == ")":
            parantheseLvl -= 1
    return parantheseLvl


def two_gaensefuesschen_in_a_row(condition):
    last_char_gaensefuesschen = False
    for char in condition:
        if char == "'":
            if not last_char_gaensefuesschen:
                last_char_gaensefuesschen = True
            else:
                return True
        else:
            last_char_gaensefuesschen = False
    return False


def bracket_open_close_in_a_row(condition):
    insideGaensefuesschen = False
    last_paranthese_open = False
    for char in condition:
        if char == "'":
            insideGaensefuesschen = not insideGaensefuesschen
        if insideGaensefuesschen:
            continue
        if char == "(":
            last_paranthese_open = True
        if char == ")" and last_paranthese_open:
            return True
        if not char == "(":
            last_paranthese_open = False


def is_valid_single_expression(single_expression: str) -> None:
    if all(check not in remove_text_inside_gaensefuesschen(single_expression) for check in ['is ', 'in ', 'start ', 'end ']):
        raise PizzaError(101, single_expression)
    if single_expression.count("'") % 2:
        raise PizzaError(102, single_expression)
    if any(check == single_expression for check in ['is', 'in', 'start', 'end', 'is ', 'in ', 'start ', 'end ']):
        raise PizzaError(103, single_expression)


def is_valid_condition(condition: str) -> None:
    if not condition:
        raise PizzaError(0, condition)
    if condition.count("'") % 2:
        raise PizzaError(1, condition)
    if condition[0] == "'":
        raise PizzaError(2, condition)
    if all(check not in condition for check in ['is ', 'in ', 'start ', 'end ']):
        raise PizzaError(3, condition)
    parentheses_lvl_fine = is_parenthese_lvl_fine(condition)
    if parentheses_lvl_fine > 0:
        raise PizzaError(301, condition)
    if parentheses_lvl_fine < 0:
        raise PizzaError(302, condition)
    if bracket_open_close_in_a_row(condition):
        raise PizzaError(303, condition)
    if two_gaensefuesschen_in_a_row(condition):
        raise PizzaError(6, condition)
    return True

def is_valid_replace_statement(replace_statement: str):
    if not replace_statement.startswith("[replace\\") or not replace_statement.endswith("]"):
        raise PizzaError(1201, replace_statement)

    if replace_statement.count("'") % 2:
        raise PizzaError(1204, replace_statement)

    inquotes = False
    openbracketcount, closebracketcount = 0, 0
    bracket_level = 0
    backslashcount = 0
    checked_valid_stringb_block = False  # (for performance)
    for i in replace_statement:
        if i == "'":
            inquotes = not inquotes
        elif not inquotes:
            if i == "\\" and bracket_level == 1:
                backslashcount += 1
            if i == "[":
                openbracketcount += 1
                bracket_level += 1
            elif i == "]":
                closebracketcount += 1
                bracket_level -= 1
            if backslashcount == 2 and not checked_valid_stringb_block:  # valid block but not random
                stringb_to_check = replace_statement.split("\\")[2]
                if stringb_to_check.startswith("[") and not stringb_to_check.startswith("[random"):
                    raise PizzaError(1208, replace_statement)
                checked_valid_stringb_block = True

    if backslashcount != 2:
        raise PizzaError(1205, replace_statement)

    if openbracketcount != closebracketcount or bracket_level != 0:
        raise PizzaError(1202, replace_statement)

    return True
