





/// Used in type signatures
pub enum StandardType {
    I8,
    I16,
    I32,
    I64,
    U8,
    U16,
    U32,
    U64,
    F32,
    F64,
    B8,
    B16,
    B32,
    B64,
    Bool,
    Char,
    String,
    Rune,
    Chain,
    List(Box<StandardType>), // [type]
    Map(Box<(StandardType, StandardType)>), // <type, type>
    Set(Box<StandardType>), // {type}
    Tuple(Vec<StandardType>), // (type, type, ..)
    Variable(String), //structs and enums, must include name
    Function(Vec<StandardType>, Box<StandardType>), //parameters and return value, |type, type, .., type|
}




pub enum Variable {
    Variable(String),
    Index(String, Box<Expression>), //could be a list, dictionary, etc
    Ref(Box<Variable>),
    Curry(Box<Variable>),
}


pub struct FunctionCall {
    name: Variable,
    arguments: Vec<Expression>,
}


/// Don't inherit from this, use ValueWrapper instead
pub enum Value {
    Variable(Variable), //starts with alpha
    Bool(bool), //based on rich tokenizer
    Integer(String), //starts with int, has only ints and underscores
    Float(String), //starts with int, has ints and underscores and decimal
    Bits(String), //starts with 0b, has no decimals or underscores, respects rules
    Hex(String), //starts with 0x, has no decimals or underscores, respects rules
    Char(String), //no dollar precursor
    String(String), //no dollar precursor
    Rune(String), //dollar precursor
    Chain(String), //dollar precursor
}


/// Don't inherit from this, use TypeWrapper instead
pub enum BaseType {
    VarI8,
    VarI16,
    VarI32,
    VarI64,
    VarU8,
    VarU16,
    VarU32,
    VarU64,
    VarF32,
    VarF64,
    VarBool,
    VarChar,
    VarStr,
    VarRune,
    VarChain,
}


///// Things that are operated on
//pub enum ValueWrapper {
//    Value(Value),
//    Curry(Value),
//    Ref(Value),
//    Index(Value, Box<Expression>),
//}


/// Things that could fit in type declaration
pub enum TypeWrapper {
    BaseType(BaseType),
    CustomType(String),
    Ref(Box<TypeWrapper>),
    List(Box<TypeWrapper>),
    Tuple(Vec<TypeWrapper>),
    Dictionary(Box<TypeWrapper>, Box<TypeWrapper>),
    Set(Box<TypeWrapper>),
    Array(String, Box<TypeWrapper>), //size, type
}


pub enum OperationName {
    Add,
    Sub,
    Mult,
    Div,
    Mod,
    Exp,

    LT,
    GT,
    LEqT,
    GEqT,
    NEqT,
    EqT,

    Band,
    Bor,
    ShiftL,
    ShiftR,

    Not,
    And,
    Or,
    Xor,

    Range,
    RangeEq,

    Pipe,
    Concat,
    Cons,
}


/// CORE
pub enum Expression {
    Value(Value),
    Operation(Box<Operation>),
    FunctionCall(FunctionCall),
}


pub struct Operation {
    operation: OperationName,
    operand0: Expression,
    operand1: Expression,
}


pub enum AssignmentName {
    Eq,
    SumEq,
    SubEq,
    MultEq,
    DivEq,
    ModEq,
    ExpEq,
    BandEq,
    BorEq,
    XorEq,
    ShiftLEq,
    ShiftREq,
    ConcatEq,
}


pub enum DeclarationType {
    None,
    Let,
    Var,
    Const,
}


/// CORE
pub struct Assignment {
    declaration: DeclarationType,
    operation: AssignmentName,
    left: Variable,
    right: Expression,
}










pub enum Line {
    Assignment(Assignment),
    Expression(Expression),
    Continue,
    Break,
    Pass,
    Return,
    ReturnValue(Expression),
    FunctionDef(FunctionDef),
    Take(String),
    Drop(String),
    //StructDef  FOR LATER, TODO
    //EnumDef  FOR LATER, TODO
}


pub enum FuncType {
    Full(TypeWrapper, Vec<Line>), //return type, body
    Short(Vec<Line>),
}


pub struct FunctionDef {
    name: String,
    parameters: Vec<(String, TypeWrapper)>, //name, type
    func_parts: FuncType, //return type (optional), body
}


pub struct File {
    uses: Vec<String>, //CHANGE THIS
    imports: Vec<String>, //CHANGE THIS
    globals: Vec<(String, TypeWrapper)>, //name, type
    functions: Vec<FunctionDef>,
}




