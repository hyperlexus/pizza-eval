
# error handling
class PizzaError(Exception):
    def __init__(self, code: int, expression: str):
        self.code = code
        self.expression = expression  # the expression that it failed on that will be returned to the user
        self.message = error_dict.get(code, f"unhandled error with code {code}")
        super().__init__(self.message)

    def __str__(self):
        return f"Error code {self.code}: {self.message}\nprocessing this expression: `{self.expression}`"

error_dict = {
    # read eval errors:
    # general errors
    0: "nothing was passed.",
    1: "odd number of single quotes. make sure to close all quotes!",
    2: "condition had `'` as its first character, which is not allowed. did you quote the entire string instead of the expression value?",
    3: "no valid simple type check contained in the expression. simple type checks are in, is, start, end",
    4: "amount of opening and closing parentheses do not match. did you close all opened parentheses?",  # unreachable, is never raised
    5: "the condition has too many spaces. please set the expression into single quotes `'<expression>'` if it contains spaces.",
    6: "your condition contains two single quotes `''` in a row. please don't do that 🍕👌",

    # simple expression handler errors
    100: "simple expression is empty",
    101: "simple expression doesn't contain necessary simple type check.",
    102: "simple expression has an incorrect amount of single quotes.",
    103: "simple expression contains only a type check, but no value. Did you pass both type and value ('is a')?",
    104: "simple expression could not evaluate, as type check is not known.",
    105: "simple expression contains characters after the last closing quote, which is not allowed (as it confuses the compiler)",

    # blocks errors
    201: "blocks were not correctly divided. there are an even number of blocks, which shouldn't happen.",
    202: "blocks were divided, but no valid operator was found.",

    # parentheses-related errors
    301: "input contains more opening parentheses than closing parentheses.",
    302: "input contains more closing parentheses than opening parentheses.",
    303: "input contains at least 1 empty pair of parentheses `()`, which is not allowed.",

    # write eval errors:
    # general errors:
    1000: "invalid write format, uncaught exception.",
    1001: "unmatched single quote in entire result.",
    1002: "entire statement has mismatched [ and ].",
    1003: "no write statement was passed. pizza cannot reply with nothing!",

    # random errors:
    1101: "invalid [random\\eventa-n\\eventb-m] format.",
    1102: "invalid eventn-p format.",
    1103: "probability has to be an integer indicating weight.",
    1104: "random statements cannot be chained together as that doesn't make sense mathematically (refer to [this](https://i.imgur.com/LvT3YcW.png)).",  # this is now possible!
    1105: "random event cannot contain a [ that isn't at the start (expression must be entire statement)",
    1106: "random event has mismatched [ and ].",
    1107: "random event cannot be an empty statement `[]`.",
    1108: "random event has too many closing ], causing it to try and close a bracket that was never opened.",
    1109: "random event has too many opening [, causing it to never close an opened bracket.",
    1110: "random event contains two event and probability separators, which is incorrect formatting: `...event-probability-probability`. please separate with backlashes!",
    1111: "random event does not contain a probability assignment.",

    # replace errors:
    1200: "replace statement not valid for uncaught reason.",
    1201: "replace statement doesn't both start with [replace and end with ].",
    1202: "replace statement has mismatched [ and ].",
    1204: "unmatched single quote in replace statement.",
    1205: "replace statement doesn't contain exactly 2 splitter backslashes outside of blocks.",
    1206: "invalid [replace\\stringa\\stringb] format. length of segments is not two.",
    1207: "replace statements cannot be chained together inside of each other as that doesn't make sense",
    1208: "statement to replace with starts with a [, but isn't a random block, which is not allowed. use single quotes (\') for this if you want to print a [ character."
}
