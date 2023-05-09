import sys


#grouping_symbols = {
#    #"(": ")",
#    #"{": "}",
#    #"[": "]",
#    "'": "'",
#    '"': '"',
#}

grouping_symbols = {"'", '"'}


def tokenize(input_file: str) -> list[str]:
    """Tokenizes the input file. All languages are tokenized the same way."""
    global grouping_symbols

    tokens = [] #holds all tokens
    group = None
    with open(input_file, "r") as file:
        while (line := file.readline()) != "": #iterate through every line
            #line = line_raw[:-1] #skip the newline

            token = "" #holds the current token
            for c in line:
                #print(c)
                #tokens.append(c)
                if group == None: #not in a group yet
                    if c in grouping_symbols: #start a group
                        group = c
                        token += c
                        continue
                    elif c == "\n": #new line
                        tokens.append(token)
                        token = ""
                        continue
                else: #in a group
                    if group == c: #ending a group
                        group = None
                        tokens.append(token + c)
                        token = ""
                        continue
                    elif c == "\n": #in a group, yet reached a newline
                        raise Exception("invalid syntax")

                if c == " ": #start a new token
                    tokens.append(token)
                    token = ""
                else: #just append, while remaining in the group
                    token += c

    return tokens


def main() -> None:
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Didn't receive exactly 2 arguments!")
        return 

    input_file = sys.argv[1]
    tokens = tokenize(input_file)
    print(tokens)


if __name__ == "__main__":
    main()

