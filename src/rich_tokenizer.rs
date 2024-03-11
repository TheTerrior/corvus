use crate::CorvusError;


#[derive(Debug, Clone)]
pub enum RichToken {

    // numbers
    Number(String), //starts with a number

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
    Path, //::


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
    Local,
    Pub,
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
    //Print,
    //Println,
    //Printf,
    //Map,
    //Filter,
    //Fold,
    //Reduce,
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
    
    True,
    False,

    As,

    Literal(String), //anything that doesn't fall into any of the other categories
}


pub fn enrich(tokens: Vec<String>) -> Result<Vec<RichToken>, CorvusError> {
    let mut ret: Vec<RichToken> = Vec::new();

    let mut i = 0;
    'outer: while i < tokens.len() {
        match tokens[i].as_str() {
            "\n" => ret.push(RichToken::Newline),
            "_" => ret.push(RichToken::Underscore),
            "." => ret.push(RichToken::Period),
            "," => ret.push(RichToken::Comma),

            "let" => ret.push(RichToken::Let),
            "var" => ret.push(RichToken::Var),
            "fn" => ret.push(RichToken::Fn),
            "local" => ret.push(RichToken::Local),
            "pub" => ret.push(RichToken::Pub),
            "take" => ret.push(RichToken::Take),
            "drop" => ret.push(RichToken::Drop),
            "if" => ret.push(RichToken::If),
            "elif" => ret.push(RichToken::Elif),
            "else" => ret.push(RichToken::Else),
            "match" => ret.push(RichToken::Match),
            "case" => ret.push(RichToken::Case),
            "while" => ret.push(RichToken::While),
            "for" => ret.push(RichToken::For),
            "in" => ret.push(RichToken::In),
            "loop" => ret.push(RichToken::Loop),
            "break" => ret.push(RichToken::Break),
            "continue" => ret.push(RichToken::Continue),
            "use" => ret.push(RichToken::Use),
            "import" => ret.push(RichToken::Import),
            "return" => ret.push(RichToken::Return),

            "struct" => ret.push(RichToken::Struct),
            "enum" => ret.push(RichToken::Enum),

            "i8" => ret.push(RichToken::VarI8),
            "i16" => ret.push(RichToken::VarI16),
            "i32" => ret.push(RichToken::VarI32),
            "i64" => ret.push(RichToken::VarI64),
            "u8" => ret.push(RichToken::VarU8),
            "u16" => ret.push(RichToken::VarU16),
            "u32" => ret.push(RichToken::VarU32),
            "u64" => ret.push(RichToken::VarU64),
            "f32" => ret.push(RichToken::VarF32),
            "f64" => ret.push(RichToken::VarF64),
            "bool" => ret.push(RichToken::VarBool),
            "char" => ret.push(RichToken::VarChar),
            "str" => ret.push(RichToken::VarStr),
            "rune" => ret.push(RichToken::VarRune),
            "chain" => ret.push(RichToken::VarChain),
            "true" => ret.push(RichToken::True),
            "false" => ret.push(RichToken::False),
            "as" => ret.push(RichToken::As),

            "|>" => ret.push(RichToken::Pipe),
            "\\" => ret.push(RichToken::LambdaStart),
            "->" => ret.push(RichToken::LambdaReturn),
            ":" => ret.push(RichToken::Colon),
            "::" => ret.push(RichToken::Path),

            "+" => ret.push(RichToken::Plus),
            "-" => ret.push(RichToken::Minus),
            "*" => ret.push(RichToken::Mult),
            "/" => ret.push(RichToken::Div),
            "%" => ret.push(RichToken::Mod),
            "**" => ret.push(RichToken::Exponent),
            "<" => ret.push(RichToken::LessThan),
            ">" => ret.push(RichToken::GreaterThan),
            "<=" => ret.push(RichToken::LessEqual),
            ">=" => ret.push(RichToken::GreaterEqual),
            "!=" => ret.push(RichToken::NotEqual),
            "==" => ret.push(RichToken::EqualTo),
            "&" => ret.push(RichToken::Band),
            "|" => ret.push(RichToken::Bor),
            "<<" => ret.push(RichToken::ShiftL),
            ">>" => ret.push(RichToken::ShiftR),
            "!" => ret.push(RichToken::Not),
            "&&" => ret.push(RichToken::And),
            "||" => ret.push(RichToken::Or),
            "^" => ret.push(RichToken::Xor),
            "++" => ret.push(RichToken::Concat),

            "=" => ret.push(RichToken::Equals),
            "+=" => ret.push(RichToken::PlusEquals),
            "-=" => ret.push(RichToken::MinusEquals),
            "*=" => ret.push(RichToken::MultEquals),
            "/=" => ret.push(RichToken::DivEquals),
            "%=" => ret.push(RichToken::ModEquals),
            "**=" => ret.push(RichToken::ExponentEquals),
            "&=" => ret.push(RichToken::BandEquals),
            "|=" => ret.push(RichToken::BorEquals),
            "^=" => ret.push(RichToken::XorEquals),
            "<<=" => ret.push(RichToken::ShiftLEquals),
            ">>=" => ret.push(RichToken::ShiftREquals),
            "++=" => ret.push(RichToken::ConcatEquals),

            ".." => ret.push(RichToken::Range),
            "..=" => ret.push(RichToken::RangeEquals),

            "@@" => ret.push(RichToken::Curry),
            "@&" => ret.push(RichToken::Reference),
            "@$" => ret.push(RichToken::RuneIdentifier),

            ")" => return Err(CorvusError::UnmatchedParentheses),
            "}" => return Err(CorvusError::UnmatchedCurlyBraces),
            "]" => return Err(CorvusError::UnmatchedSquareBrackets),

            "\"" => {
                let mut accum = String::new();
                while i < tokens.len()-1 { //keep finding all tokens of the string
                    if tokens[i+1] == "\"" {
                        ret.push(RichToken::String(accum)); //don't push quotation, just innards
                        i += 2; //account for both quotations
                        continue 'outer;
                    }
                    accum.push_str(&tokens[i+1]); //accumulate the string
                    i += 1;
                }
                return Err(CorvusError::UnmatchedString); //couldn't find matching quote
            },
            "'" => {
                if i < tokens.len()-2 && tokens[i+2] == "'" && tokens[i+1].chars().count() == 1 { //valid char tokens
                    ret.push(RichToken::Char(tokens[i+1].clone()));
                    i += 2;
                } else {
                    return Err(CorvusError::UnmatchedChar); //bad char
                }
            },
            "(" | "{" | "[" => { //all enclosing tokens
                let opening = tokens[i].as_str();
                let closing = match tokens[i].as_str() {
                    "(" => ")",
                    "{" => "}",
                    "[" => "]",
                    _ => unreachable!(),
                };
                let mut accum = Vec::new();
                let mut level = 1; //so that we don't get confused by nested enclosing tokens

                while i < tokens.len()-1 { //keep finding all tokens within enclosing symbols
                    if tokens[i+1] == opening { //opening symbol again
                        level += 1;
                    } else if tokens[i+1] == closing { //closing symbol
                        level -= 1;
                    }
                    if level == 0 {
                        let enriched = enrich(accum)?;
                        //ret.push(RichToken::Parentheses(enriched)); //need to enrich inner tokens
                        match opening { //need to enrich inner tokens and package them
                            "(" => ret.push(RichToken::Parentheses(enriched)), //need to enrich inner tokens
                            "{" => ret.push(RichToken::Curly(enriched)), //need to enrich inner tokens
                            "[" => ret.push(RichToken::Bracket(enriched)), //need to enrich inner tokens
                            _ => unreachable!(),
                        }
                        i += 2; //account for both end symbols
                        continue 'outer;
                    }
                    accum.push(tokens[i+1].clone());
                    i += 1;
                }
                return Err(match opening { //couldn't find matching end symbol
                    "(" => CorvusError::UnmatchedParentheses,
                    "{" => CorvusError::UnmatchedCurlyBraces,
                    "[" => CorvusError::UnmatchedSquareBrackets,
                    _ => unreachable!(),
                })
            },

            _ => {
                if tokens[i].starts_with("@s") { //spacing
                    let num_raw = &tokens[i][2..];
                    let num: usize = str::parse(num_raw).map_err(|_| CorvusError::NumberParse)?;
                    ret.push(RichToken::Spaces(num));
                } else if let Ok(_) = str::parse::<i32>(&tokens[i][0..1]) { //if starts with number
                    ret.push(RichToken::Number(tokens[i].clone()));
                } else { //idk
                    ret.push(RichToken::Literal(tokens[i].clone()));
                }
            },
        }
        i += 1;
    }

    Ok(ret)
}


