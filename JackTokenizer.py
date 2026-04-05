import re
import sys

# Regex para os tokens da linguagem Jack
TOKEN_SPEC = [
    ('KEYWORD',    r'\b(class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return)\b'),
    ('SYMBOL',     r'([{}()\[\],.;+\-*/&|<>=~])'),
    ('INT_CONST',  r'(\d+)'),
    ('STR_CONST',  r'"([^"\n]*)"'),
    ('IDENTIFIER', r'([a-zA-Z_][a-zA-Z_0-9]*)'),
    ('COMMENT',    r'//.*|/\*[\s\S]*?\*/'), # Comentários de linha e bloco
    ('SPACE',      r'\s+'),                 # Espaços e quebras de linha
]

# Compila a regex unificada
MASTER_RE = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC))

class JackTokenizer:
    def __init__(self, filename):
        try:
            with open(filename + ".jack", 'r') as f:
                self.source = f.read()
        except:
            print("Arquivo não encontrado. Digite o nome do arquivo jack sem a extensão.")
            sys.exit(1)


        
        self.tokens = []
        self._tokenize()
        self.current_token_idx = -1

    def _tokenize(self):
        """Transforma o código fonte em uma lista de tuplas (tipo, valor)"""
        for match in MASTER_RE.finditer(self.source):
            kind = match.lastgroup
            value = match.group(kind)
            
            if kind == 'COMMENT' or kind == 'SPACE':
                continue
            elif kind == 'STR_CONST':
                # Remove as aspas da string para o valor interno
                value = value[1:-1]
            
            self.tokens.append((kind, value))

    def has_more_tokens(self):
        return self.current_token_idx + 1 < len(self.tokens)

    def advance(self):
        if self.has_more_tokens():
            self.current_token_idx += 1
            self.current_type, self.current_value = self.tokens[self.current_token_idx]

    def getTokens(self):
        print(self.tokens)