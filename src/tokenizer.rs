use std::collections::HashSet;

use crate::values::{get_keywords, get_tokenizing_symbols};


enum State {
    Start,
    Floor,
}


pub fn tokenize(input: &str) -> Vec<String> {
    //let enclosing = HashSet::from(["(", ")", "[", "]", "{", "}", "'", "\""]);
    let precursors = vec![vec!['&'], vec!['@']];
    let keywords = get_keywords();
    let symbols: Vec<&str> = get_tokenizing_symbols();
    let symbols_chars: Vec<Vec<char>> = symbols
        .into_iter()
        .map(|symbol| symbol.chars().collect())
        .collect();

    let chars: Vec<char> = input.chars().collect();
    let mut accum: Vec<String> = Vec::new();
    let mut buf = String::new();
    let mut i = 0;

    let mut state = State::Start; //current state of tokenizer
    let mut spaces = 0;

    while i < chars.len() {
        if [' ', '\n', '\t'].contains(&chars[i]) { //whitespace
            if buf.len() > 0 { //ensure buf exists before pushing
                accum.push(buf);
                buf = String::new();
            }
            if ['\n', '\t'].contains(&chars[i]) { //keep track of certain whitespace
                accum.push(chars[i].to_string());
            }
            if chars[i] == '\n' {
                state = State::Start;
                spaces = 0;
            }
            if let State::Start = state { //if we're in the Start state, remember number of spaces
                if chars[i] == ' ' {
                    spaces += 1;
                }
            }
            i += 1;
            continue;
        }

        // try to identify an operator
        if let State::Start = state { //record all the spaces as a token
            accum.push((0..spaces).map(|_| " ").collect::<String>());
            state = State::Floor;
        }
        let op_match = symbols_chars
            .iter()
            .find(|symbol| chars[i..].starts_with(symbol));
        match op_match {
            None => { //nothing special, just push char to buf
                buf.push(chars[i]);
                i += 1;
            },
            Some(x) => { //new token
                if buf.len() > 0 { //ensure buf exists before pushing
                    accum.push(buf);
                }
                let mut pushing = String::from_iter(x); //prepare to push symbol

                //check certain symbols for space in front
                if i < chars.len() - 1 && chars[i+1] != ' ' && precursors.contains(x) {
                    pushing.push('_');
                }

                accum.push(pushing);
                buf = String::new();
                i += x.len();
            }
        }
    }

    // push any stragglers
    if buf.len() > 0 {
        accum.push(buf);
    }
    
    accum
}


