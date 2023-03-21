from typing import Any, Callable

from dataclasses import dataclass, replace

from uwu_parser import TreeRoot, TList, PLIndentifier, PLNumber

@dataclass
class PLCall:
    callee: Any
    arguments: list[Any]

    def visit(self, visitor):
        return visitor.visit_call(self)

@dataclass
class PLDecl:
    type: str
    variable: Any

    def visit(self, visitor):
        return visitor.visit_decl(self)

@dataclass
class PLStx:
    name: str
    arguments: list[Any]

    def visit(self, visitor):
        return visitor.visit_stx(self)

class Pass:
    def __init__(self, root: TreeRoot) -> None:
        self.root = root
    
    def do_pass(self) -> TreeRoot:
        return self.root.visit(self)
    
    def visit_t_list(self, t: TList) -> Any:
        callee, *args = t.children
        
        if not isinstance(callee, PLIndentifier):
            raise RuntimeError(f"Start of expression is not a identifier. {callee}")
        
        if callee.id in self.CALL_IDENTIFIERS:
            return PLCall(callee = callee, arguments = [x.visit(self) for x in args])
        elif callee.id in self.DECL_IDENTIFIERS:
            if len(args) != 1:
                raise RuntimeError(f"Declaration: syntax error. Expected just the identifier.")
            return PLDecl(type = self.DECL_IDENTIFIERS[callee.id], variable = args[0])
        elif callee.id in self.STX_IDENTFIERS:
            s = self.STX_IDENTFIERS[callee.id]
            return PLStx(name = s, arguments = args)
        raise ValueError(f"This pass does not expect a TList that cannot become other stuff.")
    
    def visit_root(self, t: Any) -> Any:
        return TreeRoot(children = [x.visit(self) for x in t.children])
    
    def _visit_others(self, t) -> Any:
        return replace(t)
    
    visit_number = _visit_others
    visit_identifier = _visit_others

    def __getattr__(self, name):
        if name.startswith('visit_'):
            def f(t):
                raise RuntimeError(f"Unknown syntax tree node. {t}")
            return f
        raise super().__getattribute__(name)

    CALL_IDENTIFIERS = {
        'UwU',
    }

    DECL_IDENTIFIERS = {
        'O.O': 'INT',
    }

    STX_IDENTFIERS = {
        ':v': 'SUM',
    }

