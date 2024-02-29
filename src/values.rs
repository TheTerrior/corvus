use std::collections::HashSet;


//pub fn get_operators() -> Vec<Vec<&'static str>> {
//    vec![
//        vec!["\\", "->"],
//        //vec!["&"], //reference
//        //vec!["@"],
//        vec!["!"],
//        vec!["**"],
//        vec!["*", "/", "%"],
//        vec!["+", "-"],
//        vec!["<<", ">>"],
//        vec!["&"], //bitwise
//        vec!["^"],
//        vec!["|"],
//        vec![":"],
//        vec!["++"],
//        vec!["==", "!=", "<", ">", "<=", ">="],
//        vec!["&&"],
//        vec!["||"],
//        vec!["..", "..="],
//        vec!["=", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>=", "**="],
//    ]
//}

/// Returns a list of "sorted" self-tokenizing symbols
pub fn get_tokenizing_symbols() -> Vec<&'static str> {
    vec![
        "::",
        ";",
        ",",
        ".",
        "_",
        "//",
        "/#",
        "#/",
        "\\",
        "@",
        ":",
        "\"",
        "'",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        "->",
        "-=",
        "-",
        "<<=",
        "<<",
        "<=",
        "<",
        "!=",
        "!",
        "**=",
        "**",
        "*=",
        "*",
        "/=",
        "/",
        ">>=",
        ">>",
        ">=",
        ">",
        "%=",
        "%",
        "++=",
        "++",
        "+=",
        "+",
        //"&&=",
        "&&",
        "&=",
        "&",
        //"||=",
        "|>",
        "||",
        "|=",
        "|",
        "^=",
        "^",
        "==",
        "=",
        "..=",
        "..",
    ]
}


/*
GLOBAL OPERATOR PRECEDENCE:
    \ ->
    & (functions)
    @
    !
    ** 
    * / %
    + -
    << >>
    &
    ^
    |
    :
    ++
    == != < > <= >=
    &&
    ||
    .. ..=
    = += -= *= /= %= &= |= ^= <<= >>= **=

*/


/*
OPERATOR PRECEDENCE:

ints and floats:
    ** 
    * / % //
    + -
    ++ --
    = += -= *= /= %=

bits:
    !
    << >>
    &
    ^
    |
    = += -= &= |= ^= <<= >>=

bools:
    !
    &
    ^
    |
    == != < > <= >=
    &&
    ||
    = &= |= ^=

lists:
    :
    ++

*/


pub fn get_keywords<'a>() -> HashSet<&'a str> {
    HashSet::from([
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
    ])
}


