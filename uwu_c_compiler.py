
from uwu_pass import PLCall, PLDecl, PLStx
from uwu_parser import TreeRoot, PLNumber, PLIndentifier

class Func:
    pass

class Printf(Func):
    f_name = 'printf'
    
    def __init__(self, compiler):
        self.compiler = compiler
    
    FORMAT_OPT = {
        'int': '%d'
    }

    def get_f_string(self, f) -> str:
        ret = self.FORMAT_OPT.get(f)
        if ret is None:
            raise RuntimeError(f"Format option for type {f} not found.")
        return ret

    def format_args(self, args):
        types = [self.compiler.get_var_type(x) for x in args]
        types_f = [self.get_f_string(x) for x in types]
        t = [x.visit(self.compiler) for x in args]
        t.insert(0, '"{}"'.format(' '.join(types_f)))
        return ', '.join(t)

class CCompiler:
    EXT = '.c'

    def __init__(self, t, o) -> None:
        self.t = t
        self.o = o

        self._var_types = {}
    
    def set_var_type(self, key, type):
        self._var_types[key] = type
    
    def get_var_type_literal(self, val) -> str:
        if isinstance(val, int):
            return 'int'
        elif isinstance(val, float):
            return 'float'
        else:
            raise RuntimeError(f"Type of literal value. {repr(val)} not known.")

    def get_var_type(self, key):
        if isinstance(key, PLIndentifier):
            key = key.id
        elif isinstance(key, PLNumber):
            val = key.value
            key = self.get_var_type_literal(val)
        elif not isinstance(key, str):
            raise TypeError(f"Expected a PLIdentifier PLNumber or str. {key}")

        v = self._var_types.get(key)
        if v is None:
            raise RuntimeError(f"Unknown var type. {key}")
        return v

    def compile(self) -> None:
        self.writeln('#include <stdio.h>')
        self.writeln('int main(int argc, char** argv) {')
        self.t.visit(self)
        self.writeln('return 0;\n}')

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
        'UwU': Printf,
    }

    def get_call_name(self, name: str) -> Func:
        f = self.CALL_NAMES.get(name)
        if f is None:
            raise RuntimeError(f"Callable name not found. {name}")
        return f(self)
    
    def format_args(self, args: list) -> str:
        t = [x.visit(self) for x in args]
        return ', '.join(t)

    def visit_call(self, call: PLCall) -> None:
        callee = call.callee
        args = call.arguments

        if not isinstance(callee, PLIndentifier):
            raise RuntimeError(f"C compiler does not support callees that are not built-in.")

        f = self.get_call_name(callee.id)
        arg_list = f.format_args(args)
        self.writeln(f"{f.f_name}({arg_list})")
    
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
        _var = decl.variable.id
        var = self.make_name_safe(decl.variable.id)
        _type = decl.type
        type_name, initializer = self.get_decl_initializer(_type)
        self.set_var_type(_var, type_name)
        self.writeln(f"{type_name} {var} = {initializer};")

    DECL_INITIALIZER = {
        'INT': ('int', '0')
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
            self.writeln(f"{var} += {val};")
            return
        
        raise RuntimeError(f"Unknown syntax name. {name}")
