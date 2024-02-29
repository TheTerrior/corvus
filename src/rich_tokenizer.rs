
pub enum RichToken {

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
    //Rune(String), //$''
    //Chain(String), //$""
    RuneIdentifier,


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
    Parentheses(Vec<RichToken>),
    Bracket(Vec<RichToken>),
    Curly(Vec<RichToken>),


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


    // keywords
    Let,
    Var,
    Fn,
    Global,
    Take,
    Drop,
    If,
    Elif,
    Else,
    Match,
    Case,
    While,
    For,
    In,
    Loop,
    Break,
    Continue,
    Use,
    Import,
    Return,
    Print,
    Println,
    Printf,
    Map,
    Filter,
    Fold,
    Reduce,
    Struct,
    Enum,
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


    Literal(String), //anything that doesn't fall into any of the other categories
}


pub fn enrich(tokens: &Vec<String>) -> () {
    let mut ret: Vec<RichToken> = Vec::new();

    let mut i = 0;
    while i < tokens.len() {
        match tokens[i].as_str() {
            "\n" => ret.push(RichToken::Newline),
            "@@" => ret.push(RichToken::Curry),
            "@&" => ret.push(RichToken::Reference),
            "@$" => ret.push(RichToken::RuneIdentifier),
            _ => {
                if tokens[i].starts_with("@s") { //spacing
                    let num = &tokens[i][2..];

                } else { //idk
                    ret.push(RichToken::Literal(tokens[i].clone()))
                }
            },
        }
        i += 1;
    }
}


