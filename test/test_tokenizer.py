
# https://www.pythonforthelab.com/blog/complete-guide-to-imports-in-python-absolute-relative-and-more/
import os
import sys
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(CURR_DIR, '..'))

from tokenizer import Tokenizer

script = """
O.O @_@
UwU @_@
:v @_@ 2
UwU @_@
"""

tkn = Tokenizer.from_string(script)
#for t in tkn:
#    print(t)
for i in range(15):
    print(tkn.next())

#for i, t in enumerate(tkn):
#    if i > 15:
#        break
#    print(t)
