import tools
from functools import reduce

grouping_symbols = {"'", '"'}
enclosing_symbols = {'(', ')', '{', '}', '[', ']'}
operator_symbols = {'+', '-', '*', '/', '%', '=', '>', '<', '|', '&', '.', ':', '!', ',', '^', '$'}

symbols = {'+', '-', '*', '/', '\\', '%', '=', '>', '<', '|', '&', '.', ',', ':', ';', '!', '?', '^', '$', '(', ')', '{', '}', '[', ']', '"', "'", '@', '#'}

def tokenize(input_file: str) -> tools.Result[list[str], str]:
    """Tokenizes the input file. All languages are tokenized the same way."""
    global grouping_symbols, enclosing_symbols, operator_symbols

    tokens: list[str] = [] #holds all tokens
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
                                tokens.append(token)
                            token = ""
                        elif c == "\n": #switch mode
                            if token != "":
                                tokens.append(token)
                            tokens.append("\n")
                            token = ""
                            mode = 1
                        elif c in grouping_symbols: #start a group
                            if token != "":
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
                            #return tools.Result("invalid syntax", False)
                            return tools.err("invalid syntax")
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
            tools.err("invalid syntax")

        # double newline cleanup, O(n) but simplifies processes later, will be incorporated into main lexer later
        level = 0
        length_const = len(tokens) - 1
        cap = len(tokens)
        i = 0
        while i < cap:
            if tokens[i].strip() == "" and i < length_const and tokens[i+1] == '\n' and len(tokens[i]) == level: #found an indentation token
                tokens.pop(i)
                tokens.pop(i)
                cap -= 2
                length_const -= 2
            i += 1

        # final whitespace cleanup, remove all useless newlines at end
        while len(tokens) > 1 and tokens[-1].strip() == '' and tokens[-2] == '\n':
            tokens = tokens[:-2]

    return tools.ok(tokens)


def tokenize_new(input_file: str) -> tools.Result[list[tuple[int, int, list[str]]], str]:
    global symbols

    all_tokens: list[tuple[int, int, list[str]]] = [] #holds all tokens, [line_number, indentation, tokens]
    line_number = 1
    in_comment = False #inside of a multiline comment
    multiline_start = 0 #starting index of multiline comment

    with open(input_file, "r") as file:
        while (line := file.readline()) != "": #iterate through every line
            tokens: list[str] = []
            token: str = ""

            # remove comments
            while True:
                if in_comment: #currently inside a multiline
                    if loc := line.find("$$") != -1: #found end to multiline comment
                        line = line[loc+2:] #remove multiline comment
                        in_comment = False
                    else: #no end to multiline
                        break

                loc_m = line.find("??")
                loc_s = line.find("//")
                if loc_s != -1 or loc_m != -1: #found some comment, ordered purposefully to exit condition sooner
                    if loc_s != -1 and (loc_m == -1 or loc_s < loc_m): #remove single-line comment
                        line = line[:loc_s]
                    #elif loc_m != -1 and (loc_s == -1 or loc_m < loc_s): #remove multiline comment
                    else: #remove multiline comment
                        sub = line[loc_m+2:] #get the end of line substring
                        loc_u = sub.find("$$") #check for a multiline end
                        if loc_u != -1: #end of multiline found
                            line = line[:loc_m] + line[loc_u+2:]
                        else: #multiline is multi-line
                            in_comment = True
                            multiline_start = line_number
                            line = line[:loc_m]
                            break #no more comments after this

                else: #no comments found
                    break

            if len(line) == 0: #whole line remove by comments
                line_number += 1
                continue

            # count indentation
            counter = 0 #how many spaces there are
            for c in line:
                if c == ' ':
                    counter += 1
                else:
                    break
            if counter % 4 != 0: #invalid number of indents
                return tools.err(f"invalid indentation on line {line_number}")
            indentation = counter // 4
            line = line.strip() #remove indentation

            # tokenize line
            for c in line:
                if c == " ":
                    if token != "":
                        tokens.append(token)
                        token = ""
                    else:
                        continue
                elif c not in symbols: #normal symbol
                    token += c
                else: #reserved symbol
                    if token != "":
                        tokens.append(token)
                        token = ""
                    tokens.append(c)
            if token != "":
                tokens.append(token)

            all_tokens.append((line_number, indentation, tokens))
            line_number += 1
    
    if in_comment:
        return tools.err(f"unclosed multiline comment starting at line {multiline_start}")

    return tools.ok(all_tokens)
    




