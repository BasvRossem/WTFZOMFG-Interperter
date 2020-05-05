"""Module that holds all functionalities that WTFZOMFG can do"""
from copy import copy

# def function_template(program_state, args):
#     p_s = copy(program_state)

#     return p_s

# Control
def label_goto(args):
    return args

def label_declare(program_state):
    return program_state

def label_goto_nonzero(program_state):
    if int(program_state.memory[program_state.pointer]):
        return True
    return False

def label_goto_zero(program_state):
    if int(program_state.memory[program_state.pointer]):
        return False
    return True

def loop_start(program_state):
    if program_state.memory[program_state.pointer]:
        return True
    return False

def loop_end(program_state):
    return program_state

def if_start(program_state):
    p_s = copy(program_state)
    if p_s.memory[p_s.pointer]:
        return True
    return False

def if_end(program_state):
    p_s = copy(program_state)
    return p_s

# Cell/Pointer Manipulation
def cell_increase(program_state, args):
    p_s = copy(program_state)
    p_s.memory[p_s.pointer] += 1
    return p_s

def cell_decrease(program_state, args):
    p_s = copy(program_state)
    p_s.memory[p_s.pointer] -= 1
    return p_s

def cell_flip(program_state, args):
    p_s = copy(program_state)
    if p_s.memory[p_s.pointer]:
        p_s.memory[p_s.pointer] = 0
    else:
        p_s.memory[p_s.pointer] = 1
    return p_s

def cell_set(program_state, args):
    p_s = copy(program_state)
    p_s.memory[p_s.pointer] = int(args)
    return p_s

def cell_increase_with(program_state, args):
    p_s = copy(program_state)
    p_s.memory[p_s.pointer] += int(args)
    return p_s

def copy_value_right(program_state, args):
    p_s = copy(program_state)
    p_s.memory[p_s.pointer + 1] = p_s.memory[p_s.pointer]
    return p_s

def copy_value_to(program_state, args):
    p_s = copy(program_state)
    p_s.memory[int(args)] = p_s.memory[p_s.pointer]
    return p_s

def pointer_move_left(program_state, args):
    p_s = copy(program_state)
    p_s.pointer -= 1
    return p_s

def pointer_move_right(program_state, args):
    p_s = copy(program_state)
    p_s.pointer += 1
    if p_s.pointer < 0:
        p_s.error = "Memory pointer cannot be a negative number"
    return p_s

def pointer_move_to(program_state, args):
    p_s = copy(program_state)
    p_s.pointer = int(args)
    if p_s.pointer < 0:
        p_s.error = "Memory pointer cannot be a negative number"
    return p_s

def pointer_move_relative(program_state, args):
    p_s = copy(program_state)
    p_s.pointer += int(args)
    if p_s.pointer < 0:
        p_s.error = "Memory pointer cannot be a negative number"
    return p_s

def cell_subtract_ascii(program_state, args):
    p_s = copy(program_state)
    p_s.memory[p_s.pointer] -= ord(args[0])
    return p_s

# Arithmetic
def cell_add_right(program_state, args):
    p_s = copy(program_state)
    p_s.memory[p_s.pointer] = int(p_s.memory[p_s.pointer] + p_s.memory[p_s.pointer + 1])
    return p_s

def cell_subtract_right(program_state, args):
    p_s = copy(program_state)
    p_s.memory[p_s.pointer] = int(p_s.memory[p_s.pointer] - p_s.memory[p_s.pointer + 1])
    return p_s

def cell_multiply_right(program_state, args):
    p_s = copy(program_state)
    p_s.memory[p_s.pointer] = int(p_s.memory[p_s.pointer] * p_s.memory[p_s.pointer + 1])
    return p_s

def cell_devide_right(program_state, args):
    p_s = copy(program_state)
    p_s.memory[p_s.pointer] = int(p_s.memory[p_s.pointer] / p_s.memory[p_s.pointer + 1])
    return p_s

# Input/Output
def scan_ascii(program_state, args):
    p_s = copy(program_state)
    p_s.memory[p_s.pointer] = str(input())[0]
    return p_s

def scan_decimal(program_state, args):
    p_s = copy(program_state)
    p_s.memory[p_s.pointer] = int(input())
    return p_s

def print_cell_ascii(program_state, args):
    p_s = copy(program_state)
    print(p_s.memory[p_s.pointer], end="")
    return p_s

def print_cell_decimal(program_state, args):
    p_s = copy(program_state)
    print(int(p_s.memory[p_s.pointer]), end="")
    return p_s

def print_character(program_state, args):
    p_s = copy(program_state)
    print(args.replace("\\n", "\n"), end="")
    return p_s


def print_until(program_state, args):
    p_s = copy(program_state)
    print(args.replace("\\n", "\n"), end="")
    return p_s

# Debug
def print_program_state(program_state, args):
    p_s = copy(program_state)
    print(p_s.pointer, p_s.memory)
    return p_s

TOKEN_FUNCTIONS = {
    'LABEL_GOTO': label_goto,
    'LABEL_DECLARE': label_declare,
    'LABEL_GOTO_NONZERO': label_goto_nonzero,
    'LABEL_GOTO_ZERO': label_goto_zero,
    'LOOP_START': loop_start,
    'LOOP_END': loop_end,
    'IF_START': if_start,
    'IF_END': if_end,
    'CELL_INCREASE': cell_increase,
    'CELL_DECREASE': cell_decrease,
    'CELL_FLIP': cell_flip,
    'CELL_SET': cell_set,
    'CELL_INCREASE_WITH': cell_increase_with,
    'COPY_VALUE_RIGHT': copy_value_right,
    'COPY_VALUE_TO': copy_value_to,
    'POINTER_MOVE_LEFT': pointer_move_left,
    'POINTER_MOVE_RIGHT': pointer_move_right,
    'POINTER_MOVE_TO': pointer_move_to,
    'POINTER_MOVE_RELATIVE': pointer_move_relative,
    'CELL_SUBTRACT_ASCII': cell_subtract_ascii,
    'CELL_ADD_RIGHT': cell_add_right,
    'CELL_SUBTRACT_RIGHT': cell_subtract_right,
    'CELL_MULTIPLY_RIGHT': cell_multiply_right,
    'CELL_DEVIDE_RIGHT': cell_devide_right,
    'SCAN_ASCII': scan_ascii,
    'SCAN_DECIMAL': scan_decimal,
    'PRINT_CELL_ASCII': print_cell_ascii,
    'PRINT_CELL_DECIMAL': print_cell_decimal,
    'PRINT_CHARACTER': print_character,
    'PRINT_UNTIL': print_until,
    'PRINT_PROGRAM_STATE': print_program_state}

CONTROL_FUNCTIONS = [
    label_goto,
    label_declare,
    label_goto_nonzero,
    label_goto_zero,
    loop_start,
    loop_end,
    if_start,
    if_end]
