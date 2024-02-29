mod values;
mod tokenizer;
mod enrich;
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
}
impl fmt::Display for CorvusError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Couldn't properly read input file.")
    } 
}
impl Error for CorvusError {
}


fn main() {
    let args = Args::parse();
    let bytes: Vec<u8> = fs::read(&args.target).expect("Something went wrong reading the file");
    let input = String::from_utf8(bytes).expect("Couldn't read file correctly");
    
    let tokens = tokenizer::tokenize(&input);
    //println!("{:?}", tokens);

    let gb = tokenizer::tokenize_garbage_collect(&tokens);
    println!("{:?}", gb);

    let enriched = enrich::enrich(&gb);
}


