from typing import Optional, Union, Any

from tokenizer import TokenType, Tokenizer, Token
from dataclasses import dataclass

@dataclass
class TreeRoot:
    children: list

@dataclass
class TList:
    children: list

@dataclass
class PLIndentifier:
    id: str
    token: Token

@dataclass
class PLNumber:
    value: float
    token: Token

class _Skip:
    pass
Skip = _Skip()

class _EOF:
    pass
EOF = _EOF()


class Parser:
    def __init__(self, tokenizer: Tokenizer) -> None:
        self.tokenizer = tokenizer
        self._current = None
        self._last = None
        self.read_next()
    
    def read_next(self) -> None:
        self._last = self._current
        self._current = self.tokenizer.next()
    
    @property
    def current(self) -> Token:
        return self._current
    
    @property
    def last(self) -> Optional[Token]:
        return self._last

    def parse(self):
        children = []
        while True:
            child = self._parse()
            if child is not Skip and child is not EOF:
                children.append(child)
            elif child is EOF:
                break
            elif child is Skip:
                pass
            else:
                raise RuntimeError(f"Unknown value returned by _parse. {child}")
        return TreeRoot(children)
    

    def try_match(self, *types: list[TokenType]) -> bool:
        for type in types:
            if self.current.type == type:
                self.read_next()
                return True
        return False
    
    def match(self, type: Union[TokenType, list[TokenType]], message: str = 'Unknown sequence of tokens.') -> bool:
        if isinstance(type, TokenType):
            type = [type]
        if not self.try_match(*type):
            raise RuntimeError(message)
        return True

    def name_eval(self, t: Token) -> Any:
        if t.type == TokenType.NAME:
            return PLIndentifier(t.value, t)
        if t.type == TokenType.NUMBER:
            return PLNumber(t.value, t)
        raise RuntimeError(f"Unknown token evaluated in name expression.")

    def name_parse(self) -> TList:
        t = [self.name_eval(self.last)]
        while self.try_match(TokenType.NAME, TokenType.NUMBER, TokenType.TYPE):
            t.append(self.name_eval(self.last))
        self.match(TokenType.NL, 'Expected new line character after sequence of expressions.')
        return TList(t)

    def _parse(self):
        if self.try_match(TokenType.NL):
            return Skip
        
        if self.try_match(TokenType.EOF):
            return EOF

        if self.match(TokenType.NAME, message = "Unknown sequence of tokens."):
            return self.name_parse()

               
        raise RuntimeError(f"Unknown sequence of tokens.")

