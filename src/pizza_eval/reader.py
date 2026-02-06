from .errors import PizzaError
from .utils import is_valid_condition, logical_xor, is_valid_single_expression


def condition_to_blocks(condition):
    sub_blocks = []
    parenthesesLvl = 0  # paranthese.
    isInsideQuotes = False
    lastBlockStartIdx = 0
    for searchedOperator in ["|", "^", "&"]:
        for i in range(len(condition)):
            current_character = condition[i]
            if current_character == "'":
                isInsideQuotes = not isInsideQuotes
            elif not isInsideQuotes:
                if current_character == "(":
                    parenthesesLvl += 1
                elif current_character == ")":
                    parenthesesLvl -= 1
                elif current_character == searchedOperator and parenthesesLvl == 0:
                    blankBefore = i > 0 and condition[i-1] == " "
                    blankAfter = i < len(condition) - 1 and condition[i+1] == " "
                    if i - lastBlockStartIdx > 0:
                        sub_blocks.append(condition[lastBlockStartIdx:i - (1 if blankBefore else 0)])
                    sub_blocks.append(current_character)
                    sub_blocks.append(condition[i + (2 if blankAfter else 1):])
                    return sub_blocks
    if len(sub_blocks) == 0:
        if condition.startswith("(") and condition.endswith(")"):
            return condition_to_blocks(condition[1:-1])
        sub_blocks.append(condition)
    return sub_blocks


def remove_quotes(string):
    string.strip()
    if string.count("'") >= 2:
        last_quote = string.rfind("'")
        a = string[last_quote + 1:].strip()
        if last_quote < len(string) - 1 and string[last_quote + 1:] and not string[last_quote + 1] == " ":
            raise PizzaError(105, string)
    if string.startswith("'") and string.endswith("'"):
        return string[1:-1]
    elif " " in string:
        raise PizzaError(5, string)
    return string

def recursively_check_entire_condition(condition: str) -> None:
    blocks = condition_to_blocks(condition)
    if len(blocks) == 1:
        is_valid_single_expression(blocks[0])
    else:
        recursively_check_entire_condition(blocks[0])
        recursively_check_entire_condition(blocks[2])

def eval_single_expression(expression: str, message: str):
    is_valid_single_expression(expression)
    isNot = False
    if expression.startswith("not "):
        isNot = True
        expression = expression[4:]
    if expression.startswith("is"):
        cond = expression.partition("is ")[2]
        operationResult = remove_quotes(cond) == message
    elif expression.startswith("in"):
        cond = expression.partition("in ")[2]
        operationResult = remove_quotes(cond) in message
    elif expression.startswith("start "):
        cond = expression.partition("start ")[2]
        operationResult = message.startswith(remove_quotes(cond))
    elif expression.startswith("end "):
        cond = expression.partition("end ")[2]
        operationResult = message.endswith(remove_quotes(cond))
    else:
        raise PizzaError(104, expression)
    return operationResult if not isNot else not operationResult


def pizza_eval_read(condition: str, message: str):
    if not condition:
        raise PizzaError(0, condition)

    condition = condition.lower()
    message = message.lower()

    is_valid_condition(condition)
    recursively_check_entire_condition(condition)

    blocks = condition_to_blocks(condition)
    if not len(blocks) % 2:
        raise PizzaError(201, condition)
    else:
        if len(blocks) == 1:
            return eval_single_expression(blocks[0], message)
        if "|" in blocks:
            return pizza_eval_read(blocks[0], message) or pizza_eval_read(blocks[2], message)
        elif "&" in blocks:
            return pizza_eval_read(blocks[0], message) and pizza_eval_read(blocks[2], message)
        elif "^" in blocks:
            return logical_xor(pizza_eval_read(blocks[0], message), pizza_eval_read(blocks[2], message))
        else:
            raise PizzaError(202, condition)
