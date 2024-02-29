
pub enum TokenType {

    // numbers
    Number(String), //doesn't include underscores and periods

    Plus,
    Minus,
    Mult,
    Div,
    Mod,
    Exponent,

    LessThan,
    GreaterThan,
    LessEqual,
    GreaterEqual,
    NotEqual,
    EqualTo,


    // bits
    Band,
    Bor,
    ShiftL,
    ShiftR,


    // bools
    Not,
    And,
    Or,
    Xor,


    // lists
    Concat,


    // list-like
    Char(String), //''
    String(String), //""
    Rune(String), //$''
    Chain(String), //$""


    // ranges
    Range,
    RangeEquals,

    
    // assignment
    Equals,
    PlusEquals,
    MinusEquals,
    MultEquals,
    DivEquals,
    ModEquals,
    ExponentEquals,

    BandEquals,
    BorEquals,
    XorEquals,

    ShiftLEquals,
    ShiftREquals,

    ConcatEquals,


    // containers
    Parentheses(Vec<TokenType>),
    Bracket(Vec<TokenType>),
    Curly(Vec<TokenType>),


    // functions and stuff
    Pipe,
    Curry,
    Reference,
    LambdaStart,
    LambdaReturn,
    Colon,


    // modules
    Dive, //::


    // formatting
    Underscore,
    Period,
    Spaces(usize),
    Newline,
    Comma,


    Literal(String), //anything that doesn't fall into any of the other categories
}


pub fn enrich(tokens: &Vec<String>) -> () {

}



