from dataclasses import dataclass
from typing import Iterator
from enum import IntEnum
from ast_nodes import *
import tokenizer


class ParseError(IntEnum):
    BigBad = -1  #reserved for reaching unreachable code
    Ok = 0
    BadIndentation = 1
    BadImport = 2
    BadInclude = 3
    WeirdScope = 4
    BadSyntax = 5

class Mode(IntEnum):
    FindImports = 0
    Scope = 1
    Definition = 2


@dataclass
class Fakerator:
    tokens: list[str]
    position: int

    def get_line(self) -> list[str]:
        """Returns the next line in the iterator."""
        accum = []

        while self.position < len(self.tokens) - 1:
            st = self.tokens[self.position]
            if st == '\n':
                accum.append(st)
                self.position += 1
                return accum
            elif st.strip() == "":  #handle indentation
                self.position += 1
                continue
            else:
                accum.append(st)
                self.position += 1
        return accum


    def get_line_str(self) -> str:
        """Returns the next line in the iterator as a string."""
        accum = ""

        while self.position < len(self.tokens) - 1:
            st = self.tokens[self.position]
            if st == '\n':
                self.position += 1
                return accum + st
            elif st.strip() == "":  #handle indentation
                self.position += 1
                continue
            else:
                accum += st
                self.position += 1
        return accum

    def peak_line_tokens(self) -> list[str]:
        """Returns the next line in the iterator without altering the Fakerator."""
        accum = []
        pos = self.position

        while self.position < len(self.tokens) - 1:
            st = self.tokens[pos]
            if st == '\n':
                accum.append(st)
                pos += 1
                return accum
            elif st.strip() == "":  #handle indentation
                pos += 1
                continue
            else:
                accum.append(st)
                pos += 1
        return accum

    def peak_line_tokens_indentation(self) -> list[str]:
        """Returns the next line in the iterator (including the indentation) without altering the Fakerator."""
        accum = []
        pos = self.position

        while self.position < len(self.tokens) - 1:
            st = self.tokens[pos]
            if st == '\n':
                accum.append(st)
                pos += 1
                return accum
            else:
                accum.append(st)
                pos += 1
        return accum

    def peak_line_str(self) -> str:
        """Returns the next line in the iterator as a string without altering the Fakerator."""
        accum = ""
        pos = self.position

        while self.position < len(self.tokens) - 1:
            st = self.tokens[pos]
            if st == '\n':
                pos += 1
                return accum + st
            elif st.strip() == "":  #handle indentation
                pos += 1
                continue
            else:
                accum += st
                pos += 1
        return accum

    def peak_rest_tokens(self) -> list[str]:
        """Returns the rest of the tokens without altering the Fakerator."""
        return self.tokens[self.position:]


def parse(tokens: list[str]) -> tuple[int, MainScope | str]:
    """Turns a list of tokens into an abstract syntax tree."""
    if tokens[0] != "":
        return (ParseError.BadIndentation, "")

    it = Fakerator(tokens, 0)

    #handle import statements here
    imports: list[Import] = []
    includes: list[Include] = []
    res = parse_modules(it, imports, includes)
    if res[0] != ParseError.Ok:
        return (res[0], res[1])  #found an error

    #handle recursive scopes here
    res = parse_recursive(it)
    if res[0] == 0 and isinstance(res[1], Scope):
        main = MainScope(res[1].level, res[1].instructions, imports, includes)
        return (ParseError.Ok, main)
    elif isinstance(res[1], str):  #found an error
        return (res[0], res[1])

    # unreachable
    return (ParseError.BigBad, "big bad things happened, reached unreachable point after recursive parsing")


def parse_modules(it: Fakerator, imports: list[Import], includes: list[Include]) -> tuple[int, MainScope | str]:
    """Parses module imports and includes."""
    while True:
        line = it.peak_line_tokens()[:-1]
        if len(line) < 2:
            break

        match line[0]:
            case "import":
                pass
            case "include":
                pass
            case _:
                break

        # import math::pi  //length 5
        # import random    //length 2
        # import example::examplething::finallythis   //length 8

        module_name = []
        
        # ensure correct length
        if (len(line) - 2) % 3 != 0:
            if line[0] == "import":
                return (ParseError.BadImport, "")
            else:
                return (ParseError.BadInclude, "")
        
        # ensure first module name is valid
        res = True
        for char in line[1]:
            res = True and char not in [tokenizer.grouping_symbols, tokenizer.operator_symbols, tokenizer.enclosing_symbols]
            if not res:
                break

        if not res:  #invalid token found for a module name
            return (ParseError.BadImport, "")
        else:
            module_name.append(line[1])

        # check each remaining module name
        left = line[2:]
        while len(left) > 0:
            chunk = left[:3]
            left = left[3:]

            # check colons
            if chunk[0] != ':' or chunk[1] != ':':
                if line[0] == "import":
                    return (ParseError.BadImport, "")
                else:
                    return (ParseError.BadInclude, "")

            # check module name
            res = True
            for char in chunk[2]:
                res = True and char not in [tokenizer.grouping_symbols, tokenizer.operator_symbols, tokenizer.enclosing_symbols]
                if not res:
                    break

            if not res:  #invalid token found for a module name
                if line[0] == "import":
                    return (ParseError.BadImport, "")
                else:
                    return (ParseError.BadInclude, "")
            else:
                module_name.append(chunk[2])

        # passed all the verification checks, convert into usable node
        if line[0] == "import":
            imports.append(Import(module_name))
        else:
            includes.append(Include(module_name))
        
        #print("here", it.peak_rest_tokens())
        it.get_line()  #consume the next line

    # unreachable
    #return (ParseError.BigBad, "big bad things happened, reached unreachable point while parsing modules")
    return (ParseError.Ok, "")


def parse_recursive(it: Fakerator) -> tuple[int, Scope | str]:
    """Recursive implementation of parsing."""
    line = it.peak_line_tokens()
    if len(line) == 0:
        return (ParseError.WeirdScope, "ran into some strange scoping problems")
    scope = Scope(len(line[0]), [])
    #print("in recursive")
    #print(f"level: {level}")
    #print(it.peak_line_tokens())
    #print(it.peak_line_str())

    mode: int = Mode.Scope  #start at default mode
    while True:
        line = it.peak_line_tokens()
        match mode:
            case Mode.Scope:  #looking for the next course of action, no current action
                #print("made it here correctly")
                #print(it.peak_rest_tokens())
                if len(line[0]) != scope.level:
                    return (ParseError.BadIndentation, "detected an invalid sudden change of indentation")
                elif len(line) > 3 and line[1] == "let":  #declaration
                    if line[3] == ':': #value declaration
                        scope.instructions.append(ValueAssignment(TypedVariable(line[2], line[4]), PlaceholderExpression()))  #DEBUG, need to recursively deduce statement
                    elif line[3] == '(':  #function declaration   )
                        scope.instructions.append(FunctionAssignment(Variable(line[2]), AssignmentTuple([]), Scope(len(line[0]), [])))  #DEBUG, need to find type
                    else:
                        return (ParseError.BadSyntax, "invalid syntax after a 'let' statement")
                #elif line[1] == "if":
                #    pass
                #elif line[1] == "elif":
                #    pass
                #elif line[1] == "else":
                #    pass
                #elif line[1] == "while":
                #    pass
                #elif line[1] == "struct":
                #    pass
                #elif line[1] == "match":
                #    pass
                elif line[1] == "import" or line[1] == "include":
                    return (ParseError.BadSyntax, "invalid syntax, import and include statements should be at the top of the file")
                elif len(line) > 2 and line[2] == "=":  #assignment
                    pass
                else:  #expression
                    pass


                pass
            case _:
                return (ParseError.BigBad, "big bad things happened, reached unreachable point while recursively parsing")
        break


    return (0, scope)


def verify_ast(tree: MainScope) -> tuple[int, str]:
    """Takes a newly created AST and ensures it's valid."""
    return (0, "")


