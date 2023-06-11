import os
import argparse
import nodes
from typing import Any


grouping_symbols = {"'", '"'}
enclosing_symbols = {'(', ')', '{', '}', '[', ']'}
operator_symbols = {'+', '-', '*', '/', '%', '=', '>', '<', '|', '&', '.', ':', '!', ',', '^', '$'}


def tokenize(input_file: str) -> list[str]:
    """Tokenizes the input file. All languages are tokenized the same way."""
    global grouping_symbols

    tokens = [] #holds all tokens
    group = None
    with open(input_file, "r") as file:

        mode = 1
        token = ""
        while (line := file.readline()) != "": #iterate through every line
            #mode = 1 #start by counting the indentation of this line
            #token = "" #holds the current token
            '''
            RULES
            -only place a newline when entering mode 1

            '''
            for c in line:

                match mode:
                    case 0: #neutral case, just finding new tokens on a line
                        if c == " ": #push last token if it's not empty
                            if token != "":
                                #tokens.append("MODE0")
                                tokens.append(token)
                            token = ""
                        elif c == "\n": #switch mode
                            if token != "":
                                #tokens.append("MODE0")
                                tokens.append(token)
                            tokens.append("\n")
                            token = ""
                            mode = 1
                        elif c in grouping_symbols: #start a group
                            if token != "":
                                #tokens.append("MODE0")
                                tokens.append(token)
                            token = ""
                            group = c
                            mode = 2
                        elif c in enclosing_symbols or c in operator_symbols:
                            if token != "":
                                tokens.append(token)
                            tokens.append(c)
                            token = ""
                            if len(tokens) < 2:
                                continue
                            last_two = tokens[-2:]
                            if last_two == ['/', '/']: #single-line comment
                                tokens = tokens[:-2]
                                mode = 3
                            elif last_two == ['/', '*']: #multi-line comment
                                tokens = tokens[:-2]
                                mode = 4
                        else:
                            token += c

                    case 1: #newline, counting the indentation of the line, always append an empty token in this state
                        if c == " ": #more spaces
                            token += " "
                        elif c == "\n": #sudden end of line, throw away the current token
                            token = ""
                        elif c in grouping_symbols: #start a group
                            tokens.append(token)
                            token = ""
                            group = c
                            mode = 2
                        elif c in enclosing_symbols or c in operator_symbols:
                            tokens.append(token)
                            tokens.append(c)
                            token = ""
                            mode = 0
                            if len(tokens) < 2:
                                continue
                            last_two = tokens[-2:]
                            if last_two == ['/', '/']: #single-line comment
                                tokens = tokens[:-2]
                                mode = 3
                            elif last_two == ['/', '*']: #multi-line comment
                                tokens = tokens[:-2]
                                mode = 4
                        else: #found something that takes us out of this mode
                            tokens.append(token)
                            token = c
                            mode = 0

                    case 2: #grouping
                        if group == c: #end the group
                            tokens.append(c + token + c)
                            token = ""
                            mode = 0
                        elif c == "\n": #newline inside of a group, probably invalid syntax, change this later if wrong
                            #to further explain, we reach here if we use python-like multiline comments '''like this'''
                            raise Exception("invalid syntax")
                            #print("HERE")
                            #tokens.append("#######")
                        else:
                            token += c

                    case 3: #single-line comment
                        if c == '\n':
                            if len(tokens) > 0 and tokens[-1] != '\n':
                                tokens.append("\n")
                            mode = 1

                    case 4: #multi-line comment
                        if c == '*':
                            token = '*'
                        elif c == '/' and token == '*': #end the comment
                            if len(tokens) > 0 and tokens[-1] == '\n': #remove redundant newline
                                tokens = tokens[:-1]
                            token = ""
                            mode = 0


        if mode in [0, 1]: #after finishing the file, we still have a token left over
            tokens.append(token)
        elif mode in [2, 4]: #should not be in these states once we finish the file
            raise Exception("invalid syntax")

        # final whitespace cleanup at start and end
        #if len(tokens) > 1 and tokens[0].strip() == '' and tokens[1] == '\n':
        while len(tokens) > 1 and tokens[0].strip() == '' and tokens[1] == '\n':
            tokens = tokens[2:]
        #if len(tokens) > 1 and tokens[-1].strip() == '' and tokens[-2] == '\n':
        while len(tokens) > 1 and tokens[-1].strip() == '' and tokens[-2] == '\n':
            tokens = tokens[:-2]

    return tokens


def parse(tokens: list[str]) -> None:
    pass


def main() -> None:
    """Main entry point."""
    aparser = argparse.ArgumentParser(
            prog = "corvus",
            )
    # non-positional
    aparser.add_argument("-V", "--version", action = "version", version = "%(prog)s 0.1")

    # required
    aparser.add_argument("<FILE>", help = "input file")

    # optional
    aparser.add_argument("-l", "--lang", action = "store", choices = ["python"], default = "python", help = "output language")
    aparser.add_argument("-o", "--output", action = "store", dest = "<OUT>", help = "output file")

    args = vars(aparser.parse_args())

    #print(args)
    #print(args["lang"])
    #print(args["<FILE>"])
    #print(args["<OUT>"])
    #print(args["lang"])


    #tokens = tokenize(input_file)
    #print(tokens)

    if not os.path.isfile(args["<FILE>"]):
        print(f"Error: file \"{args['<FILE>']}\" does not exist")
        return

    print("Tokenizing...")
    tokens = tokenize(args["<FILE>"])
    print(tokens)

if __name__ == "__main__":
    main()

