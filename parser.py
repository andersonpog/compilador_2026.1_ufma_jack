class Parser:
    TAG_MAP = {
        'KEYWORD': 'keyword',
        'SYMBOL': 'symbol',
        'INT_CONST': 'integerConstant',
        'STR_CONST': 'stringConstant',
        'IDENTIFIER': 'identifier'
    }

    XML_ESCAPE = {
        '<': '&lt;',
        '>': '&gt;',
        '&': '&amp;',
        '"': '&quot;'
    }

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.xml_output = []
        self.indent_level = 0

    def peek(self):
        """Retorna o token atual sem avançar."""
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None

    def peek_next(self):
        """Retorna o próximo token sem avançar."""
        if self.current + 1 < len(self.tokens):
            return self.tokens[self.current + 1]
        return None

    def advance(self):
        """Avança para o próximo token e retorna o atual."""
        token = self.peek()
        if token is not None:
            self.current += 1
        return token

    def match(self, expected_type, expected_value=None):
        """
        Verifica se o token atual é do tipo esperado
        e opcionalmente do valor esperado.
        """
        token = self.peek()

        if token is None:
            raise SyntaxError("Erro de sintaxe: fim inesperado da entrada")

        token_type, token_value = token

        if token_type != expected_type:
            raise SyntaxError(
                f"Erro de sintaxe: esperado tipo {expected_type}, "
                f"encontrado {token_type} ({token_value})"
            )

        if expected_value is not None and token_value != expected_value:
            raise SyntaxError(
                f"Erro de sintaxe: esperado valor '{expected_value}', "
                f"encontrado '{token_value}'"
            )

        self.write_token(token)
        self.advance()
        return token

    def parse_term(self):
        self.open_tag("term")
        token = self.peek()

        if token is None:
            raise SyntaxError("Termo esperado, mas fim da entrada encontrado")

        token_type, token_value = token

        if token_type == 'INT_CONST':
            self.write_token(self.advance())

        elif token_type == 'STR_CONST':
            self.write_token(self.advance())

        elif token_type == 'KEYWORD' and token_value in ['true', 'false', 'null', 'this']:
            self.write_token(self.advance())

        elif token_type == 'IDENTIFIER':
            self.write_token(self.advance())

        else:
            raise SyntaxError(f"Termo esperado, encontrado: {token_value}")

        self.close_tag("term")

    def parse_expression(self):
        self.open_tag("expression")
        self.parse_term()

        while self.peek() and self.peek()[1] in "+-*/&|<>=":
            self.write_token(self.advance())  # Escreve o operador
            self.parse_term()

        self.close_tag("expression")

    def parse_let(self):
        self.open_tag("letStatement")

        self.match('KEYWORD', 'let')
        self.match('IDENTIFIER')

        if self.peek() and self.peek()[1] == '[':
            self.match('SYMBOL', '[')
            self.parse_expression()
            self.match('SYMBOL', ']')

        self.match('SYMBOL', '=')
        self.parse_expression()
        self.match('SYMBOL', ';')

        self.close_tag("letStatement")

    def open_tag(self, tag_name):
        indent = "  " * self.indent_level
        self.xml_output.append(f"{indent}<{tag_name}>")
        self.indent_level += 1

    def close_tag(self, tag_name):
        self.indent_level -= 1
        indent = "  " * self.indent_level
        self.xml_output.append(f"{indent}</{tag_name}>")

    def escape_xml(self, value):
        return self.XML_ESCAPE.get(value, value)

    def write_token(self, token):
        token_type, token_value = token
        indent = "  " * self.indent_level

        if token_type not in self.TAG_MAP:
            raise ValueError(f"Tipo de token desconhecido: {token_type}")

        tag = self.TAG_MAP[token_type]
        token_value = self.escape_xml(token_value)

        self.xml_output.append(f"{indent}<{tag}> {token_value} </{tag}>")

    def get_xml(self):
        return "\n".join(self.xml_output)