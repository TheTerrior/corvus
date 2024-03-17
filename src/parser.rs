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


/// Parse an expression into a tree
pub fn parse_expression(tokens: &[RichToken]) -> Result<Expression, CorvusError> {
    //Ok(Expression::Value(ExpressionType::I8(String::from("placeholder"))))
    Err(CorvusError::BadExpression)
}


pub fn parse(tokens: Vec<RichToken>) -> Result<Main, CorvusError> {
    let blocks = into_chunks(tokens)?;






    Ok(Main {
        block: Block {
            lines: Vec::new(),
        }
    })
}


