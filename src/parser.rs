use crate::rich_tokenizer::RichToken;


pub enum OperationName {
    Add,
    Sub,
    Mult,
    Div,
    Mod,
    Exp,
}


pub struct NumberOperation {
    operation: OperationName,
    operand0: String,
}


pub enum Value {
    Variable,
    Number,
}


pub struct Operation {
    operation: OperationName,
    operand0: Value,
    operand1: Value,
}


pub fn parse(tokens: &Vec<RichToken>) -> () {

}




