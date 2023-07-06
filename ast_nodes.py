#from typing import Any, Self
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
    module: list[str]


@dataclass
class Import(Module):
    """Imports a standard or third-party module."""


@dataclass
class Include(Module):
    """Includes a local file or module."""



'''

VALUES

'''


@dataclass
class CompoundExpression(Expression):
    """An expression resultant from other expressions."""
    #expressions: list[Expression | Operator]
    operator: Operator
    operands: list[Expression]


@dataclass
class Value(Expression):
    """Base class for values."""


@dataclass
class Bool(Value):
    """Boolean."""
    value: bool | CompoundExpression


@dataclass
class Int(Value):
    """Int."""
    value: int | CompoundExpression


@dataclass
class Int8(Value):
    """Int8."""
    value: int | CompoundExpression


@dataclass
class Int16(Value):
    """Int16."""
    value: int | CompoundExpression


@dataclass
class Int32(Value):
    """Int32."""
    value: int | CompoundExpression


@dataclass
class Int64(Value):
    """Int64."""
    value: int | CompoundExpression


@dataclass
class UInt8(Value):
    """UInt8."""
    value: int | CompoundExpression


@dataclass
class UInt16(Value):
    """UInt16."""
    value: int | CompoundExpression


@dataclass
class UInt32(Value):
    """UInt32."""
    value: int | CompoundExpression


@dataclass
class UInt64(Value):
    """UInt64."""
    value: int | CompoundExpression


@dataclass
class Float32(Value):
    """Float32."""
    value: float | CompoundExpression


@dataclass
class Float64(Value):
    """Float64."""
    value: float | CompoundExpression


@dataclass
class Char(Value):
    """Char."""
    value: str | CompoundExpression


@dataclass
class Rune(Value):
    """Rune."""
    value: str | CompoundExpression


@dataclass
class String(Value):
    """String."""
    value: str | CompoundExpression


@dataclass
class Tuple(Value):
    """Tuple."""
    values: list[Value | CompoundExpression]


@dataclass
class List(Value):
    """List."""
    values: list[Value | CompoundExpression]



'''

ASSIGNMENT

'''


@dataclass
class PlaceholderExpression(Expression):
    """For development, and for uninitialized variables."""


@dataclass
class Variable(Expression):
    """Class for variables."""
    name: str


@dataclass
class TypedVariable(Variable):
    """Class for typed variables (optional for assignments if type can be inferenced, or for parameters)"""
    var_type: str


@dataclass
class VariableDeclaration(Statement):
    """Declares or shadows a variable."""
    variable: Variable | TypedVariable


@dataclass
class ParameterTuple:
    """Holds a list of parameters."""
    variables: list[TypedVariable]


@dataclass
class AssignmentTuple:
    """Holds a list of variables for assignment."""
    variables: list[Variable | TypedVariable]


@dataclass
class Assignment(Statement):
    """Base class for assignments."""


@dataclass
class FunctionAssignment(Assignment):
    """Assign a function to a variable."""
    var: Variable | TypedVariable 
    parameters: ParameterTuple
    value: Scope


@dataclass
class ValueAssignment(Assignment):
    """Assign a value to a variable."""
    var: Variable
    value: Expression


@dataclass
class Return(Statement):
    """A return statement."""


@dataclass
class Pass(Statement):
    """A pass statement."""


@dataclass
class Break(Statement):
    """A break statement."""



'''

AAAAAAAAAAAAAAAA

'''


@dataclass
class MainScope(Scope):
    """Outer container for the AST."""
    imports: list[Import]
    includes: list[Include]
    globals: list[TypedVariable]


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









