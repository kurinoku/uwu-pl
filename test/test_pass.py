import common
from tokenizer import Tokenizer
from uwu_parser import Parser
from uwu_pass import Pass
script = """
O.O @_@
:v @_@ 2
UwU @_@
"""


tkn = Tokenizer.from_string(script)
p = Parser(tkn)
print(
    Pass(p.parse()).do_pass()
)

