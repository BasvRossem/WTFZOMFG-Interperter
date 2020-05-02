"""A WTFZOMFG Lexer"""
from copy import copy
from re import findall
from typing import List, Tuple

from wtf_objects import LexerStates, LexerVars, Token

TOKENS_COMMAND = {
    # Control
    '(' : 'LOOP_START',
    ')' : 'LOOP_END',
    '{' : 'IF_START',
    '}' : 'IF_END',

    # Cell/Pointer Manipulation
    '+' : 'CELL_INCREASE',
    '-' : 'CELL_DECREASE',
    '|' : 'CELL_FLIP',

    '&' : 'COPY_VALUE_RIGHT',

    '<' : 'POINTER_MOVE_LEFT',
    '>' : 'POINTER_MOVE_RIGHT',

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

    # Debug
    'w' : "PRINT_PROGRAM_STATE"}

TOKENS_COMMAND_VALUE = {
    # Control
    ':' : 'LABEL_GOTO',
    ';' : 'LABEL_DECLARE',
    '?' : 'LABEL_GOTO_NONZERO',
    '!' : 'LABEL_GOTO_ZERO',

    # Cell/Pointer Manipulation
    '=' : 'CELL_SET',
    '~' : 'CELL_INCREASE_WITH',

    '%' : 'COPY_VALUE_TO',

    '_' : 'POINTER_MOVE_TO',
    '*' : 'POINTER_MOVE_RELATIVE',

    '@' : 'CELL_SUBTRACT_ASCII',

    # Input/Output
    '.' : 'PRINT_CHARACTER',

    '\'' : 'PRINT_UNTIL',
    '\"' : 'PRINT_STOP',

    # Commenting
    '#' : 'COMMENT',
    '[' : 'COMMENT_START',
    ']' : 'COMMENT_END'}

LEXER_COMMANDS = [
    'ADD_TO_PREVIOUS']

def switch_lexer_state(lexer_state: LexerStates, command: str) -> LexerStates:
    """
    This function returns a state depending on the command
    """
    state = copy(lexer_state)
    if command == 'COMMENT':
        state = LexerStates.GO_UNTIL_NEWLINE
    elif command == 'PRINT_UNTIL':
        state = LexerStates.GO_UNTIL_END_PRINT
    elif command == 'COMMENT_START':
        state = LexerStates.GO_UNTIL_END_COMMENT
    return state

def find_token(lexer_state: LexerStates, element: str) -> Tuple[LexerStates, Token]:
    """
    A fucntion that creates a token using an element
    """
    state = copy(lexer_state)
    token = Token(None, None)

    # The lexer will try to make a new token
    if state == LexerStates.DEFAULT:
        # The element is a valid single character command
        if element in TOKENS_COMMAND and len(element) == 1:
            token.command = TOKENS_COMMAND[element]
        # The element is a valid single character command that reqiures a value
        elif element[0] in TOKENS_COMMAND_VALUE:
            token.command = TOKENS_COMMAND_VALUE[element[0]]
            token.value = element[1:]
            state = switch_lexer_state(state, token.command)
            # If the command is a multi character print
            if token.command == 'PRINT_UNTIL' and element[-1] == '"':
                token.value = element[1:-1]
                state = LexerStates.DEFAULT
            # If the command is a multi character comment
            if token.command == 'COMMENT_START' and element[-1] == ']':
                token.value = element[1:-1]
                state = LexerStates.DEFAULT
    # The lexer will need to add these tokens to the last, so mark them if needed
    elif state != LexerStates.DEFAULT:
        token.command = 'ADD_TO_PREVIOUS'
        combinations = [
            state == LexerStates.GO_UNTIL_NEWLINE and element[-1] == '\n',
            state == LexerStates.GO_UNTIL_END_PRINT and element[-1] == '\"',
            state == LexerStates.GO_UNTIL_END_COMMENT and element[-1] == ']'
        ]
        if any(combinations):
            token.value = element[:-1]
            state = LexerStates.DEFAULT
        else:
            token.value = element

    # Remove empty add to previous that have nothing to do with the string
    if token.value == "\n":
        token.command = None
        token.value = None
    return state, token

def combine_tokens(token_list: List[Token], i: int) -> List[Token]:
    """
    Combines tokens with the next token in the sequence if needed
    """
    tokens = copy(token_list)
    if i == 0:
        tokens.reverse()

    if not i < len(tokens):
        tokens.reverse()
        return tokens

    if tokens[i].command == 'ADD_TO_PREVIOUS':
        tokens[i + 1].value += " " + tokens[i].value
        tokens[i].command = None
    i += 1

    return combine_tokens(tokens, i)

def remove_comments(token_list: List[Token], i: int) -> List[Token]:
    """
    Removes comment tokens
    """
    tokens = copy(token_list)
    if not i < len(tokens):
        return tokens

    if tokens[i].command == 'COMMENT' or tokens[i].command == 'COMMENT_START':
        tokens[i].command = None
        tokens[i].value = None
    i += 1

    return remove_comments(tokens, i)

def cleanup_tokens(token_list: List[Token]) -> List[Token]:
    """
    A function that cleans up the given tokens.

    This is done in three steps:
    1. Filtering out all None tokens
    2. Combining tokens when necessary
    3. Filtering out all None tokens once more

    Returns a list of tokens
    """
    tokens = copy(token_list)

    tokens = list(filter(lambda token: token.command, tokens))
    tokens = combine_tokens(tokens, 0)
    tokens = remove_comments(tokens, 0)
    tokens = list(filter(lambda token: token.command, tokens))

    return tokens

def make_tokens(lexer_vars: LexerVars) -> List[Token]:
    """
    Returns a list of tokens which depend on the previously generated tokens
    """
    tokens = copy(lexer_vars.token_list)
    state = copy(lexer_vars.lexer_state)
    source = copy(lexer_vars.source_list)
    i = copy(lexer_vars.i)

    if not i < len(source):
        return tokens

    state, token = find_token(state, source[i])
    tokens.append(token)

    lexer_variables = LexerVars(
        tokens,
        state,
        source,
        i + 1)

    return make_tokens(lexer_variables)

def lexer(source: str) -> List[Token]:
    """
    A function that converts a string of characters into tokens
    Returns a list of tokens
    """
    source_list = findall(r'\S+|\n', source)
    lexer_vars = LexerVars([], LexerStates.DEFAULT, source_list, 0)
    tokens = make_tokens(lexer_vars)
    return cleanup_tokens(tokens)
