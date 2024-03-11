use crate::{parser_types::*, rich_tokenizer::RichToken, CorvusError};

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


/// May contain a list of tokens or an indented block
pub enum TokenBlock {
    Tokens(Vec<RichToken>),
    Block(IndentBlock),
}


/// An indented block, contains chunks, each of which is a TokenBlock
pub struct IndentBlock {
    indentation: usize,
    chunks: Vec<TokenBlock>,
}


/// Extracts one line, starting at a Spaces and ending at a Newline
pub fn extract_line(tokens: &mut Vec<RichToken>) -> Result<Vec<RichToken>, CorvusError> {
    if let RichToken::Spaces(_) = tokens[0] {
        for i in 0..tokens.len() {
            if let RichToken::Newline = tokens[i] {
                return Ok(tokens.drain(0..i).collect::<Vec<RichToken>>());
            }
        }
        // could not find a newline
    }
    Err(CorvusError::BadLine)
}


pub fn extract_block(tokens: &mut Vec<RichToken>) -> Result<IndentBlock, CorvusError> {
    let mut ret: Vec<TokenBlock> = Vec::new();
    let mut buf: Vec<RichToken> = Vec::new();
    let mut nested = false; //we will have to recurse if true

    let indentation;
    if let RichToken::Spaces(n) = tokens[0] {
        indentation = n; //get indentation
    } else {
        return Err(CorvusError::BadBlock);
    }
    loop {
        if tokens.len() > 0 {
            let cur = extract_line(tokens)?;
            if let RichToken::Spaces(n) = cur[0] {
                // n can never be less than the indentation of the block
                // because of the way I'll be recursing, it should be impossible

                if n != indentation {
                    nested = true;
                }
            }
        } else {
            break;
        }
    }

    if nested {
        todo!()
    }
    //if let RichToken::Spaces(n) = tokens[0] {
    //    let indentation = n;
    //    let mut chunks: Vec<TokenBlock> = Vec::new(); //ret
    //    let buffer: Vec<RichToken> = Vec::new();


    //    Ok(IndentBlock { indentation, chunks })
    //} else {
    //    Err(CorvusError::BadBlock)
    //}
    todo!()
}


pub fn parse_expression(tokens: &[RichToken]) -> Expression {




    todo!()
}


pub fn parse(tokens: Vec<RichToken>) -> Main {






    Main {
        block: Block {
            lines: Vec::new(),
        }
    }

}




