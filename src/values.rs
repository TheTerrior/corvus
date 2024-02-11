
pub fn get_operators<'a>() -> Vec<&'a str> {
    vec![
        "+", //numbers
        "-", //numbers
        "*", //numbers
        "/", //numbers
        "%", //numbers
        "<", //numbers
        ">", //numbers
        "<=", //numbers
        ">=", //numbers
        "++", //numbers, lists
        "--", //numbers

        "==", //any
        "!=", //any

        "&&", //bools
        "||", //bools
        "!", //bools

        "|", //bits, piping
        "&", //bits, referencing
        "^", //bits, bools

        "@", //currying


        "=", //assignment
        "+=", //assignment
        "-=", //assignment
        "*=", //assignment
        "/=", //assignment
        "|=", //assignment

        ":", //blocks, types, steps

        "..", //ranges
        "..=", //ranges

        "\\", //lambda
        "->", //lambda
    ]
}

pub fn get_keywords<'a>() -> Vec<&'a str> {
    vec![
        "let", //define
        "var", //define
        "fn", //define

        "global", //globals
        "take", //globals
        "drop", //globals

        "if", //conditional
        "elif", //conditional
        "else", //conditional

        "match", //matching
        "case", //matching

        "loop", //loops
        "for", //loops
        "in", //loops, iterators
        "break", //loops
        "continue", //loops

        "use", //packaged modules
        "import", //user modules

        "return", //returning

        "print", //function
        "println", //function
        "printf", //function
        "map", //function
        "filter", //function
        "fold", //function
        "reduce", //function

        "i8", //type
        "i16", //type
        "i32", //type
        "i64", //type
        "u8", //type
        "u16", //type
        "u32", //type
        "u64", //type
        "f32", //type
        "f64", //type
        "bool", //type
        "char", //type
        "str", //type
        "rune", //type
        "chain", //type

        "struct", //algebraic types
        "enum", //algebraic types
    ]
}


