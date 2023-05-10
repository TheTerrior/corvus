import sys
from typing import Any
from dataclasses import dataclass


#grouping_symbols = {
#    #"(": ")",
#    #"{": "}",
#    #"[": "]",
#    "'": "'",
#    '"': '"',
#}


grouping_symbols = {"'", '"'}


@dataclass
class Node:
    """Struct for structing an abstract syntax tree."""
    token: str | None
    values: list[Any]


def tokenize1(input_file: str) -> list[str]:
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
                            #tokens.append("MODE1")
                            tokens.append(token)
                            token = ""
                            group = c
                            mode = 2
                        else: #found something that takes us out of this mode
                            #tokens.append("MODE1")
                            tokens.append(token)
                            token = c
                            mode = 0

                    case 2: #grouping
                        if group == c: #end the group
                            #tokens.append("MODE2")
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
                



def tokenize(input_file: str) -> list[str]:
    """Tokenizes the input file. All languages are tokenized the same way."""
    global grouping_symbols

    tokens = [] #holds all tokens
    group = None
    with open(input_file, "r") as file:

        mode = 1 #0 = neutral, 1 = newline
        while (line := file.readline()) != "": #iterate through every line
            #line = line_raw[:-1] #skip the newline

            token = "" #holds the current token
            for c in line:

                #handle groups
                if group == None: #not in a group yet
                    if c in grouping_symbols: #start a group
                        group = c
                        token += c
                        continue
                    elif c == "\n": #new line
                        if token != "":
                            tokens.append(token)
                        tokens.append("\n")
                        token = ""
                        continue
                else: #in a group
                    if group == c: #ending a group
                        if token != "":
                            tokens.append(token + c)
                        token = ""
                        group = None
                        continue
                    elif c == "\n": #in a group, yet reached a newline
                        raise Exception("invalid syntax")

                #handle normal cases
                if c == " ": #start a new token
                    if mode == 1 and (len(tokens) == 0 or tokens[-1] == "\n"): #handle indentation
                        token += " "
                        continue

                    #last token was not special
                    if token != "":
                        tokens.append(token)
                    token = ""
                elif c == ":":
                    if token != "":
                        tokens.append(token)
                    token = ":"
                elif c == "=":
                    if token != "":
                        tokens.append(token)
                    tokens.append("=")
                    token = ""
                else: #just append, while remaining in the group
                    token += c

    return tokens


def parse() -> None:

    pass


def main() -> None:
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Didn't receive exactly 2 arguments!")
        return 

    input_file = sys.argv[1]
    #tokens = tokenize(input_file)
    #print(tokens)
    tokens = tokenize1(input_file)
    print(tokens)

if __name__ == "__main__":
    main()

