import tools

symbols = {'+', '-', '*', '/', '\\', '%', '=', '>', '<', '|', '&', '.', ',', ':', ';', '!', '?', '^', '$', '(', ')', '{', '}', '[', ']', '"', "'", '@', '#'}

def tokenize(input_file: str) -> tools.Result[list[tuple[int, int, list[str]]], str]:
    """Tokenizes the input file. All languages are tokenized the same way."""
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

            if len(line.strip()) == 0: #whole line remove by comments
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
    




