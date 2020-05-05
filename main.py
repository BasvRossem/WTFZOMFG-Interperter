"""Example main"""
import argparse
from wtf_interperter import interpret

if __name__ == "__main__":
    # Parsing command line arguments
    ARG_PARSER = argparse.ArgumentParser(
        description='Interprets wtfzomfg code froma file')

    ARG_PARSER.add_argument("-f", "--file", required=True,
                            type=str, help="filepath to a .wtf file")
    ARG_PARSER.add_argument("-m", "--memory", required=True,
                            type=int, help="amount of cells of memory the program has")
    ARG_PARSER.add_argument("-e", "--ignore_errors", action="store_true",
                            help="use this to ignore errors")

    ARGS = ARG_PARSER.parse_args()

    # Creatign variables needed to interpret
    FILE = ARGS.file
    MEM_SIZE = ARGS.memory
    IGNORE_ERRORS = ARGS.ignore_errors

    # Interpret
    OUTPUT = interpret(FILE, MEM_SIZE, IGNORE_ERRORS)

    # print errors
    print(OUTPUT.lexer_errors)
    print(OUTPUT.parser_errors)
    print(OUTPUT.program_errors)
