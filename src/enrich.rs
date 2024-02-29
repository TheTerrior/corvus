
pub enum EnrichedToken {

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
    Parentheses(Vec<EnrichedToken>),
    Bracket(Vec<EnrichedToken>),
    Curly(Vec<EnrichedToken>),


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
    let mut ret: Vec<EnrichedToken> = Vec::new();

    let mut i = 0;
    while i < tokens.len() {
        match tokens[i].as_str() {
            "\n" => ret.push(EnrichedToken::Newline),
            "@@" => ret.push(EnrichedToken::Curry),
            "@&" => ret.push(EnrichedToken::Reference),
            "@$" => ret.push(EnrichedToken::RuneIdentifier),
            _ => {
                if tokens[i].starts_with("@s") { //spacing

                } else { //idk
                    ret.push(EnrichedToken::Literal(tokens[i].clone()))
                }
            },
        }
        i += 1;
    }
}


