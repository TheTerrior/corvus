use crate::{ast_types::*, preparser::into_chunks, rich_tokenizer::RichToken, CorvusError};


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


pub fn parse_expression(tokens: &[RichToken]) -> Expression {
    Expression::Value(ExpressionType::I8(String::from("placeholder")))
}


pub fn parse(tokens: Vec<RichToken>) -> Result<Main, CorvusError> {
    let blocks = into_chunks(tokens)?;






    Ok(Main {
        block: Block {
            lines: Vec::new(),
        }
    })
}


