"""All the objects needed for the lexer, parser, and runner"""
from typing import List
from enum import Enum
from wtf_errors import WtfError


class LexerStates(Enum):
    """A class which represents all the possible states the lexer can be in"""
    DEFAULT = 0
    GO_UNTIL_NEWLINE = 1
    GO_UNTIL_END_COMMENT = 2
    GO_UNTIL_END_PRINT = 3


class Token:
    """A token class which consists of a command and a value if needed"""

    def __init__(self, command: str = None, value: str = None):
        self.command = command
        self.value = value

    def __str__(self):
        return "(" + str(self.command) + ", " + str(self.value) + ")"

    def __repr__(self):
        return self.__str__()


class LexerVars:
    """A lexer data holder which contains information needed to generate tokens"""

    def __init__(self,
                 token_list: List[Token],
                 lexer_state: LexerStates,
                 source_list: List[str],
                 line_nr: int,
                 word_nr: int,
                 errors: List[WtfError]):
        self.tokens = token_list
        self.state = lexer_state
        self.source = source_list
        self.line_nr = line_nr
        self.word_nr = word_nr
        self.errors = errors

    def __str__(self):
        return "(" + str(self.tokens) + "\n " + \
            str(self.source) + "\n " + \
            str(self.state) + "\n " + \
            str(self.line_nr) + "\n " + \
            str(self.word_nr) + ")"

    def __repr__(self):
        return self.__str__()


class ProgramState:
    """A data object that holds the current state of the program and other information"""

    def __init__(self, memory, pointer, error, next_index):
        self.memory = memory
        self.pointer = pointer
        self.errors = error
        self.next_index = next_index
        self.goto_labels = {}

    def get_errors(self, i=0):
        if not i < len(self.errors):
            return ""
        return "\n    " + str(self.errors[i]) + self.get_errors(i + 1)

    def __str__(self):
        return \
            "Memory:\n    " + str(self.memory) + "\n" \
            "Pointer:\n   " + str(self.pointer) + "\n" \
            "Errors: " + self.get_errors()

    def __repr__(self):
        return self.__str__()


class Function:
    """A data object that holds a function and its arguments"""

    def __init__(self, function=None, args=None):
        self.func = function
        self.args = args

    def __str__(self):
        return \
            "Function: " + str(self.func.__name__) + \
            " Arguments: " + str(self.args)

    def __repr__(self):
        return self.__str__()


class Interpreter:
    """A data object to encompass the variables created by the interpreter"""

    def __init__(self, tokens, lexer_errors, parsed, parser_errors, program_state):
        self.tokens = tokens
        self.lexer_errors = lexer_errors
        self.parsed = parsed
        self.parser_errors = parser_errors
        self.program_memory = program_state.memory
        self.program_pointer = program_state.pointer
        self.program_errors = program_state.errors

    def __str__(self):
        return \
            "Tokens: " + str(self.tokens) + "\n" + \
            "Lexer errors: " + str(self.lexer_errors) + "\n" + \
            "Parsed: " + str(self.parsed) + "\n" + \
            "Parser errors: " + str(self.parser_errors) + "\n" + \
            "Program momery: " + str(self.program_memory) + "\n" + \
            "Program pointer" + str(self.program_pointer) + "\n" + \
            "Program errors" + str(self.program_errors) + "\n"

    def __repr__(self):
        return self.__str__()
