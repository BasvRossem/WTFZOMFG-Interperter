"""Module for a WTFZOMFG parser"""
from typing import List, Tuple, Union

from wtf_errors import UnknownTokenError, UnknownTypeError, WtfError
from wtf_functions import TOKEN_FUNCTIONS
from wtf_objects import Function, Token


def find_function(token: Token) -> Union[Function, WtfError]:
    """
    Match a token to a function and return a Function object
    or an error if no corresponding function can be found.
    """
    if type(token) is not type(Token()):
        return UnknownTypeError(Token(), token)
    if token.command not in TOKEN_FUNCTIONS:
        return UnknownTokenError(token)
    return Function(TOKEN_FUNCTIONS[token.command], token.value)


def parse(tokens: List[Token]) -> Tuple[List[Function], List[WtfError]]:
    """
    Parse a list of tokens. Return two lists,
    one with the corrsponding functions, and one with errors
    """
    response = list(map(find_function, tokens))

    functions = list(filter(lambda elmnt: issubclass(
        type(elmnt), type(Function())), response))
    errors = list(filter(lambda elmnt: issubclass(
        type(elmnt), type(WtfError())), response))

    return functions, errors
