from typing import Iterable
from enum import IntEnum
from ast_nodes import *


class ParseError(IntEnum):
    BigBad = -1  #reserved for reaching unreachable code
    Ok = 0
    BadIndentation = 1

class Mode(IntEnum):
    FindImports = 0
    Scope = 1
    Definition = 2


def parse(tokens: list[str]) -> tuple[int, MainScope | str]:
    """Turns a list of tokens into an abstract syntax tree."""
    if tokens[0] != "":
        return (ParseError.BadIndentation, "")

    '''handle imports here'''
    modules = []

    it = iter(tokens)
    res = parse_recursive(it, 0)
    if res[0] == 0 and isinstance(res[1], Scope):
        main = MainScope(res[1].level, res[1].instructions, modules)
        return (ParseError.Ok, main)
    elif isinstance(res[1], str):
        return (res[0], res[1])

    # unreachable
    return (ParseError.BigBad, "big bad things happened, reached unreachable point")


def parse_recursive(it: Iterable[str], level: int) -> tuple[int, Scope | str]:
    """Recursive implementation of parsing."""
    scope = Scope(level, [])
    return (0, scope)


def verify_ast(tree: MainScope) -> tuple[int, str]:
    """Takes a newly created AST and ensures it's valid."""
    return (0, "")


