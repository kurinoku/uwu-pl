from collections.abc import Iterable
from typing import Optional, Any

from dataclasses import dataclass
from enum import Enum, auto

from uwu_exception import UWUTokenizerError

class TokenType(Enum):
    NL = auto()
    NAME = auto()
    NUMBER = auto()
    TYPE = auto()
    EOF = auto()

@dataclass
class Token:
    line: int
    col: int
    n: int
    span: int
    source_name: Optional[str]
    source_path: Optional[str]
    type: TokenType
    value: Any

@dataclass
class SourcePosition:
    line: int
    col: int
    n: int

KEYWORDS = {
    'O.O': TokenType.NAME
}

class Tokenizer:
    source: Iterable[str]
    source_name: Optional[str]
    source_path: Optional[str]
    _line: int
    _col: int
    _char: int
    
    _last_token: Optional[Token]

    def __init__(self, source: Iterable[str], source_name: Optional[str] = None, source_path: Optional[str] = None) -> None:
        self.source = source
        self.source_name = source_name
        self.source_path = source_path

        self._line = 0
        self._col = 0
        self._char = 0
        self._current_char_position = SourcePosition(0, 0, 0)
        self._last_char = ''
        self._rescue_last_char = False
        self._last_token = None

    def make_error(self, msg: str) -> UWUTokenizerError:
        return UWUTokenizerError(msg)

    def make_token(self, type: TokenType, value: Any = None, start_position: Optional[SourcePosition] = None) -> Token:
        line = self._line
        col = self._col
        char = self._char
        span = 1
        if start_position is not None:
            line = start_position.line
            col = start_position.col
            span = char - start_position.n - 1
            char = start_position.n
        
        t = Token(
            type = type, value = value, 
            source_name = self.source_name, source_path = self.source_path,
            line = line, col = col, n = char, span = span
            )
        self._last_token = t
        return t

    def eof_token(self):
        return self.make_token(TokenType.EOF)

    def next_char(self) -> str:
        if self._rescue_last_char:
            self._rescue_last_char = False
            return self._last_char
        c = next(self.source)
        self._last_char = c
        self._current_char_position = SourcePosition(
            self._line,
            self._col,
            self._char
        )
        self._char += 1
        self._col += 1
        if c == '\n':
            self._line += 1
            self._col = 0
        return c

    def rescue_char(self) -> None:
        """
        Make self.next_char use the last char fetch instead of
        fetching a new one from source

        This is a workaround since I'm using an iterator for source.
        """
        self._rescue_last_char = True

    def is_last_token(self, token_type: TokenType) -> bool:
        return self._last_token is not None and self._last_token.type == token_type

    def is_name_start(self, c: str) -> bool:
        return c.isalpha() or c in '_!.@/\\~:'
    
    def is_name_character(self, c: str) -> bool:
        return self.is_name_start(c) or c.isdigit()

    def name(self, c: str, original_position: SourcePosition) -> Token:
        try:
            t = [c]
            c = self.next_char()
            while self.is_name_character(c):
                t.append(c)
                c = self.next_char()
            self.rescue_char()
        except StopIteration:
            pass
        
        s = ''.join(t)
        return self.make_token(TokenType.NAME, s, original_position)

    def number(self, c: str, original_position: SourcePosition) -> Token:
        try:
            t = [c]
            c = self.next_char()
            while c.isdigit() or c in '_':
                if c not in '_':
                    t.append(c)
                c = self.next_char()
            
            if c == '.':
                t.append(c)
                c = self.next_char()

                if c.isdigit() or c in '_':
                    while c.isdigit() or c in '_':
                        if c not in '_':
                            t.append(c)
                        c = self.next_char()
                else:
                    raise self.make_error(f"Expected digit or underscore after dot in decimal.")


            self.rescue_char()
        except StopIteration:
            pass

        s = ''.join(t)
        return self.make_token(TokenType.NUMBER, float(s), original_position)

    def next(self) -> Token:
        try:
            while True:
                c = self.next_char()
                if c == '\n' and not self.is_last_token(TokenType.NL):
                    return self.make_token(type = TokenType.NL)
                elif self.is_name_start(c):
                    return self.name(c, self._current_char_position)
                elif c in '\t ':
                    continue
                elif c.isdigit():
                    return self.number(c, self._current_char_position)
                else:
                    raise self.make_error(f"Unknown token. {repr(c)}")
        except StopIteration:
            return self.eof_token()
    
    def get_last_token(self) -> Token:
        return self._last_token

    def generator(self):
        t = self.next()
        while t.type != TokenType.EOF:
            yield t
            t = self.next()
        yield t
    
    def __iter__(self):
        return iter(self.generator())
    
    @classmethod
    def from_string(cls, s: str) -> 'Tokenizer':
        name = '<string>'
        source = iter(s)
        return cls(source = source, source_name = name)