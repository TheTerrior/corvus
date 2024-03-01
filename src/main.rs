mod values;
mod tokenizer;
mod rich_tokenizer;
mod ast;

use std::{fs, error::Error, fmt};
use clap::Parser;


#[derive(Debug, Parser, Default)]
#[clap(name = "corvus", version = "0.0.1", about = "Compiler for Ambester",)]
pub struct Args {
    /// The input file to read
    pub target: String,
    ///// Print the raw bits from the target
    //#[clap(long, short, action)]
    //pub read_bits: bool,
}


#[derive(Debug, Clone)]
pub enum CorvusError {
    FileRead,
    NumberParse, //likely a compiler error not a user error
    UnmatchedParentheses,
    UnmatchedCurlyBraces,
    UnmatchedSquareBrackets,
    UnmatchedString,
    UnmatchedChar,
}
impl fmt::Display for CorvusError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Received error: {}", self)
    } 
}
impl Error for CorvusError {
}


fn main() {
    let args = Args::parse();
    let bytes: Vec<u8> = fs::read(&args.target).expect("Something went wrong reading the file");
    let input = String::from_utf8(bytes).expect("Couldn't read file correctly");
    
    let tokens = tokenizer::tokenize(&input);
    let gb = tokenizer::tokenize_garbage_collect(&tokens);
    let enriched = rich_tokenizer::enrich(&gb);
    println!("{:?}", enriched);
}


