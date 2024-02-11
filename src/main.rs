mod values;
mod tokenizer;
mod ast;

use std::fs;
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

fn main() {
    let args = Args::parse();
    let bytes: Vec<u8> = fs::read(&args.target).expect("Something went wrong reading the file");
    let input = String::from_utf8(bytes).expect("Couldn't read file correctly");
    
    let tokens = tokenizer::tokenize(&input);
}


