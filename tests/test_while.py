import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser import Parser

tokens = [
    ('KEYWORD', 'while'),
    ('SYMBOL', '('),
    ('KEYWORD', 'false'),
    ('SYMBOL', ')'),
    ('SYMBOL', '{'),

    ('KEYWORD', 'return'),
    ('INT_CONST', '10'),
    ('SYMBOL', ';'),

    ('SYMBOL', '}')
]

parser = Parser(tokens)

parser.parse_while()

print(parser.get_vm_output())