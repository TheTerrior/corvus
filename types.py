from typing import Any, Self
from dataclasses import dataclass



'''

BASE

'''


@dataclass
class Instruction:
    """Base class for any instruction."""


@dataclass
class Statement(Instruction):
    """Base class for any statement."""


@dataclass
class Expression(Instruction):
    """Base class for any expression."""


@dataclass
class Operator:
    """Base class for all operators."""



'''

MAIN

'''


@dataclass
class Scope:
    """Contains a scope."""
    level: int
    instructions: list[Instruction]


@dataclass
class Module:
    """Base class for imports and includes."""
    module: str


@dataclass
class Import(Module):
    """Imports an external module."""


@dataclass
class Include(Module):
    """Includes a local file or module."""


@dataclass
class MainScope:
    """Outer container for the AST."""
    modules: list[Module]
    scope: Scope



'''

INTERNAL

'''


@dataclass
class Assignment(Statement):
    """Base class for assignments."""


@dataclass
class FunctionAssignment(Assignment):
    """Assign a function to a variable."""


@dataclass
class ValueAssignment(Assignment):
    """Assign a value to a variable."""


@dataclass
class Return(Statement):
    """A return statement."""


@dataclass
class Pass(Statement):
    """A pass statement."""


@dataclass
class Break(Statement):
    """A break statement."""


@dataclass
class CompoundExpression(Expression):
    """An expression resultant from other expressions."""
    expressions: list[Expression | Operator]




'''

VALUES

'''


@dataclass
class Value(Expression):
    """Base class for values."""


@dataclass
class Bool(Value):
    """Boolean."""
    value: bool


@dataclass
class Int(Value):
    """Int."""
    value: int


@dataclass
class Int8(Value):
    """Int8."""
    value: int


@dataclass
class Int16(Value):
    """Int16."""
    value: int


@dataclass
class Int32(Value):
    """Int32."""
    value: int


@dataclass
class Int64(Value):
    """Int64."""
    value: int

@dataclass
class UInt8(Value):
    """UInt8."""
    value: int


@dataclass
class UInt16(Value):
    """UInt16."""
    value: int


@dataclass
class UInt32(Value):
    """UInt32."""
    value: int


@dataclass
class UInt64(Value):
    """UInt64."""
    value: int


@dataclass
class Float32(Value):
    """Float32."""
    value: float


@dataclass
class Float64(Value):
    """Float64."""
    value: float


@dataclass
class Char(Value):
    """Char."""
    value: str


@dataclass
class Rune(Value):
    """Rune."""
    value: str


@dataclass
class String(Value):
    """String."""
    value: str


#TODO
#@dataclass
#class List(Value):



'''

OPERATORS

'''


@dataclass
class Addition(Operator):
    """Addition."""


@dataclass
class Subtraction(Operator):
    """Subtraction."""


@dataclass
class Multiplication(Operator):
    """Multiplication."""


@dataclass
class Division(Operator):
    """Division."""


#TODO modulus and other things



'''

BLOCKS

'''


@dataclass
class Block:
    """Groups instructions together without impacting variable scope."""
    instructions: list[Instruction]


@dataclass
class IfConditional(Statement):
    """An if statement."""
    condition: Bool | CompoundExpression
    block: Block


@dataclass
class ElifConditional(Statement):
    """An elif statement."""
    condition: Bool | CompoundExpression
    block: Block


@dataclass
class ElseConditional(Statement):
    """An else statement."""
    block: Block


@dataclass
class WhileLoop(Statement):
    """A while loop."""
    condition: Bool | CompoundExpression
    block: Block


#TODO
#@dataclass
#class ForLoop(Statement):
#    condition


@dataclass
class Loop(Statement):
    """A normal loop."""
    block: Block









