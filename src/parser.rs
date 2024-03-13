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
#[derive(Debug)]
pub enum TokenBlock {
    Tokens(Vec<Vec<RichToken>>), //list of lines of richtokens
    Block(IndentBlock),
}


/// An indented block, contains chunks, each of which is a TokenBlock
#[derive(Debug)]
pub struct IndentBlock {
    //indentation: usize,
    chunks: Vec<TokenBlock>,
}


///// Extracts one line, starting at a Spaces and ending at a Newline
//pub fn extract_line(tokens: &mut Vec<RichToken>) -> Result<Vec<RichToken>, CorvusError> {
//    println!("extracting a line: {:?}", tokens);
//    if let RichToken::Spaces(_) = tokens[0] {
//        for i in 0..tokens.len() {
//            if let RichToken::Newline = tokens[i] {
//                return Ok(tokens.drain(0..i+1).collect::<Vec<RichToken>>());
//            }
//        }
//        // could not find a newline
//    }
//    Err(CorvusError::BadLine)
//}


/// Extracts one line, starting at a Spaces and ending at a Newline
pub fn extract_line(tokens: &mut Vec<RichToken>) -> Result<Vec<RichToken>, CorvusError> {
    println!("extracting a line: {:?}", tokens);
    if let RichToken::Spaces(_) = tokens[0] {
        for i in 0..tokens.len() {
            if let RichToken::Newline = tokens[i] {
                return Ok(tokens.drain(0..i+1).collect::<Vec<RichToken>>());
            }
        }
        // could not find a newline
    }
    Err(CorvusError::BadLine)
}


///// Takes a block of code and recursively breaks it into deeper blocks and chunks
//pub fn extract_block(tokens: &mut Vec<RichToken>) -> Result<IndentBlock, CorvusError> {
//    if tokens.len() == 0 {
//        return Err(CorvusError::EmptyBlock);
//    }
//
//    let mut chunks: Vec<TokenBlock> = Vec::new(); //returns blockized tokens
//    let mut lines: Vec<Vec<RichToken>> = Vec::new(); //contains lines for collection later
//
//    // retrieve indentation
//    let indentation;
//    if let RichToken::Spaces(n) = tokens[0] { //see if our tokens are correct
//        indentation = n; //get base indentation for this block
//    } else {
//        return Err(CorvusError::BadBlock);
//    }
//
//    // first split into lines
//    while tokens.len() > 0 {
//        lines.push(extract_line(tokens)?);
//    }
//
//    // then break into chunks of lines and blocks
//    let mut on_base = true; //start on base layer by default
//    let mut buf = Vec::new();
//    for i in 0..lines.len() {
//        match lines[i][0] {
//            RichToken::Spaces(n) if n == indentation => { //same indentation as base
//                if !on_base { //if just got back to the base layer
//                    on_base = true;
//                    chunks.push(TokenBlock::Block( //parse the inner block
//                        extract_block(&mut buf
//                            .into_iter()
//                            .flatten()
//                            .collect::<Vec<RichToken>>()
//                        )?
//                    ));
//                } else {
//                    buf.push(lines[i].clone()); //already on base layer, append to buf
//                }
//            },
//            RichToken::Spaces(_) => { //diff indentation as base
//                if on_base { //moving from base to inner layer
//                    on_base = false;
//                    chunks.push(TokenBlock::Tokens(buf)); //save the base chunk
//                } else {
//                    buf.push(lines[i].clone());
//                }
//            }
//            _ => return Err(CorvusError::BadBlock),
//        }
//        buf = Vec::new();
//    }
//
//    //Ok(IndentBlock { indentation, chunks })
//    Ok(IndentBlock { chunks })
//}


/// Takes a block of code and recursively breaks it into deeper blocks and chunks
pub fn extract_block(mut tokens: Vec<RichToken>) -> Result<IndentBlock, CorvusError> {
    if tokens.len() == 0 {
        return Err(CorvusError::EmptyBlock);
    }

    let mut chunks: Vec<TokenBlock> = Vec::new(); //returns blockized tokens
    let mut lines: Vec<Vec<RichToken>> = Vec::new(); //contains lines for collection later

    // retrieve indentation
    let indentation;
    if let RichToken::Spaces(n) = tokens[0] { //see if our tokens are correct
        indentation = n; //get base indentation for this block
    } else {
        return Err(CorvusError::BadBlock);
    }

    // first split into lines
    while tokens.len() > 0 {
        lines.push(extract_line(&mut tokens)?);
    }

    // then break into chunks of lines and blocks
    let mut on_base = true; //start on base layer by default
    let mut buf = Vec::new();
    for i in 0..lines.len() {
        match lines[i][0] {
            RichToken::Spaces(n) if n == indentation => { //same indentation as base
                if !on_base { //if just got back to the base layer
                    on_base = true;
                    if buf.len() != 0 {
                        chunks.push(TokenBlock::Block( //parse the inner block
                            extract_block(buf
                                .into_iter()
                                .flatten()
                                .collect::<Vec<RichToken>>()
                            )?
                        ));
                    }
                    buf = Vec::new();
                    //buf = vec![lines[i].clone()];
                //} else {
                //    buf.push(lines[i].clone()); //already on base layer, append to buf
                }
            },
            RichToken::Spaces(_) => { //diff indentation as base
                if on_base { //moving from base to inner layer
                    on_base = false;
                    if buf.len() != 0 {
                        chunks.push(TokenBlock::Tokens(buf)); //save the base chunk
                    }
                    buf = Vec::new();
                    //buf = vec![lines[i].clone()];
                //} else {
                }
            }
            _ => return Err(CorvusError::BadBlock),
        }
        buf.push(lines[i].clone());
    }

    if buf.len() != 0 { //clean up rest of buf
        // need to find out if we have lines or a block
        match buf[0][0] {
            RichToken::Spaces(n) if n == indentation => { //same indentation as base
                chunks.push(TokenBlock::Tokens(buf)); //save the base chunk
            },
            RichToken::Spaces(_) => { //diff indentation as base
                chunks.push(TokenBlock::Block( //parse the inner block
                    extract_block(buf
                        .into_iter()
                        .flatten()
                        .collect::<Vec<RichToken>>()
                    )?
                ));
            },
            _ => return Err(CorvusError::BadBlock),
        }
    }

    //Ok(IndentBlock { indentation, chunks })
    Ok(IndentBlock { chunks })
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




