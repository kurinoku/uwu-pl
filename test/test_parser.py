
# https://www.pythonforthelab.com/blog/complete-guide-to-imports-in-python-absolute-relative-and-more/
import os
import sys
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(CURR_DIR, '..'))

from tokenizer import Tokenizer
from uwu_parser import Parser

script = """
O.O @_@
:v @_@ 2
UwU @_@
"""

tkn = Tokenizer.from_string(script)
p = Parser(tkn)
print(p.parse())

