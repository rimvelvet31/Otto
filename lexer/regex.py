import re


def match_int(number):
    int_regex = re.compile(r"^[0-9]+$")
    return re.match(int_regex, number)


def match_float(number):
    float_regex = re.compile(r'^[0-9]+\.[0-9]+$')
    return re.match(float_regex, number)


# IDENTIFIER RULES
# - Identifiers are case sensitive
# - They cannot contain whitespace
# - They cannot contain special chars, expect underscore (_)
# - They can contain numbers, but are not allowed to start with one
# - They must start with an uppercase or lowercase letter, or with underscore
IDENTIFIER_REGEX = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
