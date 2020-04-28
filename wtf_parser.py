from copy import copy

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

def function_template(program_state, args):
    ps = copy(program_state)

    return ps

# Control
def label_goto(program_state, args):
    return args

def label_declare(program_state, args):
    return program_state

def label_goto_nonzero(program_state, args):
    if int(program_state.memory[program_state.pointer]):
        return True
    return False

def label_goto_zero(program_state, args):
    if int(program_state.memory[program_state.pointer]):
        return False
    return True

def loop_start(program_state, args):
    if(program_state.memory[program_state.pointer]):
        return True
    return False

def loop_end(program_state, args):
    return program_state

def if_start(program_state, args):
    ps = copy(program_state)
    if(ps.memory[ps.pointer]):
        return True
    return False

def if_end(program_state, args):
    ps = copy(program_state)
    return ps

# Cell/Pointer Manipulation
def cell_increase(program_state, args):
    ps = copy(program_state)
    ps.memory[ps.pointer] += 1
    return ps

def cell_decrease(program_state, args):
    ps = copy(program_state)
    ps.memory[ps.pointer] -= 1
    return ps

def cell_flip(program_state, args):
    ps = copy(program_state)
    if ps.memory[ps.pointer]:
        ps.memory[ps.pointer] = 0
    else:
        ps.memory[ps.pointer] = 1
    return ps

def cell_set(program_state, args):
    ps = copy(program_state)
    ps.memory[ps.pointer] = int(args)
    return ps

def cell_increase_with(program_state, args):
    ps = copy(program_state)
    ps.memory[ps.pointer] += int(args)
    return ps

def copy_value_right(program_state, args):
    ps = copy(program_state)
    ps.memory[ps.pointer + 1] = ps.memory[ps.pointer]
    return ps

def copy_value_to(program_state, args):
    ps = copy(program_state)
    ps.memory[int(args)] = ps.memory[ps.pointer]
    return ps

def pointer_move_left(program_state, args):
    ps = copy(program_state)
    ps.pointer -= 1
    return ps

def pointer_move_right(program_state, args):
    ps = copy(program_state)
    ps.pointer += 1
    if ps.pointer < 0:
        ps.error = "Memory pointer cannot be a negative number"
    return ps

def pointer_move_to(program_state, args):
    ps = copy(program_state)
    ps.pointer = int(args)
    if ps.pointer < 0:
        ps.error = "Memory pointer cannot be a negative number"
    return ps

def pointer_move_relative(program_state, args):
    ps = copy(program_state)
    ps.pointer += int(args)
    if ps.pointer < 0:
        ps.error = "Memory pointer cannot be a negative number"
    return ps

def cell_subtract_ascii(program_state, args):
    ps = copy(program_state)
    ps.memory[ps.pointer] -= ord(args[0])
    return ps

# Arithmetic
def cell_add_right(program_state, args):
    ps = copy(program_state)
    ps.memory[ps.pointer] = int(ps.memory[ps.pointer] + ps.memory[ps.pointer + 1])
    return ps

def cell_subtract_right(program_state, args):
    ps = copy(program_state)
    ps.memory[ps.pointer] = int(ps.memory[ps.pointer] - ps.memory[ps.pointer + 1])
    return ps

def cell_multiply_right(program_state, args):
    ps = copy(program_state)
    ps.memory[ps.pointer] = int(ps.memory[ps.pointer] * ps.memory[ps.pointer + 1])
    return ps

def cell_devide_right(program_state, args):
    ps = copy(program_state)
    ps.memory[ps.pointer] = int(ps.memory[ps.pointer] / ps.memory[ps.pointer + 1])
    return ps

# Input/Output
def scan_ascii(program_state, args):
    ps = copy(program_state)
    ps.memory[ps.pointer] = str(input())[0]
    return ps

def scan_decimal(program_state, args):
    ps = copy(program_state)
    ps.memory[ps.pointer] = int(input())
    return ps

def print_cell_ascii(program_state, args):
    ps = copy(program_state)
    print(ps.memory[ps.pointer], end="")
    return ps

def print_cell_decimal(program_state, args):
    ps = copy(program_state)
    print(int(ps.memory[ps.pointer]), end="")
    return ps

def print_character(program_state, args):
    ps = copy(program_state)
    print(args.replace("\\n", "\n"), end="")
    return ps


def print_until(program_state, args):
    ps = copy(program_state)
    print(args.replace("\\n", "\n"), end="")
    return ps

# Debug
def print_program_state(program_state, args):
    ps = copy(program_state)
    print(ps)
    return ps

def parse(tokens, token_index = 0):
    functions = []
    i = token_index
    while (i < len(tokens)):
        print(str(i)+"/"+str(len(tokens) - 1), tokens[i])
        # Control
        if tokens[i].command == 'LABEL_GOTO':
            functions.append(Function(label_goto, tokens[i].value))
        elif tokens[i].command == 'LABEL_DECLARE':
            functions.append(Function(label_declare, tokens[i].value))
        elif tokens[i].command == 'LABEL_GOTO_NONZERO':
            functions.append(Function(label_goto_nonzero, tokens[i].value))
        elif tokens[i].command == 'LABEL_GOTO_ZERO':
            functions.append(Function(label_goto_zero, tokens[i].value))
        elif tokens[i].command == 'LOOP_START':
            functions.append(Function(loop_start, None))
        elif tokens[i].command == 'LOOP_END':
            functions.append(Function(loop_end, None))
        elif tokens[i].command == 'IF_START':
            functions.append(Function(if_start, None))
        elif tokens[i].command == 'IF_END':
            functions.append(Function(if_end, None))

        # Cell/Pointer manipulation
        elif tokens[i].command == 'CELL_INCREASE':
            functions.append(Function(cell_increase, None))
        elif tokens[i].command == 'CELL_DECREASE':
            functions.append(Function(cell_decrease, None))
        elif tokens[i].command == 'CELL_FLIP':
            functions.append(Function(cell_flip, None))
        elif tokens[i].command == 'CELL_SET':
            functions.append(Function(cell_set, tokens[i].value))
        elif tokens[i].command == 'CELL_INCREASE_WITH':
            functions.append(Function(cell_increase_with, tokens[i].value))

        elif tokens[i].command == 'COPY_VALUE_RIGHT':
            functions.append(Function(copy_value_right, None))
        elif tokens[i].command == 'COPY_VALUE_TO':
            functions.append(Function(copy_value_to, tokens[i].value))

        elif tokens[i].command == 'POINTER_MOVE_LEFT':
            functions.append(Function(pointer_move_left, None))
        elif tokens[i].command == 'POINTER_MOVE_RIGHT':
            functions.append(Function(pointer_move_right, None))
        elif tokens[i].command == 'POINTER_MOVE_TO':
            functions.append(Function(pointer_move_to, tokens[i].value))
        elif tokens[i].command == 'POINTER_MOVE_RELATIVE':
            functions.append(Function(pointer_move_relative, tokens[i].value))
        
        elif tokens[i].command == 'CELL_SUBTRACT_ASCII':
            functions.append(Function(cell_subtract_ascii, tokens[i].value))

        # Arithmetic
        elif tokens[i].command == 'CELL_ADD_RIGHT':
            functions.append(Function(cell_add_right, None))
        elif tokens[i].command == 'CELL_SUBTRACT_RIGHT':
            functions.append(Function(cell_subtract_right, None))
        elif tokens[i].command == 'CELL_MULTIPLY_RIGHT':
            functions.append(Function(cell_multiply_right, None))
        elif tokens[i].command == 'CELL_DEVIDE_RIGHT':
            functions.append(Function(cell_devide_right, None))

        # Input/Output
        elif tokens[i].command == 'SCAN_ASCII':
            functions.append(Function(scan_ascii, None))
        elif tokens[i].command == 'SCAN_DECIMAL':
            functions.append(Function(scan_decimal, None))
        elif tokens[i].command == 'PRINT_CELL_ASCII':
            functions.append(Function(print_cell_ascii, None))
        elif tokens[i].command == 'PRINT_CELL_DECIMAL':
            functions.append(Function(print_cell_decimal, None))
        elif tokens[i].command == 'PRINT_CHARACTER':
            functions.append(Function(print_character, tokens[i].value))
        elif tokens[i].command == 'PRINT_UNTIL':
            functions.append(Function(print_until, tokens[i].value))
        
        # Debug
        elif tokens[i].command == 'PRINT_PROGRAM_STATE':
            functions.append(Function(print_program_state, None))
        i += 1
    return functions, i