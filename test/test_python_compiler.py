import common

import io

from tokenizer import Tokenizer
from uwu_parser import Parser
from uwu_pass import Pass
from uwu_python_compiler import PythonCompiler

script = """
O.O @_@
:v @_@ 2
UwU @_@
"""

tkn = Tokenizer.from_string(script)
p = Parser(tkn)
ps = Pass(p.parse())
t = ps.do_pass()
output = io.StringIO()
compiler = PythonCompiler(t, output)
compiler.compile()
print(output.getvalue())
