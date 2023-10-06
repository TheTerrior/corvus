def find_parentheses_pair(string: str, loc: int) -> int:
    """Returns the index of the parenthesis' pair. Returns -1 if no pair exists."""
    deep = 1
    cur = loc
    
    while True:
        if cur >= len(string):
            return -1
        cur += 1
        
        if string[cur] == '(': #)
            deep += 1
        elif string[cur] == ')':
            deep -= 1
            if deep == 0:
                return cur
        else:
            continue

def find_parentheses_pair_tokens(lis: list[str], loc: int) -> int:
    """Returns the index of the parenthesis' pair. Returns -1 if no pair exists."""
    deep = 1
    cur = loc
    
    while True:
        if cur >= len(lis):
            return -1
        cur += 1
        
        if lis[cur] == '(': #)
            deep += 1
        elif lis[cur] == ')':
            deep -= 1
            if deep == 0:
                return cur
        else:
            continue

