import random
from datetime import datetime

from .utils import is_valid_replace_statement, command_contains_logic
from .errors import PizzaError

def command_to_blocks(write_command):
    if not write_command:
        raise PizzaError(1003, write_command)
    in_quotes = False
    blocks = []
    current_block = ""
    parentheses_level = 0
    for idx, char in enumerate(write_command):
        if char == "'":
            in_quotes = not in_quotes
            current_block += char
        elif not in_quotes:
            if char == "[":
                if parentheses_level == 0:
                    if current_block:
                        blocks.append(current_block)
                    current_block = "["
                else:
                    current_block += "["
                parentheses_level += 1
            elif char == "]":
                current_block += "]"
                if parentheses_level == 1:
                    if current_block:
                        blocks.append(current_block)
                    current_block = ""
                parentheses_level -= 1
            else:
                current_block += char
        elif in_quotes:
            current_block += char
    if current_block:
        blocks.append(current_block)
    if in_quotes:
        raise PizzaError(1001, write_command)
    if parentheses_level != 0:
        raise PizzaError(1002, write_command)
    return blocks

def separate_random_blocks(random_block: str) -> list[tuple]:
    random_block += "\\"
    in_quotes = False
    current_string = ""
    looking_for_event = True
    options = []
    current_event = ""
    parentheses_level = 0
    for char in random_block:
        if char == "'":
            in_quotes = not in_quotes
        elif in_quotes:
            current_string += char
        elif not in_quotes:
            if char == "[":
                parentheses_level += 1
                current_string += "["
            elif char == "]":
                if parentheses_level > 0:
                    parentheses_level -= 1
                    current_string += "]"
                else:
                    raise PizzaError(1108, random_block)
            elif char == "-":
                if parentheses_level == 0:
                    if not looking_for_event:
                        raise PizzaError(1110, random_block)
                    looking_for_event = False
                    current_event = current_string
                    current_string = ""
                else:
                    current_string += char
            elif char == "\\":
                if parentheses_level == 0:
                    if looking_for_event:
                        raise PizzaError(1111, random_block)
                    try:
                        weight = int(current_string)
                    except ValueError:
                        raise PizzaError(1103, current_string)
                    options.append((current_event, weight))
                    current_event = ""
                    current_string = ""
                    looking_for_event = True
                else:
                    current_string += char
            else:
                current_string += char

    if parentheses_level > 0:
        raise PizzaError(1109, random_block)
    return options

def separate_replace_blocks(replace_block: str) -> list:
    """
    returns a list of length 2 that contains the replace statement separated into its top level components.
    :returns: list[to_be_replaced, to_replace_with]
    """
    in_quotes: bool = False
    parentheses_level: int = 0
    segments: list = []
    current_statement: str = ""
    for char in replace_block:
        if char == "'":
            in_quotes = not in_quotes
        elif in_quotes:
            current_statement += char
        elif not in_quotes:
            if char == "[":
                parentheses_level += 1
                current_statement += "["
            elif char == "]":
                if parentheses_level > 0:
                    parentheses_level -= 1
                    current_statement += "]"
            elif char == "\\":
                if parentheses_level == 0:
                    segments.append(current_statement)
                    current_statement = ""
                else:
                    current_statement += "\\"
            else:
                current_statement += char
    if current_statement:
        segments.append(current_statement)
    return segments

class PizzaWriter:
    def __init__(self, author_name: str, original_message: str):
        self.author_name = author_name
        self.original_message = original_message

    def process_general_block(self, block: str) -> str:
        if not command_contains_logic(block):
            return block
        if block == "[author]":
            return str(self.author_name)
        elif block == "[time]":
            return datetime.now().strftime('%H:%M:%S')  # todo in future version: [time+3h], [time-5d3m]
        elif block == "[message]":
            return self.original_message
        elif block.startswith("[random\\"):
            return self.process_random_block(block)
        elif block.startswith("[replace\\"):
            return self.process_replace_blocks(block)
        else:
            return f"{block}"  # dont change irrelevant blocks

    def process_random_block(self, random_block):
        random_block = random_block[1:-1]
        random_block = random_block[7:]
        options = separate_random_blocks(random_block)
        weighted_options = {}
        for option in options:
            try:
                event, weight = option[0], option[1]
                try:
                    weight = int(weight)
                except ValueError:
                    raise PizzaError(1103, random_block)
            except ValueError:
                raise PizzaError(1102, random_block)
            if event.startswith("[") and event.endswith("]"):
                event = self.process_general_block(event)

            weighted_options[event] = weight
        return random.choices(list(weighted_options.keys()), list(weighted_options.values()), k=1)[0]

    def process_replace_blocks(self, replace_block):
        is_valid_replace_statement(replace_block)
        replace_block = replace_block[1:-1]
        replace_block = replace_block[8:]
        to_replace, to_replace_with = separate_replace_blocks(replace_block)  # returns fixed length array
        to_replace = self.process_general_block(to_replace)
        to_replace_with = self.process_general_block(to_replace_with)
        return self.original_message.replace(to_replace, to_replace_with)

    def write(self, write_result: str) -> str:
        command_blocks = command_to_blocks(write_result)  # höhö minecraft
        if len(command_blocks) == 1:
            return self.process_general_block(command_blocks[0])
        else:
            output = ""
            for command_block in command_blocks:
                output += self.process_general_block(command_block)
            return output
