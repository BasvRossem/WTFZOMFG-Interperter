"""Module for a WTFZOMFG parser"""
from wtf_objects import Function
from wtf_functions import TOKEN_FUNCTIONS

def find_function(token):
    return Function(TOKEN_FUNCTIONS[token.command], token.value)

def parse(tokens):
    functions = list(map(find_function, tokens))

    return functions
