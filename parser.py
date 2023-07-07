from dataclasses import dataclass
from re import T
from typing import Iterator
from enum import IntEnum
from ast_nodes import *
from tools import *
import tokenizer


class ParseError(IntEnum):
    BigBad = -1  #reserved for reaching unreachable code
    Ok = 0
    BadIndentation = 1
    BadImport = 2
    BadInclude = 3
    WeirdScope = 4
    BadSyntax = 5
    BadGlobal = 6
    BadModuleName = 7
    BadVariableName = 8

class Mode(IntEnum):
    FindImports = 0
    Scope = 1
    Definition = 2


@dataclass
class Fakerator:
    tokens: list[str]
    position: int

    def get_line(self) -> list[str]:
        """Returns the next line in the iterator, mostly used to consume the next line after peaking."""
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
        """Returns the next line in the iterator (not including indentation) as a string."""
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
        """Returns the next line in the iterator (not including indentation) without altering the Fakerator."""
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
        """Returns the next line in the iterator (not including indentation) as a string without altering the Fakerator."""
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

    #handle global declarations here
    globals: list[TypedVariable] = []
    res = parse_globals(it, globals)
    if res[0] != ParseError.Ok:
        return (res[0], res[1])  #found an error

    #handle recursive scopes here
    rec_res = parse_recursive(it)
    if res[0] == 0 and isinstance(rec_res[1], Scope):
        main = MainScope(0, rec_res[1].instructions, imports, includes, globals)
        return (ParseError.Ok, main)
    elif isinstance(rec_res[1], str):  #found an error
        return (rec_res[0], rec_res[1])

    # unreachable
    return (ParseError.BigBad, "big bad things happened, reached unreachable point after recursive parsing")


def parse_modules(it: Fakerator, imports: list[Import], includes: list[Include]) -> tuple[int, MainScope | str]:
    """Parses module imports and includes."""
    while True:
        line = it.peak_line_tokens()[:-1]
        if len(line) < 2 or line[0] not in ["import", "include"]:
            break

        # import math::pi  //length 5
        # import random    //length 2
        # import example::examplething::finallythis   //length 8

        module_name = []
        
        # ensure correct length
        if (len(line) - 2) % 3 != 0:
            if line[0] == "import":
                return (ParseError.BadImport, "Incorrect syntax for an import statement")
            else:
                return (ParseError.BadInclude, "Incorrect syntax for an include statement")
        
        # ensure first module name is valid
        res = True
        for char in line[1]:
            if char in [tokenizer.grouping_symbols, tokenizer.operator_symbols, tokenizer.enclosing_symbols]:
                res = False
                break

        if not res:  #invalid token found for a module name
            return (ParseError.BadModuleName, "Attempted to import module with an invalid name")
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


def parse_globals(it: Fakerator, globals: list[TypedVariable]) -> tuple[int, str]:
    """Parses module imports and includes."""
    while True:
        line = it.peak_line_tokens()[:-1]
        if len(line) < 2 or line[0] != "global":  #global x: int, stop iterating when we don't run into a global statement
            break

        # import math::pi  //length 5
        # import random    //length 2
        # import example::examplething::finallythis   //length 8

        # ensure correct length
        if len(line) != 4 or line[2] != ":":
            return (ParseError.BadGlobal, "Incorrect syntax for a global declaration")
        
        # ensure variable name and type is valid
        res = True
        for char in (line[1] + line[3]):
            if char in [tokenizer.grouping_symbols, tokenizer.operator_symbols, tokenizer.enclosing_symbols]:
                res = False
                break

        if not res:  #invalid token found for a module name
            return (ParseError.BadVariableName, "Tried to utilize a variable or type with an invalid name")

        # passed all the verification checks, convert into usable node
        if line[0] == "global":
            globals.append(TypedVariable(line[1], line[3]))
        
        #print("here", it.peak_rest_tokens())
        it.get_line()  #consume the next line

    return (ParseError.Ok, "")



def parse_expression(tokens: list[str]) -> tuple[int, Expression | str]:  #TODO
    """Parses an expression into a tree."""
    '''
    Hierarchy of precedence

    () []
    . $ function_call
    !
    **
    * / // %
    + -
    << >>
    &
    ^
    |
    < > <= >= == !=
    &&
    ||
    '''
    return (ParseError.Ok, PlaceholderExpression())


def parse_parameters(tokens: list[str]) -> tuple[int, list[TypedVariable] | str]:
    """Parses a set of parameters."""
    variables: list[TypedVariable] = []
    pos = 0
    while pos < len(tokens):
        if not (tokens[pos+1] == ':' and (pos+3 >= len(tokens) or tokens[pos+3] == ',')):
            return (ParseError.BadSyntax, "Invalid parameter syntax")
        variables.append(TypedVariable(tokens[pos], tokens[pos+2]))
        pos += 4
    return (ParseError.Ok, variables)


def parse_recursive(it: Fakerator) -> tuple[int, Scope | str]:
    """Recursive implementation of parsing."""
    line = it.peak_line_tokens_indentation()
    print(f"line: {line}")
    if len(line) == 0:
        return (ParseError.WeirdScope, "ran into some strange scoping problems")
    scope = Scope(len(line[0]), [])

    mode: int = Mode.Scope  #start at default mode
    while True:
        line = it.peak_line_tokens_indentation()
        match mode:
            case Mode.Scope:  #looking for the next course of action, no current action
                print(line)
                if len(line[0]) != scope.level:
                    return (ParseError.BadIndentation, "detected an invalid sudden change of indentation")

                elif line[1] == "let":  #declaration
                    if len(line) < 4:  #for now blank declarations with type inference are disallowed: let x
                        return (ParseError.BadSyntax, "invalid syntax when declaring a variable")

                    if line[3] == ':':  #value declaration with type, let x: int = 5
                        if len(line) < 5:  #incorrect syntax
                            return (ParseError.BadSyntax, "invalid syntax when declaring a variable")

                        if len(line) > 5 and line[5] == '=':  #declaration with assignment
                            expression_tree_res = parse_expression(line[6:])  #recursively deduce assignment
                            if isinstance(expression_tree_res[1], str):
                                return (expression_tree_res[0], expression_tree_res[1])  #error while parsing expression
                            scope.instructions.append(VariableDeclaration(TypedVariable(line[2], line[4])))
                            scope.instructions.append(ValueAssignment(Variable(line[2]), expression_tree_res[1]))
                            it.get_line()
                        elif len(line) == 5: #declaration without assignment
                            scope.instructions.append(VariableDeclaration(TypedVariable(line[2], line[4])))
                            it.get_line()
                        else:
                            return (ParseError.BadSyntax, "invalid syntax when declaring a variable")

                    elif line[3] == '=':  #value declaration with type inference, let x = 5
                        expression_tree_res = parse_expression(line[4:])  #recursively deduce assignment
                        if isinstance(expression_tree_res[1], str):
                            return (expression_tree_res[0], expression_tree_res[1])  #error while parsing expression
                        scope.instructions.append(VariableDeclaration(Variable(line[2])))
                        scope.instructions.append(ValueAssignment(Variable(line[2]), expression_tree_res[1]))  #type inference will be done during semantic analysis
                        it.get_line()

                    #elif line[2] == '(':  #) assignment tuple, TODO
                    #    pass

                    elif line[3] == '(':  #function declaration ), let x(y: int, z: int): int =, let x() =
                        loc = find_parentheses_pair_tokens(line, 3)  #type declarations can have parentheses, i.e. tuples
                        if loc == -1 or len(line) < loc + 2:
                            return (ParseError.BadSyntax, "invalid syntax when declaring a function")

                        #from here there are two types of functions, those with return types and those without
                        if line[loc + 1] == ':':  #function with return type
                            if len(line) < loc + 4 or line[loc + 1] != ':' or line[loc + 3] != '=':
                                return (ParseError.BadSyntax, "invalid syntax when declaring a function")
                            func_type = line[loc + 2]

                            parameters_res = parse_parameters(line[4:loc])
                            if isinstance(parameters_res[1], str):
                                return (parameters_res[0], parameters_res[1])  #error while parsing expression

                            if len(line) > loc + 4:  #one-line definition, must be an expression
                                expression_tree_res = parse_expression(line[loc+4:])  #recursively deduce assignment
                                if isinstance(expression_tree_res[1], str):
                                    return (expression_tree_res[0], expression_tree_res[1])  #error while parsing expression

                                scope.instructions.append(VariableDeclaration(Variable(line[2])))  #will let semantic analysis figure out the type
                                scope.instructions.append(FunctionAssignment(TypedVariable(line[2], func_type), ParameterTuple(parameters_res[1]), Scope(scope.level+1, [expression_tree_res[1]])))
                                it.get_line()
                            else:  #multiple-line definition, recursion
                                it.get_line()
                                res = parse_recursive(it)
                                if isinstance(res[1], str):  #error
                                    return (res[0], res[1])
                                scope.instructions.append(VariableDeclaration(Variable(line[2])))  #will let semantic analysis figure out the type
                                scope.instructions.append(FunctionAssignment(TypedVariable(line[2], func_type), ParameterTuple(parameters_res[1]), res[1]))

                        else:  #function without return type
                            if line[loc + 1] != '=':
                                return (ParseError.BadSyntax, "invalid syntax when declaring a function")

                            parameters_res = parse_parameters(line[4:loc])
                            if isinstance(parameters_res[1], str):
                                return (parameters_res[0], parameters_res[1])  #error while parsing expression

                            if len(line) > loc + 2:  #one-line definition, must be an expression
                                expression_tree_res = parse_expression(line[loc+2:])  #recursively deduce assignment
                                if isinstance(expression_tree_res[1], str):
                                    return (expression_tree_res[0], expression_tree_res[1])  #error while parsing expression

                                scope.instructions.append(VariableDeclaration(Variable(line[2])))  #will let semantic analysis figure out the type
                                scope.instructions.append(FunctionAssignment(Variable(line[2]), ParameterTuple(parameters_res[1]), Scope(scope.level+1, [expression_tree_res[1]])))
                                it.get_line()
                            else:  #multiple-line definition, recursion
                                it.get_line()
                                res = parse_recursive(it)
                                if isinstance(res[1], str):  #error
                                    return (res[0], res[1])
                                scope.instructions.append(VariableDeclaration(Variable(line[2])))  #will let semantic analysis figure out the type
                                scope.instructions.append(FunctionAssignment(Variable(line[2]), ParameterTuple(parameters_res[1]), res[1]))

                    else:
                        return (ParseError.BadSyntax, "invalid syntax after a 'let' statement")

                elif line[1] == "drop":
                    pass
                elif line[1] == "import" or line[1] == "include":
                    return (ParseError.BadSyntax, "invalid syntax, import and include statements should be at the top of the file")
                elif line[1] == "global":
                    return (ParseError.BadSyntax, "invalid syntax, global statements should be at the top of the file under the import statements")
                elif len(line) > 2 and line[2] == "=":  #assignment, no declaration
                    it.get_line()
                    expression_tree_res = parse_expression(line[1:])  #recursively deduce assignment
                    if isinstance(expression_tree_res[1], str):
                        return (expression_tree_res[0], expression_tree_res[1])  #error while parsing expression
                    scope.instructions.append(ValueAssignment(Variable(line[1]), expression_tree_res[1]))
                    pass
                # have an elif case here that detects tuple assignments, first need to find an opening parentheses, closing, then equal operator right after, TODO
                else:  #expression
                    expression_tree_res = parse_expression(line[1:])  #recursively deduce assignment
                    if isinstance(expression_tree_res[1], str):
                        return (expression_tree_res[0], expression_tree_res[1])  #error while parsing expression
                    scope.instructions.append(expression_tree_res[1])  #append the expression to the scope

                '''
                not sure what's happening with indentation issues, but here's future things to implement:
                    elif line[1] == "if":                                                                                 
                        pass                                                                                              
                    elif line[1] == "elif":                                                                               
                        pass                                                                                              
                    elif line[1] == "else":                                                                               
                        pass                                                                                              
                    elif line[1] == "while":                                                                              
                        pass                                                                                              
                    elif line[1] == "struct":                                                                             
                        pass                                                                                              
                    elif line[1] == "match":                                                                              
                        pass
                '''

            case _:
                return (ParseError.BigBad, "big bad things happened, reached unreachable point while recursively parsing")
        break

    return (0, scope)


def verify_ast(tree: MainScope) -> tuple[int, str]:
    """Takes a newly created AST and ensures it's valid."""
    return (0, "")


