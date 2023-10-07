from dataclasses import dataclass
from typing import Any, TypeVar, Generic


T = TypeVar('T')
E = TypeVar('E')


class Result(Generic[T, E]):
    """Stores an Error or Ok value."""

    is_ok: bool
    value: Any
    err: Any


    def unwrap(self) -> T:
        """Unwraps the contained value or throws the contained error."""
        if self.is_ok:
            return self.value
        raise Exception(self.err)

class Option(Generic[T]):
    """Stores a Some or None value."""

    is_some: bool
    value: Any 

    def unwrap(self) -> T | None:
        """Unwraps the contained value or returns None."""
        if self.is_some:
            return self.value
        return None

def err(error: E) -> Result[Any, E]:
    ret: Result[Any, E] = Result()
    ret.is_ok = False
    ret.value = None
    ret.err = error
    return ret

def ok(value: T) -> Result[T, Any]:
    ret: Result[T, Any] = Result()
    ret.is_ok = True
    ret.value = value
    ret.err = None
    return ret

def some(value: T) -> Option[T]:
    ret: Option[T] = Option()
    ret.is_some = True
    ret.value = value
    return ret

def none() -> Option[Any]:
    ret: Option[Any] = Option()
    ret.is_some = False
    ret.value = None 
    return ret


def find_paren_str(string: str, loc: int) -> int:
    """Returns the index of the parenthesis' pair in a string. Returns -1 if no pair exists."""
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


def find_paren_tokens(lis: list[str], loc: int) -> int:
    """Returns the index of the parenthesis' pair in a list of tokens. Returns -1 if no pair exists."""
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


@dataclass
class Fakerator:
    """Turns a list of tokens into an iterator."""

    tokens: list[str]
    position: int

    def consume_line_tokens(self) -> list[str]:
        """Consumes the next line in the iterator."""
        #accum = []

        #while self.position < len(self.tokens) - 1:
        #    st = self.tokens[self.position]
        #    if st == '\n':
        #        accum.append(st)
        #        self.position += 1
        #        return accum
        #    elif st.strip() == "":  #handle indentation
        #        self.position += 1
        #        continue
        #    else:
        #        accum.append(st)
        #        self.position += 1
        #return accum

        pos = self.position
        tabs = 0
        tabbing = True
        #while pos < len(self.tokens) - 1:
            #if tabbing and self.tokens[pos] == "":
        return []



    def consume_line_str(self) -> str:
        """Consumes the next line in the iterator (not including indentation) as a string."""
        accum = ""

        while self.position < len(self.tokens) - 1:
            st = self.tokens[self.position]
            if st == '\n':
                self.position += 1
                return accum + st
            elif st.strip() == "":  #handle indentation
                self.position += 1
                continue
            else:
                accum += st
                self.position += 1
        return accum

    def peak_line_tokens(self) -> list[str]:
        """Peaks the next line in the iterator (not including indentation) without altering the Fakerator."""
        accum = []
        pos = self.position

        while self.position < len(self.tokens) - 1:
            st = self.tokens[pos]
            if st == '\n':
                accum.append(st)
                pos += 1
                return accum
            elif st.strip() == "":  #handle indentation
                pos += 1
                continue
            else:
                accum.append(st)
                pos += 1
        return accum

    def peak_line_tokens_indent(self) -> list[str]:
        """Peaks the next line in the iterator (including the indentation) without altering the Fakerator."""
        accum = []
        pos = self.position

        while self.position < len(self.tokens) - 1:
            st = self.tokens[pos]
            if st == '\n':
                accum.append(st)
                pos += 1
                return accum
            else:
                accum.append(st)
                pos += 1
        return accum

    def peak_line_str(self) -> str:
        """Peaks the next line in the iterator (not including indentation) as a string without altering the Fakerator."""
        accum = ""
        pos = self.position

        while self.position < len(self.tokens) - 1:
            st = self.tokens[pos]
            if st == '\n':
                pos += 1
                return accum + st
            elif st.strip() == "":  #handle indentation
                pos += 1
                continue
            else:
                accum += st
                pos += 1
        return accum

    def peak_rest_tokens(self) -> list[str]:
        """Returns the rest of the tokens without altering the Fakerator."""
        return self.tokens[self.position:]




























@dataclass
class Fakerator_old:
    """Turns a list of tokens into an iterator."""

    tokens: list[str]
    position: int

    def consume_line_tokens(self) -> list[str]:
        """Consumes the next line in the iterator."""
        accum = []

        while self.position < len(self.tokens) - 1:
            st = self.tokens[self.position]
            if st == '\n':
                accum.append(st)
                self.position += 1
                return accum
            elif st.strip() == "":  #handle indentation
                self.position += 1
                continue
            else:
                accum.append(st)
                self.position += 1
        return accum


    def consume_line_str(self) -> str:
        """Consumes the next line in the iterator (not including indentation) as a string."""
        accum = ""

        while self.position < len(self.tokens) - 1:
            st = self.tokens[self.position]
            if st == '\n':
                self.position += 1
                return accum + st
            elif st.strip() == "":  #handle indentation
                self.position += 1
                continue
            else:
                accum += st
                self.position += 1
        return accum

    def peak_line_tokens(self) -> list[str]:
        """Peaks the next line in the iterator (not including indentation) without altering the Fakerator."""
        accum = []
        pos = self.position

        while self.position < len(self.tokens) - 1:
            st = self.tokens[pos]
            if st == '\n':
                accum.append(st)
                pos += 1
                return accum
            elif st.strip() == "":  #handle indentation
                pos += 1
                continue
            else:
                accum.append(st)
                pos += 1
        return accum

    def peak_line_tokens_indent(self) -> list[str]:
        """Peaks the next line in the iterator (including the indentation) without altering the Fakerator."""
        accum = []
        pos = self.position

        while self.position < len(self.tokens) - 1:
            st = self.tokens[pos]
            if st == '\n':
                accum.append(st)
                pos += 1
                return accum
            else:
                accum.append(st)
                pos += 1
        return accum

    def peak_line_str(self) -> str:
        """Peaks the next line in the iterator (not including indentation) as a string without altering the Fakerator."""
        accum = ""
        pos = self.position

        while self.position < len(self.tokens) - 1:
            st = self.tokens[pos]
            if st == '\n':
                pos += 1
                return accum + st
            elif st.strip() == "":  #handle indentation
                pos += 1
                continue
            else:
                accum += st
                pos += 1
        return accum

    def peak_rest_tokens(self) -> list[str]:
        """Returns the rest of the tokens without altering the Fakerator."""
        return self.tokens[self.position:]

