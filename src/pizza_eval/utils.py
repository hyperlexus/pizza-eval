import re
from .errors import PizzaError

valid_checks = ['is ', 'in ', 'start ', 'end ', 'isolated ']

def logical_xor(a, b):
    return (a or b) and not (a and b)


# condition validator 3000
def remove_text_inside_quotes(expression):  # for contains_a_check
    out = ""
    inside_quotes = False
    for char in expression:
        if char == "'":
            out += char
            inside_quotes = not inside_quotes
            continue
        if not inside_quotes:
            out += char
    return out

def check_trailing_garbage(expression: str) -> None:  # works for single expressions
    last_quote_idx = expression.rfind("'")
    if last_quote_idx != -1:
        trailing_stuff = expression[last_quote_idx + 1:].strip()
        if trailing_stuff:
            raise PizzaError(105, expression)

def is_parentheses_level_fine(condition: str):
    inside_quotes = False
    parentheses_level = 0
    for char in condition:
        if char == "'":
            inside_quotes = not inside_quotes
        if inside_quotes:
            continue
        if char == "(":
            parentheses_level += 1
        elif char == ")":
            parentheses_level -= 1
    return parentheses_level

def two_quotes_in_a_row(condition: str):
    return "''" in condition

def bracket_open_close_in_a_row(condition):
    clean_condition = re.sub(r"'.*?'", "", condition)
    return "()" in clean_condition

def is_valid_single_expression(single_expression: str) -> None:
    valid_checks_stripped = [check.strip() for check in valid_checks]
    if single_expression == "":
        raise PizzaError(100, single_expression)
    if all(check not in remove_text_inside_quotes(single_expression) for check in valid_checks):
        raise PizzaError(101, single_expression)
    if single_expression.count("'") % 2:
        raise PizzaError(102, single_expression)
    if any(check == single_expression for check in (valid_checks + valid_checks_stripped)):
        raise PizzaError(103, single_expression)
    if any(check == single_expression for check in valid_checks):
        pass

def isolated_check(cond: str, message: str) -> bool:
    return message.startswith(f"{cond} ") or message.endswith(f" {cond}") or message.__contains__(f" {cond} ") or message.__eq__(f"{cond}")

def is_valid_condition(condition: str) -> None:
    if not condition:
        raise PizzaError(0, condition)
    if condition.count("'") % 2:
        raise PizzaError(1, condition)
    if condition[0] == "'":
        raise PizzaError(2, condition)
    if all(check not in condition for check in valid_checks):
        raise PizzaError(3, condition)
    parentheses_lvl_fine = is_parentheses_level_fine(condition)
    if parentheses_lvl_fine > 0:
        raise PizzaError(301, condition)
    if parentheses_lvl_fine < 0:
        raise PizzaError(302, condition)
    if bracket_open_close_in_a_row(condition):
        raise PizzaError(303, condition)
    if two_quotes_in_a_row(condition):
        raise PizzaError(6, condition)
    return None


# writer
def is_valid_replace_statement(replace_statement: str):
    if not replace_statement.startswith("[replace\\") or not replace_statement.endswith("]"):
        raise PizzaError(1201, replace_statement)

    if replace_statement.count("'") % 2:
        raise PizzaError(1204, replace_statement)

    in_quotes = False
    open_bracket_count, close_bracket_count = 0, 0
    bracket_level = 0
    backslash_count = 0
    checked_valid_stringb_block = False  # (for performance)
    for i in replace_statement:
        if i == "'":
            in_quotes = not in_quotes
        elif not in_quotes:
            if i == "\\" and bracket_level == 1:
                backslash_count += 1
            if i == "[":
                open_bracket_count += 1
                bracket_level += 1
            elif i == "]":
                close_bracket_count += 1
                bracket_level -= 1
            # if backslash_count == 2 and not checked_valid_stringb_block:  # valid block but not random
            #     stringb_to_check = replace_statement.split("\\")[2]
            #     if stringb_to_check.startswith("[") and not stringb_to_check.startswith("[random"):
            #         raise PizzaError(1208, replace_statement)
            #     checked_valid_stringb_block = True

    if open_bracket_count != close_bracket_count or bracket_level != 0:
        raise PizzaError(1202, replace_statement)
    if backslash_count != 2:
        raise PizzaError(1205, replace_statement)
    return True

def command_contains_logic(command: str) -> bool:
    in_quotes = False
    for char in command:
        if char == "'":
            in_quotes = not in_quotes
        if not in_quotes and char in ("[", "]"):
            return True
    return False
