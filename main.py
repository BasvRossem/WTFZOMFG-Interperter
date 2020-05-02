"""Module to run the interperter"""
import wtf_lexer
import wtf_parser
import wtf_interperter
import wtf_objects

SOURCE = open("wtf/test2.wtf", "r").read()
TOKENS = wtf_lexer.lexer(SOURCE)
print(TOKENS)
PARSED = wtf_parser.parse(TOKENS)
print(PARSED)
MEMORY = [0 for i in range(10)]
POINTER = 0
PROGRAM = wtf_objects.ProgramState(MEMORY, POINTER, 0)
PS = wtf_interperter.run(PARSED, PROGRAM)
print(PS)
