use crate::{rich_tokenizer::RichToken, CorvusError};


/// May contain a list of tokens or an indented block
#[derive(Debug)]
pub enum Chunk {
    Tokens(Vec<Vec<RichToken>>), //list of lines of richtokens
    Block(Vec<Chunk>), //indented piece of code
}


/// Extracts one line, starting at a Spaces and ending at a Newline
pub fn extract_line(tokens: &mut Vec<RichToken>) -> Result<Vec<RichToken>, CorvusError> {
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


/// Takes a block of code and recursively breaks it into deeper blocks and chunks
pub fn into_chunks(mut tokens: Vec<RichToken>) -> Result<Vec<Chunk>, CorvusError> {
    if tokens.len() == 0 {
        return Err(CorvusError::EmptyBlock);
    }

    let mut chunks: Vec<Chunk> = Vec::new(); //returns blockized tokens
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
                        chunks.push(Chunk::Block( //parse the inner block
                            into_chunks(buf
                                .into_iter()
                                .flatten()
                                .collect::<Vec<RichToken>>()
                            )?
                        ));
                    }
                    buf = Vec::new();
                }
            },
            RichToken::Spaces(_) => { //diff indentation as base
                if on_base { //moving from base to inner layer
                    on_base = false;
                    if buf.len() != 0 {
                        chunks.push(Chunk::Tokens(buf)); //save the base chunk
                    }
                    buf = Vec::new();
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
                chunks.push(Chunk::Tokens(buf)); //save the base chunk
            },
            RichToken::Spaces(_) => { //diff indentation as base
                chunks.push(Chunk::Block( //parse the inner block
                    into_chunks(buf
                        .into_iter()
                        .flatten()
                        .collect::<Vec<RichToken>>()
                    )?
                ));
            },
            _ => return Err(CorvusError::BadBlock),
        }
    }

    Ok(chunks)
}


