


//
// #### BASIC COMPONENTS ####
//


/// Used in type signatures
pub enum StandardType {
    Unsure, //futureproofing for better type inference, useless for now
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
    CustomType(String), //structs and enums, must include name
    Function(Vec<StandardType>, Box<StandardType>), //parameters and return value, |type, type, .., type|
}


/// Used to build expressions
pub enum ExpressionType {
    I8(String),
    I16(String),
    I32(String),
    I64(String),
    U8(String),
    U16(String),
    U32(String),
    U64(String),
    F32(String),
    F64(String),
    B8(String),
    B16(String),
    B32(String),
    B64(String),
    Hex(String), //may be mapped to bits or uints
    Bool(bool),
    Char(String),
    String(String),
    Rune(String), //may be constructed with $'' or same as char with type hinting
    Chain(String), //may be constructed with $"" or same as string with type hinting
    List(Vec<ExpressionType>), //constructed with [_,_,_,] and optional last comma
    Map(Vec<ExpressionType>), //constructed with {_:_,_:_,_:_,} and optional last comma
    Set(Vec<ExpressionType>), //constructed with {_,_,_,} and optional last comma
    Tuple(Vec<ExpressionType>), //constructed with (_,_,_,) and optional last comma
    
}


pub enum Operator {
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

    Dot, //for calling methods
    Path, //for modules
    Index, //[_]
}


pub enum AssignmentType {
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


pub enum Locality {
    // reassignment
    None,

    // only accessible in scope
    Let, //immutable, assigned at run time
    Var, //mutable
    Const, //immutable, assigned at compile time

    // accessible anywhere within file if 'taken'
    LocalLet,
    LocalVar,
    LocalConst,

    // accessible from any file
    PubLet,
    PubVar, //mutable within the file
    PubConst,
    //Universal, //mutable from any file
}


pub struct Operation {
    operator: Operator,
    operand0: Expression,
    operand1: Expression,
}


//pub struct Parameter {
//    name: String,
//    param_type: StandardType,
//}


pub enum ImportType {
    Use, //installed modules
    Import, //local files, flesh this out later
}



//
// ##### LINE TYPES #####
//


pub enum Expression {
    Value(ExpressionType),
    Operation(Box<Operation>),
    FunctionCall(String, Vec<Expression>), //variable name, parameters
}


pub struct Assignment {
    name: Expression, //very limited however, just variable names and indexing
    value: Expression,
    locality: Locality,
    assignment_type: AssignmentType,
    variable_type: StandardType, //may use Unsure
}


/// Normal function definition, fully expanded, special type of assignment
pub struct FunctionDef {
    name: Expression,
    parameters: Vec<String>, //parameter names
    type_signature: StandardType, //very restricted, only Function value
    locality: Locality, //restricted
    block: Block,
}


pub struct If {
    condition: Expression,
    block: Block,
}


pub struct Elif {
    condition: Expression,
    block: Block,
}


pub struct Else {
    block: Block,
}


pub struct Loop {
    block: Block,
}


pub struct While {
    condition: Expression,
    block: Block,
}


pub struct For {
    pattern_match: Expression, //very restricted, just tuples and variable names
    iteratable: Expression,
    block: Block,
}


pub struct Import {
    import_type: ImportType,
    line: Expression, //very restricted, will flesh this out later
}


pub struct Return {
    value: Option<Expression>,
}


pub struct Take {
    value: String, //variable to take
}


pub struct Drop {
    value: String, //variable to drop
}


/// Highly important enum
pub enum Line {
    Expression(Expression),
    Assignment(Assignment),
    FunctionDef(FunctionDef),
    If(If),
    Elif(Elif),
    Else(Else),
    Loop(Loop),
    While(While),
    For(For),
    Import(Import),
    Break,
    Continue,
    Return(Return),
    Take(String), //variable to take
    Drop(String), //variable to drop
}


// Basis of many other things
pub struct Block {
    lines: Vec<Line>,
}


// Main scope
pub struct Main {
    block: Block,
}


