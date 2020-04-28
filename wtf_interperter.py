import parser
from copy import copy

def run(parsed, program_state):
    ps = copy(program_state)
    for function in parsed:
        ps = function.func(ps, function.args)
    return ps
