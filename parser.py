from VMWriter import VMWriter, Segment


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

        # Integração inicial com o gerador VM
        self.vmWriter = VMWriter()

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

        # 1. Constantes e Palavras-chave
        if token_type == 'INT_CONST':
            self.write_token(self.advance())
            self.vmWriter.writePush(Segment.CONST, int(token_value))

        elif token_type == 'STR_CONST':
            self.write_token(self.advance())

        elif token_type == 'KEYWORD' and token_value in ['true', 'false', 'null', 'this']:
            self.write_token(self.advance())

        # 2. Expressões entre parênteses: ( expression )
        elif token_value == '(':
            self.match('SYMBOL', '(')
            self.parse_expression()
            self.match('SYMBOL', ')')

        # 3. Operadores Unários: -x ou ~y
        elif token_value in ['-', '~']:
            self.match('SYMBOL', token_value)
            self.parse_term()

        # 4. Identificadores (Variáveis, Arrays ou Chamadas de Função)
        elif token_type == 'IDENTIFIER':
            self.write_token(self.advance())

            # Caso seja um Array: varName[expression]
            if self.peek() and self.peek()[1] == '[':
                self.match('SYMBOL', '[')
                self.parse_expression()
                self.match('SYMBOL', ']')

            # Caso seja uma chamada de método/função no meio de expressão
            elif self.peek() and self.peek()[1] in ['(', '.']:
                if self.peek()[1] == '.':
                    self.match('SYMBOL', '.')
                    self.match('IDENTIFIER')
                self.match('SYMBOL', '(')
                self.parse_expression_list()
                self.match('SYMBOL', ')')

        else:
            raise SyntaxError(f"Termo esperado, encontrado: {token_value}")

        self.close_tag("term")

    def parse_expression(self):
        self.open_tag("expression")
        self.parse_term()

        while self.peek() and self.peek()[1] in "+-*/&|<>=":
            self.write_token(self.advance())
            self.parse_term()

        self.close_tag("expression")

    def parse_expression_list(self):
        self.open_tag("expressionList")

        if self.peek() and self.peek()[1] != ')':
            self.parse_expression()

            while self.peek() and self.peek()[1] == ',':
                self.match('SYMBOL', ',')
                self.parse_expression()

        self.close_tag("expressionList")

    def parse_class(self):
        self.open_tag("class")
        self.match('KEYWORD', 'class')
        self.match('IDENTIFIER')
        self.match('SYMBOL', '{')

        while self.peek() and self.peek()[1] in ['static', 'field']:
            self.parse_class_var_dec()

        while self.peek() and self.peek()[1] in ['constructor', 'function', 'method']:
            self.parse_subroutine()

        self.match('SYMBOL', '}')
        self.close_tag("class")

    def parse_class_var_dec(self):
        self.open_tag("classVarDec")
        self.match('KEYWORD')
        self.match('KEYWORD' if self.peek()[0] == 'KEYWORD' else 'IDENTIFIER')
        self.match('IDENTIFIER')

        while self.peek() and self.peek()[1] == ',':
            self.match('SYMBOL', ',')
            self.match('IDENTIFIER')

        self.match('SYMBOL', ';')
        self.close_tag("classVarDec")

    def parse_subroutine(self):
        self.open_tag("subroutineDec")
        self.match('KEYWORD')
        self.match('KEYWORD' if self.peek()[0] == 'KEYWORD' else 'IDENTIFIER')
        self.match('IDENTIFIER')
        self.match('SYMBOL', '(')
        self.parse_parameter_list()
        self.match('SYMBOL', ')')

        self.open_tag("subroutineBody")
        self.match('SYMBOL', '{')

        while self.peek() and self.peek()[1] == 'var':
            self.parse_var_dec()

        self.parse_statements()

        self.match('SYMBOL', '}')
        self.close_tag("subroutineBody")
        self.close_tag("subroutineDec")

    def parse_var_dec(self):
        self.open_tag("varDec")
        self.match('KEYWORD', 'var')

        self.match('KEYWORD' if self.peek()[0] == 'KEYWORD' else 'IDENTIFIER')
        self.match('IDENTIFIER')

        while self.peek() and self.peek()[1] == ',':
            self.match('SYMBOL', ',')
            self.match('IDENTIFIER')

        self.match('SYMBOL', ';')
        self.close_tag("varDec")

    def parse_parameter_list(self):
        self.open_tag("parameterList")

        if self.peek() and self.peek()[1] != ')':
            self.match('KEYWORD' if self.peek()[0] == 'KEYWORD' else 'IDENTIFIER')
            self.match('IDENTIFIER')

            while self.peek() and self.peek()[1] == ',':
                self.match('SYMBOL', ',')
                self.match('KEYWORD' if self.peek()[0] == 'KEYWORD' else 'IDENTIFIER')
                self.match('IDENTIFIER')

        self.close_tag("parameterList")

    def parse_statements(self):
        self.open_tag("statements")

        while self.peek() and self.peek()[1] in ['let', 'if', 'while', 'do', 'return']:
            val = self.peek()[1]

            if val == 'let':
                self.parse_let()
            elif val == 'if':
                self.parse_if()
            elif val == 'while':
                self.parse_while()
            elif val == 'do':
                self.parse_do()
            elif val == 'return':
                self.parse_return()

        self.close_tag("statements")

    def parse_if(self):
        self.open_tag("ifStatement")
        self.match('KEYWORD', 'if')
        self.match('SYMBOL', '(')
        self.parse_expression()
        self.match('SYMBOL', ')')
        self.match('SYMBOL', '{')
        self.parse_statements()
        self.match('SYMBOL', '}')

        if self.peek() and self.peek()[1] == 'else':
            self.match('KEYWORD', 'else')
            self.match('SYMBOL', '{')
            self.parse_statements()
            self.match('SYMBOL', '}')

        self.close_tag("ifStatement")

    def parse_while(self):
        self.open_tag("whileStatement")
        self.match('KEYWORD', 'while')
        self.match('SYMBOL', '(')
        self.parse_expression()
        self.match('SYMBOL', ')')
        self.match('SYMBOL', '{')
        self.parse_statements()
        self.match('SYMBOL', '}')
        self.close_tag("whileStatement")

    def parse_do(self):
        self.open_tag("doStatement")
        self.match('KEYWORD', 'do')

        self.match('IDENTIFIER')

        if self.peek() and self.peek()[1] == '.':
            self.match('SYMBOL', '.')
            self.match('IDENTIFIER')

        self.match('SYMBOL', '(')
        self.parse_expression_list()
        self.match('SYMBOL', ')')

        self.match('SYMBOL', ';')
        self.close_tag("doStatement")

    def parse_return(self):
        self.open_tag("returnStatement")
        self.match('KEYWORD', 'return')

        if self.peek() and self.peek()[1] != ';':
            self.parse_expression()
        else:
            self.vmWriter.writePush(Segment.CONST, 0)

        self.match('SYMBOL', ';')

        self.vmWriter.writeReturn()

        self.close_tag("returnStatement")

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
        return "\n".join(self.xml_output) + "\n"

    def get_vm_output(self):
        return self.vmWriter.vmOutput()