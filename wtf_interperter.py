import parser
from copy import copy

def run(parsed, program_state, index = 0):
    ps = copy(program_state)

    #Find goto labels
    i = 0
    while i < len(parsed):
        if parsed[i].func.__name__ == "label_declare":
            ps.goto_labels[parsed[i].args] = i
        i += 1
    # Run code
    function_index = index
    while function_index < len(parsed):
        if parsed[function_index].func.__name__ == "if_start":
            result = parsed[function_index].func(ps, parsed[function_index].args)
            function_index += 1
            if(result == False): # Start skipping lines until correct stop bracket is found
                ps.if_counter = 1
                while(ps.if_counter > 0 and function_index < len(parsed)):
                    if parsed[function_index].func.__name__ == "if_start":
                        ps.if_counter += 1
                    elif parsed[function_index].func.__name__ == "if_end":
                        ps.if_counter -= 1
                    function_index += 1
        elif parsed[function_index].func.__name__ == "loop_start":
            if parsed[function_index].func(ps, parsed[function_index].args):
                tmp_function_index = function_index + 1
                ps = run(parsed, ps, tmp_function_index)
            else: 
                ps.while_counter = 1
                function_index += 1
                while(ps.while_counter > 0):
                    if parsed[function_index].func.__name__ == "loop_start":
                        ps.while_counter += 1
                    elif parsed[function_index].func.__name__ == "loop_end":
                        ps.while_counter -= 1
                    function_index += 1
        elif parsed[function_index].func.__name__ == "loop_end":
            return ps
        elif parsed[function_index].func.__name__ == "label_goto":
            if parsed[function_index].args in ps.goto_labels:
                function_index = ps.goto_labels[parsed[function_index].func(ps, parsed[function_index].args)]
        elif parsed[function_index].func.__name__ == "label_goto_nonzero":
            if parsed[function_index].func(ps, parsed[function_index].args) and parsed[function_index].args in ps.goto_labels:
                function_index = ps.goto_labels[parsed[function_index].args] + 1
            else:
                function_index += 1
        elif parsed[function_index].func.__name__ == "label_goto_zero":
            if parsed[function_index].func(ps, parsed[function_index].args) and parsed[function_index].args in ps.goto_labels:
                function_index = ps.goto_labels[parsed[function_index].args] + 1
            else:
                function_index += 1


        else:
            ps = parsed[function_index].func(ps, parsed[function_index].args)
            function_index += 1
    return ps
