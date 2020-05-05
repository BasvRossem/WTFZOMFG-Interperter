"""A python WTFZOMFG interpreter"""

import sys
from copy import copy

from wtf_errors import UnknownTypeError
from wtf_lexer import lexer
from wtf_objects import Function, Interpreter, ProgramState, Token
from wtf_parser import parse
from wtf_functions import CONTROL_FUNCTIONS

# def old_run(parsed, program_state, index=0):
#     ps = copy(program_state)

#     # Find goto labels
#     i = 0
#     while i < len(parsed):
#         if parsed[i].func.__name__ == "label_declare":
#             ps.goto_labels[parsed[i].args] = i
#         i += 1
#     # Run code
#     function_index = index
#     while function_index < len(parsed):

#         if parsed[function_index].func.__name__ == "if_start":
#             result = parsed[function_index].func(
#                 ps, parsed[function_index].args)
#             function_index += 1
#             if(result == False):  # Start skipping lines until correct stop bracket is found
#                 ps.if_counter = 1
#                 while(ps.if_counter > 0 and function_index < len(parsed)):
#                     if parsed[function_index].func.__name__ == "if_start":
#                         ps.if_counter += 1
#                     elif parsed[function_index].func.__name__ == "if_end":
#                         ps.if_counter -= 1
#                     function_index += 1
#         elif parsed[function_index].func.__name__ == "loop_start":
#             if parsed[function_index].func(ps, parsed[function_index].args):
#                 tmp_function_index = function_index + 1
#                 ps = run(parsed, ps, tmp_function_index)
#             else:
#                 ps.while_counter = 1
#                 function_index += 1
#                 while(ps.while_counter > 0):
#                     if parsed[function_index].func.__name__ == "loop_start":
#                         ps.while_counter += 1
#                     elif parsed[function_index].func.__name__ == "loop_end":
#                         ps.while_counter -= 1
#                     function_index += 1
#         elif parsed[function_index].func.__name__ == "loop_end":
#             return ps
#         elif parsed[function_index].func.__name__ == "label_goto":
#             if parsed[function_index].args in ps.goto_labels:
#                 function_index = ps.goto_labels[parsed[function_index].func(
#                     ps, parsed[function_index].args)]
#         elif parsed[function_index].func.__name__ == "label_goto_nonzero":
#             if parsed[function_index].func(ps, parsed[function_index].args) and \
#                 parsed[function_index].args in ps.goto_labels:
#                 function_index = ps.goto_labels[parsed[function_index].args] + 1
#             else:
#                 function_index += 1
#         elif parsed[function_index].func.__name__ == "label_goto_zero":
#             if parsed[function_index].func(ps, parsed[function_index].args) and \
#                 parsed[function_index].args in ps.goto_labels:
#                 function_index = ps.goto_labels[parsed[function_index].args] + 1
#             else:
#                 function_index += 1

#         else:
#             ps = parsed[function_index].func(ps, parsed[function_index].args)
#             function_index += 1
#     return ps


def pre_run(program_state, functions):
    p_s = copy(program_state)
    fnc = copy(functions)

    i = 0
    while i < len(fnc):
        # Check if it is a function and remove if it isn't
        if not isinstance(fnc[i], type(Function())):
            p_s.errors.append(UnknownTypeError(Function(), fnc[i]))
            fnc.pop(i)
        else:
            if fnc[i].func.__name__ == "label_declare":
                p_s.goto_labels[fnc[i].args] = i
            i += 1

    return p_s, fnc


def skip_to_end(functions, index, start, end):
    i = copy(index)
    counter = 1
    while(counter > 0 and i < len(functions)):
        if functions[i].func.__name__ == start:
            counter += 1
        elif functions[i].func.__name__ == end:
            counter -= 1
        i += 1

    return i


def execute(program_state, functions, index=0):
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
            index = skip_to_end(functions, index, "if_start", "if_end")

    # Loop function
    elif function in CONTROL_FUNCTIONS and function.__name__ == "loop_start":
        if function(p_s):
            p_s.next_index = index + 1
            p_s = execute(p_s, functions, p_s.next_index)
        else:
            index += 1
            index = skip_to_end(functions, index, "loop_start", "loop_end")

    elif function in CONTROL_FUNCTIONS and function.__name__ == "loop_end":
        p_s.next_index = index + 1
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
    elif function in CONTROL_FUNCTIONS and function.__name__ == "label_declare" or function.__name__ == "if_end":
        index += 1

    # =================== #
    # All other functions #
    # =================== #
    else:
        p_s = function(p_s, argument)
        index += 1

    p_s.next_index = index

    return execute(p_s, functions, p_s.next_index)


def run(program_state, functions):
    p_s = copy(program_state)
    fncs = copy(functions)

    p_s, fncs = pre_run(p_s, fncs)
    p_s = execute(p_s, fncs)
    return p_s


def interpret(file, memory_length, ignore_errors):
    source = open(file, "r")
    tokens, lexer_errors = lexer(source)
    # tokens.append("Hey how are ya")
    # tokens.append(Token(None, "Ho"))

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

    # parsed.append("Hey how are ya")
    # parsed.append(Token(None, "Ho"))

    # for fnc in TOKENS: print(fnc)
    memory = [0 for i in range(memory_length)]
    pointer = 0
    program = ProgramState(memory, pointer, [], 0)
    program_state = run(program, parsed)

    if program_state.errors and not ignore_errors:
        print("There were runtime errors:")
        for err in program_state.errors:
            print(err)

    return Interpreter(tokens, lexer_errors, parsed, parser_errors, program_state)
