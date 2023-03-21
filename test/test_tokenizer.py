import common
from tokenizer import Tokenizer

script = """
O.O @_@
UwU @_@
:v @_@ 2
UwU @_@
:v @_@ 2.5
UwU @_@
"""

tkn = Tokenizer.from_string(script)
for t in tkn:
    print(t)
#for i in range(50):
#    print(tkn.next())

#for i, t in enumerate(tkn):
#    if i > 15:
#        break
#    print(t)
