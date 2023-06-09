import os
import argparse
from typing import Any


grouping_symbols = {"'", '"'}
enclosing_symbols = {'(', '{', '['} #) } ]
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
            mode = 1 #start by counting the indentation of this line
            token = "" #holds the current token
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
                        elif c == ":":
                            if token != "":
                                tokens.append(token)
                            tokens.append(":")
                            token = ""
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
                        else: #found something that takes us out of this mode
                            tokens.append(token)
                            token = c
                            mode = 0

                    case 2: #grouping
                        if group == c: #end the group
                            tokens.append(c + token + c)
                            token = ""
                            mode = 0
                        elif c == "\n": #probably invalid syntax, change this later if wrong
                            raise Exception("invalid syntax")
                        else:
                            token += c

        if mode in [0, 1]: #after finishing the file, we still have a token left over
            tokens.append(token)
        elif mode in [2]: #should not be in these states once we finish the file
            raise Exception("invalid syntax")

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

