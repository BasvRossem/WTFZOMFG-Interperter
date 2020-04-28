"""A WTFZOMFG Lexer"""
from copy import copy
from enum import Enum

TOKENS = {
    # Control
    ':' : 'LABEL_GOTO',
    ';' : 'LABEL_DECLARE',
    '?' : 'LABEL_GOTO_NONZERO',
    '!' : 'LABEL_GOTO_ZERO',
    '(' : 'LOOP_START',
    ')' : 'LOOP_END',
    '{' : 'IF_START',
    '}' : 'IF_END',

    # Cell/Pointer Manipulation
    '+' : 'CELL_INCREASE',
    '-' : 'CELL_DECREASE',
    '|' : 'CELL_FLIP',
    '=' : 'CELL_SET',
    '~' : 'CELL_INCREASE_WITH',

    '&' : 'COPY_VALUE_RIGHT',
    '%' : 'COPY_VALUE_TO',

    '<' : 'POINTER_MOVE_LEFT',
    '>' : 'POINTER_MOVE_RIGHT',
    '_' : 'POINTER_MOVE_TO',
    '*' : 'POINTER_MOVE_RELATIVE',

    '@' : 'CELL_SUBTRACT_ASCII',

    # Arithmetic
    'a' : 'CELL_ADD_RIGHT',
    's' : 'CELL_SUBTRACT_RIGHT',
    'm' : 'CELL_MULTIPLY_RIGHT',
    'd' : 'CELL_DEVIDE_RIGHT',

    # Input/Output
    '^' : 'SCAN_ASCII',
    '/' : 'SCAN_DECIMAL',
    'v' : 'PRINT_CELL_ASCII',
    '\\' : 'PRINT_CELL_DECIMAL',
    '.' : 'PRINT_CHARACTER',
    '\'' : 'PRINT_UNTIL',
    '\"' : 'PRINT_STOP',

    # Commenting
    '#' : 'COMMENT',
    '[' : 'COMMENT_START',
    ']' : 'COMMENT_END',

    # Debug
    'w' : "PRINT_PROGRAM_STATE"
}

class Token():
    """A token class which consists of a command and a value if needed"""
    def __init__(self, command, value):
        self.command = command
        self.value = value

    def __str__(self):
        return "(" + str(self.command) + ", " + str(self.value) + ")"

    def __repr__(self):
        return self.__str__()

class LexerStates(Enum):
    """A class which represents all the possible states the lexer can be in"""
    DEFAULT = 0
    PRINT = 1
    PRINT_UNTIL = 2
    COMMENT = 3
    COMMENT_UNTIL = 4
    CELL_SUBTRACT_ASCII = 5
    POINTER_MOVE_RELATIVE = 6

def find_token(lexer_state, element):
    """
    A function which turns a character into a token
    Returns a list of tokens
    """
    if element == '\\':
        print("======================================================================================")
        #TODO: If a single backslah is found in the file without any character after it, it is skipped in the lexer  
    state = copy(lexer_state)
    if state == LexerStates.DEFAULT and element in TOKENS:
        if TOKENS[element] == 'PRINT_CHARACTER':
            state = LexerStates.PRINT
        if TOKENS[element] == 'PRINT_UNTIL':
            state = LexerStates.PRINT_UNTIL
        if TOKENS[element] == 'COMMENT' or TOKENS[element] == 'LABEL_DECLARE' or TOKENS[element] == 'LABEL_GOTO':
            state = LexerStates.COMMENT
        if TOKENS[element] == 'COMMENT_START':
            state = LexerStates.COMMENT_UNTIL
        if TOKENS[element] == 'CELL_SUBTRACT_ASCII':
            state = LexerStates.CELL_SUBTRACT_ASCII
        if TOKENS[element] == 'POINTER_MOVE_RELATIVE' or TOKENS[element] == 'SCAN_DECIMAL':
            state = LexerStates.POINTER_MOVE_RELATIVE
        return state, Token(TOKENS[element], None)
    if state == LexerStates.PRINT:
        state = LexerStates.DEFAULT
    if state == LexerStates.CELL_SUBTRACT_ASCII:
        state = LexerStates.DEFAULT
    if state == LexerStates.POINTER_MOVE_RELATIVE:
        state = LexerStates.DEFAULT
    if state == LexerStates.COMMENT:
        if element == '\n':
            state = LexerStates.DEFAULT
    if state in (LexerStates.PRINT_UNTIL, LexerStates.COMMENT_UNTIL):
        if element in TOKENS and (TOKENS[element] in ('PRINT_STOP', 'COMMENT_END')):
            state = LexerStates.DEFAULT
            return state, Token(TOKENS[element], None)
    return state, Token('VALUE', element)

def cleanup_tokens(token_list):
    """
    A function which cleans up tokens by combining where necessary
    Returns a list of tokens
    """
    # Stich strings together
    clean_tokens = []
    i = 0
    while i < len(token_list):
        if not token_list[i].value:
            clean_tokens.append(copy(token_list[i]))
            i += 1
        else:
            previous = clean_tokens[-1]
            stiched = ""
            while i < len(token_list) and token_list[i].value:
                stiched += token_list[i].value
                i += 1
            previous.value = stiched.replace("\n", "")

    # Remove comments
    new_clean_tokens = []
    i = 0
    while i < len(clean_tokens):
        if clean_tokens[i].command == 'COMMENT_START':
            i += 1
        elif clean_tokens[i].command == 'COMMENT':
            pass
        else:
            new_clean_tokens.append(clean_tokens[i])
        i += 1

    return new_clean_tokens

def make_tokens(source):
    """
    A function that converts a string of characters into tokens
    Returns a list of tokens
    """
    token_list = []
    lxr_state = LexerStates.DEFAULT
    for element in source:
        lxr_state, returned_token = find_token(lxr_state, element)
        token_list.append(returned_token)
    clean_tokens = cleanup_tokens(token_list)
    print("========================")
    for tok in clean_tokens:
        print(tok)
    print("========================")
    return clean_tokens
