from typing import List, Tuple
from enum import Enum

class LexerStates(Enum):
    """A class which represents all the possible states the lexer can be in"""
    DEFAULT = 0
    GO_UNTIL_NEWLINE = 1
    GO_UNTIL_END_COMMENT = 2
    GO_UNTIL_END_PRINT = 3

class Token():
    """A token class which consists of a command and a value if needed"""
    def __init__(self, command: str, value: str):
        self.command = command
        self.value = value

    def __str__(self):
        return "(" + str(self.command) + ", " + str(self.value) + ")"

    def __repr__(self):
        return self.__str__()

class LexerVars():
    """A lexer data holder which contains information needed to generate tokens"""
    def __init__(self,
                 token_list: List[Token],
                 lexer_state: LexerStates,
                 source_list: List[str],
                 i: int):
        self.token_list = token_list
        self.lexer_state = lexer_state
        self.source_list = source_list
        self.i = i

    def __str__(self):
        return "(" + str(self.token_list) + ", " + \
                    str(self.source_list) + ", " + \
                    str(self.lexer_state) + ", " + \
                    str(self.i) + ")"

    def __repr__(self):
        return self.__str__()

class ProgramState():
    def __init__(self, memory, pointer, error):
        self.memory = memory
        self.pointer = pointer
        self.error = error
        self.goto_labels = {}

    def __str__(self):
        return \
            "Memory: " + str(self.memory) + "\n" \
            "Pointer: " + str(self.pointer) + "\n" \
            "Error: " + str(self.error)
    
    def __repr__(self):
        return self.__str__()

class Function():
    def __init__(self, function, args):
        self.func = function
        self.args = args
    
    def __str__(self):
        return \
            "Function: " + str(self.func.__name__) + \
            " Arguments: " + str(self.args)
    
    def __repr__(self):
        return self.__str__()
