use std::collections::HashSet;

use crate::values::{get_keywords, get_tokenizing_symbols};


pub fn tokenize(input: &str) -> Vec<Vec<char>> {
    //let enclosing = HashSet::from(["(", ")", "[", "]", "{", "}", "'", "\""]);
    let keywords = get_keywords();
    //let operators: Vec<&str> = get_tokenizing_symbols();

    let chars: Vec<char> = input.chars().collect();
    let mut accum = Vec::new();
    let mut buf = Vec::new();
    let mut i = 0;
    while i < chars.len() {

        if chars[i] == ' ' && buf.len() > 0 { //ensure buf exists before pushing
            accum.push(buf);
            buf = Vec::new();
        } else { //try to identify an operator
            let mut op_matches: Vec<&str> = operators.iter()
                .map(|start| {
                    let cur_chars: Vec<char> = start.chars().collect();
                    (chars[i..].starts_with(&cur_chars), start)
                })
                .filter(|x| x.0)
                .map(|x| *x.1)
                .collect();
            op_matches.sort();
            println!("{:?}", op_matches);
        }


        i += 1;

    }
    
    accum
}


