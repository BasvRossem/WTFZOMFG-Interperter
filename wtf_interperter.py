import parser

def run(parsed, memory = [], pointer = 0):
    mem = memory.copy()
    ptr = pointer
    err = 0
    for function in parsed:
        if(type(function) == type([])):
            mem, ptr = function[0](mem, ptr, function[1])
        else:
            mem, ptr = function(mem, ptr)
    return err, mem, ptr
