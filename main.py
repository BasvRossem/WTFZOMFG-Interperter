import wtf_lexer
import wtf_parser  
import wtf_interperter

source = open("wtf/test.wtf", "r").read()
tokens = wtf_lexer.make_tokens(source)
# for tok in tokens:
#     print(tok)
parsed = wtf_parser.parse(tokens)[0]
# for func in parsed:
#     print(func)
memory = [0 for i in range(10)]
pointer = 0
program = wtf_parser.ProgramState(memory, pointer, 0)
ps = wtf_interperter.run(parsed, program)