


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
    As, //for some type casting
}


pub enum UnaryOperator {
    Not,
    Negate,
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
}


pub struct Operation {
    pub operator: Operator,
    pub operand0: Expression,
    pub operand1: Expression,
}


pub struct UnaryOperation {
    pub operator: UnaryOperator,
}


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
    UnaryOperation(Box<UnaryOperation>),
    FunctionCall(String, Vec<Expression>), //variable name, parameters
    FunctionCurry(String, Vec<Expression>), //variable name, parameters
}


pub struct Assignment {
    pub name: Expression, //very limited however, just variable names and indexing
    pub value: Expression,
    pub locality: Locality,
    pub assignment_type: AssignmentType,
    pub variable_type: StandardType, //may use Unsure
}


/// Normal function definition, fully expanded, special type of assignment
pub struct FunctionDef {
    pub name: Expression,
    pub parameters: Vec<String>, //parameter names
    pub type_signature: StandardType, //very restricted, only Function value
    pub locality: Locality, //restricted
    pub block: Block,
}


pub struct If {
    pub condition: Expression,
    pub block: Block,
}


pub struct Elif {
    pub condition: Expression,
    pub block: Block,
}


pub struct Else {
    pub block: Block,
}


pub struct Loop {
    pub block: Block,
}


pub struct While {
    pub condition: Expression,
    pub block: Block,
}


pub struct For {
    pub pattern_match: Expression, //very restricted, just tuples and variable names
    pub iteratable: Expression,
    pub block: Block,
}


pub struct Import {
    pub import_type: ImportType,
    pub line: Expression, //very restricted, will flesh this out later
}


pub struct Return {
    pub value: Option<Expression>,
}


pub struct Take {
    pub value: String, //variable to take
}


pub struct Drop {
    pub value: String, //variable to drop
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


// Basis of many other things, contains a collection of lines, sometimes acts as a scope
pub struct Block {
    pub lines: Vec<Line>,
}


// Main scope
pub struct Main {
    pub block: Block,
}


