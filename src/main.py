from lexer import Lexer
from parser_class import Parser
import traceback
import logging
import coloredlogs

DEBUG = False

lexer = Lexer().get_lexer()
pg = Parser()
pg.parse()
parser = pg.get_parser()
logger = logging.getLogger(__name__)
coloredlogs.install(level=logging.DEBUG)

program = input("Enter program: ")
if program == "ide.ls":
    while True:
        try:
            text_input = input(">> ")
            if text_input == "exit()":
                break
            elif text_input == "clear()":
                print("\n" * 100)
                # clear the global_context
                parser.global_context = {}
                continue
            elif text_input == "debug()":
                DEBUG = not DEBUG
                continue
            elif text_input == "help()":
                print("Here are a list of commands for the IDE: ")
                print("exit: Exits the IDE")
                print(
                    "clear(): Restarts the session (clears screen as well as the VM varible list")
                print("help(): Prints this list")
                print("debug(): Toggles debug mode")
                continue
            elif text_input == "":
                continue
            tokens = lexer.lex(text_input)
            if DEBUG:
                for token in tokens.copy():
                    logging.debug((token))
            parser.parse(tokens).eval()
        except Exception as e:
            traceback.print_exc()
            logging.critical("VM crashed, resuming execution runtime")
else:
    with open(program, "r") as file:
        text_input = file.read()
        # tokenize the input
        tokens = lexer.lex(text_input)
        if DEBUG:
            for token in tokens:
                print(token)
        # parse the tokens
        parser.parse(tokens).eval()
