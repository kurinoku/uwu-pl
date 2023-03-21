
from uwu_pass import PLCall, PLDecl, PLStx
from uwu_parser import TreeRoot, PLNumber, PLIndentifier

class PythonCompiler:

    def __init__(self, t, o) -> None:
        self.t = t
        self.o = o
    
    def compile(self) -> None:
        self.t.visit(self)

    def write(self, s) -> None:
        self.o.write(s)
    def writeln(self, s) -> None:
        self.o.write(s)
        self.o.write('\n')

    def __getattr__(self, name):
        if name.startswith('visit_'):
            def f(t):
                raise RuntimeError(f"Unknown syntax tree node. {t}")
            return f
        raise super().__getattribute__(name)
    
    CALL_NAMES = {
        'UwU': 'print',
    }

    def get_call_name(self, name: str) -> str:
        return self.CALL_NAMES[name]
    
    def format_args(self, args: list) -> str:
        t = [x.visit(self) for x in args]
        return ', '.join(t)

    def visit_call(self, call: PLCall) -> None:
        callee = call.callee
        args = call.arguments

        if not isinstance(callee, PLIndentifier):
            raise RuntimeError(f"Python compiler does not support callees that are not built-in.")

        f_name = self.get_call_name(callee.id)
        arg_list = self.format_args(args)
        self.writeln(f"{f_name}({arg_list})")
    
    def visit_root(self, root: TreeRoot) -> None:
        for child in root.children:
            child.visit(self)
    
    def visit_number(self, n: PLNumber) -> str:
        return '{}'.format(n.value)
    

    def make_name_safe(self, name: str) -> str:
        name = name.replace('@', '_at_')
        name = name.replace('!', '_bang_')
        name = name.replace('.', '_dot_')
        name = name.replace('/', '_slash_')
        name = name.replace('\\', '_bslash_')
        name = name.replace('~', '_tilde_')
        name = name.replace(':', '_colon_')
        return name
    
    def visit_identifier(self, id: PLIndentifier) -> str:
        return self.make_name_safe(id.id)

    def get_decl_initializer(self, name: str) -> str:
        v = self.DECL_INITIALIZER.get(name)
        if v is None:
            raise RuntimeError(f"Declaration initializer not found {name}.")
        return v

    def visit_decl(self, decl: PLDecl) -> None:
        var = self.make_name_safe(decl.variable.id)
        _type = decl.type
        initializer = self.get_decl_initializer(_type)
        self.writeln(f"{var} = {initializer}")

    DECL_INITIALIZER = {
        'INT': '0'
    }

    def visit_stx(self, stx: PLStx) -> None:
        name = stx.name

        if name == 'SUM':
            if len(stx.arguments) != 2:
                raise RuntimeError(f"Expected 2 parameters in SUM syntax. An identifier and a value.")
            iden, val = stx.arguments
            if not isinstance(iden, PLIndentifier):
                raise RuntimeError(f"Expected identifier as first parameter in SUM syntax.")
            val = val.visit(self)
            var = self.make_name_safe(iden.id)
            self.writeln(f"{var} += {val}")
            return
        
        raise RuntimeError(f"Unknown syntax name. {name}")