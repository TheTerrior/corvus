use crate::values::{get_keywords, get_tokenizing_symbols};


/// Helps tokenizer keep track of current process
enum State {
    Start,
    Floor,

    Scan,
    String,
    Comment,
    Multiline,
}


/// Take a string and perform the initial tokenization with limited processing
pub fn tokenize(input: &str) -> Vec<String> {
    let precursors = vec![vec!['&'], vec!['@'], vec!['$']];
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
            //accum.push((0..spaces).map(|_| " ").collect::<String>());
            accum.push(format!("@s{}", spaces));
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

                //check certain symbols for space in front, precursors
                let pushing: String;
                if i < chars.len() - 1 && chars[i+1] != ' ' && precursors.contains(x) {
                    //pushing.insert(0, x);
                    pushing = String::from("@") + &String::from_iter(x); //push symbol with precursor notation
                } else {
                    pushing = String::from_iter(x); //push just symbol
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
    
    tokenize_garbage_collect(accum)
}


/// Clean up generated tokens
pub fn tokenize_garbage_collect(tokens: Vec<String>) -> Vec<String> {
    let mut ret = Vec::new();
    let mut ret1 = Vec::new();
    let mut state = State::Scan;

    // first remove all comments
    let mut i = 0;
    while i < tokens.len() {
        let cur = &tokens[i];

        // remove repeat newlines
        if cur == "\n" {
            while i < tokens.len() - 1 && tokens[i+1] == "\n" {
                i += 1;
            }
        }

        // handle comments
        match &state {
            State::Scan => { //not currently in a special state
                match cur.as_str() {
                    "\"" => {
                        state = State::String; //always push with a string
                        ret.push(cur.clone());
                    },
                    "//" => state = State::Comment,
                    "/#" => state = State::Multiline,
                    _ => ret.push(cur.clone()),
                }
            },
            State::String => { //inside of a string
                if cur == "\"" {
                    state = State::Scan;
                }
                ret.push(cur.clone());
            },
            State::Comment => { //inside of a comment
                if cur == "\n" {
                    ret.push(cur.clone());
                    state = State::Scan;
                }
            },
            State::Multiline => { //inside of a multiline comment
                if cur == "#/" {
                    state = State::Scan;
                }
            },
            _ => unreachable!(),
        }

        i += 1;
    }

    // remove repeat newlines with tabs
    i = 0;
    while i < ret.len() {
        if ret[i].starts_with("@s") {
            while i < ret.len() - 2 && ret[i+1] == "\n" && ret[i+2].starts_with("@s") {
                i += 2;
            }
            println!("{}, {}", ret[i+1], ret[i+2]);
        }

        ret1.push(ret[i].clone());
        i += 1;
    }

    if ret1.len() > 0 && ret1[ret1.len()-1] != "\n" {
        ret1.push(String::from("\n"));
    }

    ret1
}


