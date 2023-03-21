
import argparse
import os
import sys

from tokenizer import Tokenizer
from uwu_parser import Parser
from uwu_pass import Pass
from uwu_c_compiler import CCompiler
from uwu_python_compiler import PythonCompiler

parser = argparse.ArgumentParser(
    prog = 'UWUc',
    description = 'I un-uwu a file in the UWU programming language.',
    epilog = 'UWU your world.'
)

parser.add_argument('file')
group = parser.add_mutually_exclusive_group()
group.add_argument('--c', action='store_true')
group.add_argument('--python', action='store_true')

def err(msg):
    print(msg, file=sys.stderr)
    exit(-1)

def comp(path, compiler_cls):
    filename = os.path.basename(path)
    no_ext, _ = os.path.splitext(path)
    target = no_ext + compiler_cls.EXT

    with open(target, 'w', encoding='utf-8') as o:
        with open(path, 'r', encoding='utf-8') as f:
            tknzr = Tokenizer(iter(f.read()), source_path = path, source_name = filename)
            parser = Parser(tknzr)
            tree_1 = parser.parse()
            pass_1 = Pass(tree_1)
            t = pass_1.do_pass()
            compiler = compiler_cls(t, o)
            compiler.compile()

def main(args):
    path = args.file
    if not os.path.isfile(path):
        err(f"UWUc: '{path}' does not exist.")
    
    if args.c:
        comp(path, CCompiler)
    else:
        comp(path, PythonCompiler)
        


if __name__ == '__main__':
    main(parser.parse_args())
