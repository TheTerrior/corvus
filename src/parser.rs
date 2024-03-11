use crate::{parser_types::*, rich_tokenizer::RichToken};

/*
OPERATOR PRECEDENCE:

    Path,
    Dot,
    Index,
    Not, Negate,
    As,
    Exp,
    Mult, Div, Mod,
    Add, Sub,
    ShiftL, ShiftR,
    Band,
    Xor,
    Bor,
    Cons, Concat,
    LT, GT, LEqT, GEqT, NEqT, EqT,
    And,
    Or,
    Range, RangeEq,
    Pipe,
*/


pub fn parse_expression(tokens: &[RichToken]) {

}


pub fn parse(tokens: &Vec<RichToken>) -> Main {






    Main {
        block: Block {
            lines: Vec::new(),
        }
    }

}




