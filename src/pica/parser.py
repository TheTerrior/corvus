#from dataclasses import dataclass
#from re import T
from typing import Iterator, Any
from enum import IntEnum

#import sys
#sys.path.append("..")
#
#from tools import *


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


#def parse() -> Result[Any, str]




