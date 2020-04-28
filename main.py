from wtf_lexer import make_tokens
from wtf_parser import parse 
from wtf_interperter import run

source = open("wtf/beer.wtf", "r").read()
tokens = make_tokens(source)
# print(tokens)
# parsed = parse(tokens)[0]

# memory = [0 for i in range(10)]
# pointer = 0
# error, memory, pointer = run(parsed, memory, pointer)