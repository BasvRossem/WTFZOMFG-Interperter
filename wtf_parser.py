def increase_pointer(memory, pointer):
    new_memory = memory.copy()
    new_memory[pointer] += 1
    return new_memory, pointer

def decrease_pointer(memory, pointer):
    new_memory = memory.copy()
    new_memory[pointer] -= 1
    return new_memory, pointer

def print_pointer(memory, pointer):
    print(memory[pointer])
    return memory, pointer

def shift_left(memory, pointer):
    new_pointer = pointer - 1 
    return memory, new_pointer

def shift_right(memory, pointer):
    new_pointer = pointer + 1 
    return memory, new_pointer

def loop(memory, pointer, functions):
    new_memory = memory.copy()
    new_pointer = pointer
    while(new_memory[new_pointer] != 0):
        for function in functions:
            if(type(function) == type([])):
                new_memory, new_pointer = function[0](memory = new_memory, pointer = new_pointer, functions = function[1])
            else:
                new_memory, new_pointer = function(memory = new_memory, pointer = new_pointer)
    return new_memory, new_pointer

def print_until(memory, pointer, functions):
    new_memory = memory.copy()
    new_pointer = pointer
    print(functions)
    return new_memory, new_pointer

def parse(tokens, custom_token_index = 0):
    functions = []
    token_index = custom_token_index
    while (token_index < len(tokens)):
        if tokens[token_index][0] == 'PLUS':
            functions.append(increase_pointer)
        elif tokens[token_index][0] == 'MINUS':
            functions.append(decrease_pointer)
        elif tokens[token_index][0] == 'PRINT':
            functions.append(print_pointer)
        elif tokens[token_index][0] == 'SHIFT_LEFT':
            functions.append(shift_left)
        elif tokens[token_index][0] == 'SHIFT_RIGHT':
            functions.append(shift_right)
        elif tokens[token_index][0] == 'COMMENT':
            while(token_index < len(tokens) and tokens[token_index][0] != 'END_LINE'):
                token_index += 1
        elif tokens[token_index][0] == 'BEGIN_LOOP': 
            token_index += 1
            returned_functions, token_index = parse(tokens, token_index)
            functions.append([loop, returned_functions])
        elif tokens[token_index][0] == 'END_LOOP': 
            token_index += 1
            return functions, token_index  
        elif tokens[token_index][0] == 'PRINT_UNTIL':
            token_index += 1
            total_string = ""
            while(tokens[token_index][0] != 'PRINT_STOP'):
                total_string += tokens[token_index][1]
                token_index += 1
            functions.append([print_until, total_string])
        token_index += 1
    return functions, token_index