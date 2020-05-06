"""A python WTFZOMFG interpreter"""

import sys
from copy import copy
from typing import List, Tuple

from wtf_errors import UnknownTypeError
from wtf_functions import CONTROL_FUNCTIONS
from wtf_lexer import lexer
from wtf_objects import Function, Interpreter, ProgramState
from wtf_parser import parse


def execute_counter(function):
    """
    A decorator to count how many times a function is executed
    """
    def inner(program_state: ProgramState,
              functions: List[Function],
              index: int = 0) -> ProgramState:
        inner.counter += 1
        return function(program_state, functions, index)
    inner.counter = 0
    return inner


def pre_run(program_state: ProgramState,
            functions: List[Function],
            index: int) -> Tuple[ProgramState, List[Function]]:
    """
    Does some function cleanup and finds all goto declarations
    """
    p_s = copy(program_state)
    fnc = copy(functions)

    i = index

    if not i < len(fnc):
        return p_s, fnc

    # Check if it is a function and remove if it isn't
    if not isinstance(fnc[i], type(Function())):
        p_s.errors.append(UnknownTypeError(Function(), fnc[i]))
        fnc.pop(i)
    else:
        if fnc[i].func.__name__ == "label_declare":
            p_s.goto_labels[fnc[i].args] = i
        i += 1

    return pre_run(p_s, fnc, i)


def skip_to_end(functions: List[Function], index: int, start: str, end: str, counter: int) -> int:
    """
    Recursivly searches for the end function of an if statement or
    while loop and returns the index of the function afther that
    """
    i = copy(index)
    cntr = counter

    if not cntr > 0 and i < len(functions):
        return i

    if functions[i].func.__name__ == start:
        cntr += 1
    elif functions[i].func.__name__ == end:
        cntr -= 1

    i += 1

    return skip_to_end(functions, i, start, end, cntr)


@execute_counter
def execute(program_state: ProgramState, functions: List[Function], index: int = 0) -> ProgramState:
    """
    Executes the list of functions recursively for every function.
    Maganes lops, if statements, while loops and goto statements.
    """
    p_s = copy(program_state)

    if not index < len(functions):
        return p_s

    function = functions[index].func
    argument = functions[index].args

    # ======================= #
    # Check control functions #
    # ======================= #
    # If function
    if function in CONTROL_FUNCTIONS and function.__name__ == "if_start":
        index += 1
        if not function(p_s):
            index = skip_to_end(functions, index, "if_start", "if_end", 1)

    # Loop function
    elif function in CONTROL_FUNCTIONS and function.__name__ == "loop_start":
        if function(p_s):
            p_s.next_index = index + 1
            p_s = execute(p_s, functions, p_s.next_index)
        else:
            index += 1
            index = skip_to_end(functions, index, "loop_start", "loop_end", 1)

    elif function in CONTROL_FUNCTIONS and function.__name__ == "loop_end":
        p_s.next_index = index
        return p_s

    elif function in CONTROL_FUNCTIONS and \
            function.__name__ == "label_goto_nonzero" or \
            function.__name__ == "label_goto_zero" or \
            function.__name__ == "label_goto":
        if function(p_s) and argument in p_s.goto_labels:
            index = p_s.goto_labels[argument] + 1
        else:
            index += 1

    # Empty functions, they exists to help the interpreter
    elif function.__name__ == "label_declare" or function.__name__ == "if_end":
        index += 1

    # =================== #
    # All other functions #
    # =================== #
    elif argument:
        p_s = function(p_s, argument)
        index += 1
    else:
        p_s = function(p_s)
        index += 1

    p_s.next_index = index

    return execute(p_s, functions, p_s.next_index)


def run(program_state: ProgramState, functions: List[Function]) -> Tuple[ProgramState, int]:
    """
    A function that executes the program
    """
    p_s = copy(program_state)
    fncs = copy(functions)

    p_s, fncs = pre_run(p_s, fncs, 0)
    p_s = execute(p_s, fncs)
    return p_s, execute.counter


def interpret(file: str, memory_length: int, ignore_errors: bool) -> Interpreter:
    """
    This frunction interprets a WTFZOMGF file,
    runs the program and returns an object containing
    errors and the final state of the program.
    """
    source = open(file, "r")
    tokens, lexer_errors = lexer(source)

    if lexer_errors and not ignore_errors:
        print("There were lexer errors:")
        for err in lexer_errors:
            print(err)
        if input("Would you like to continue? y/n ").lower() != "y":
            sys.exit()

    parsed, parser_errors = parse(tokens)

    if parser_errors and not ignore_errors:
        print("There were parser errors:")
        for err in parser_errors:
            print(err)
        if input("Would you like to continue? y/n ").lower() != "y":
            sys.exit()

    memory = [0 for i in range(memory_length)]
    pointer = 0
    program = ProgramState(memory, pointer, [], 0)
    program_state, count = run(program, parsed)

    if program_state.errors and not ignore_errors:
        print("There were runtime errors:")
        for err in program_state.errors:
            print(err)
    print("Execute was called", count, "times")
    return Interpreter(tokens, lexer_errors, parsed, parser_errors, program_state)
