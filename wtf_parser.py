from copy import copy

class ProgramState():
    def __init__(self, memory, pointer, error):
        self.memory = memory
        self.pointer = pointer
        self.error = error
    
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
def if_start(program_state, args):
    ps = copy(program_state)
    if ps.memory[ps.pointer] != 0:
        for function in args:
            ps = function.func(ps, function.args)
    return ps

def loop(program_state, args):
    new_memory = memory.copy()
    new_pointer = pointer
    while(new_memory[new_pointer] != 0):
        for function in functions:
            if(type(function) == type([])):
                new_memory, new_pointer = function[0](memory = new_memory, pointer = new_pointer, functions = function[1])
            else:
                new_memory, new_pointer = function(memory = new_memory, pointer = new_pointer)
    return new_memory, new_pointer

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
    ps.memory[ps.pointer] -= ord(args)
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
        if tokens[i].command == 'IF_START':
            args, i = parse(tokens, i + 1)
            functions.append(Function(if_start, args))
        elif tokens[i].command == 'IF_END':
            break

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
        elif tokens[i].command == 'PRINT_UNTIL':
            functions.append(Function(print_until, tokens[i].value))
        
        # Debug
        elif tokens[i].command == 'PRINT_PROGRAM_STATE':
            functions.append(Function(print_program_state, None))
        i += 1
    return functions, i