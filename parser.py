from VMWriter import VMWriter, Segment, Command
from symbol_table import SymbolTable, Kind


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

        self.vmWriter = VMWriter()
        self.symbol_table = SymbolTable()

        self.class_name = ""

        self.if_label_num = 0
        self.while_label_num = 0

    def kind_to_segment(self, kind):
        if kind == Kind.STATIC:
            return Segment.STATIC
        if kind == Kind.FIELD:
            return Segment.THIS
        if kind == Kind.VAR:
            return Segment.LOCAL
        if kind == Kind.ARG:
            return Segment.ARG

        return None

    def peek(self):
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None

    def peek_next(self):
        if self.current + 1 < len(self.tokens):
            return self.tokens[self.current + 1]
        return None

    def advance(self):
        token = self.peek()
        if token is not None:
            self.current += 1
        return token

    def match(self, expected_type, expected_value=None):
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
            self.vmWriter.writePush(Segment.CONST, int(token_value))

        elif token_type == 'STR_CONST':
            self.write_token(self.advance())

        elif token_type == 'KEYWORD' and token_value in ['true', 'false', 'null', 'this']:
            self.write_token(self.advance())

            if token_value == 'true':
                self.vmWriter.writePush(Segment.CONST, 0)
                self.vmWriter.writeArithmetic(Command.NOT)

            elif token_value == 'false' or token_value == 'null':
                self.vmWriter.writePush(Segment.CONST, 0)

            elif token_value == 'this':
                self.vmWriter.writePush(Segment.POINTER, 0)

        elif token_value == '(':
            self.match('SYMBOL', '(')
            self.parse_expression()
            self.match('SYMBOL', ')')

        elif token_value in ['-', '~']:
            self.match('SYMBOL', token_value)
            self.parse_term()

            if token_value == '-':
                self.vmWriter.writeArithmetic(Command.NEG)
            elif token_value == '~':
                self.vmWriter.writeArithmetic(Command.NOT)

        elif token_type == 'IDENTIFIER':
            name = token_value
            self.write_token(self.advance())

            if self.peek() and self.peek()[1] in ['(', '.']:
                if self.peek()[1] == '.':
                    self.match('SYMBOL', '.')
                    self.match('IDENTIFIER')

                self.match('SYMBOL', '(')
                self.parse_expression_list()
                self.match('SYMBOL', ')')

            else:
                if self.peek() and self.peek()[1] == '[':
                    self.match('SYMBOL', '[')
                    self.parse_expression()
                    self.match('SYMBOL', ']')

                else:
                    symbol = self.symbol_table.resolve(name)

                    if symbol is not None:
                        segment = self.kind_to_segment(symbol.kind)
                        self.vmWriter.writePush(segment, symbol.index)

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

        class_name_token = self.match('IDENTIFIER')
        self.class_name = class_name_token[1]

        self.match('SYMBOL', '{')

        while self.peek() and self.peek()[1] in ['static', 'field']:
            self.parse_class_var_dec()

        while self.peek() and self.peek()[1] in ['constructor', 'function', 'method']:
            self.parse_subroutine()

        self.match('SYMBOL', '}')
        self.close_tag("class")

    def parse_class_var_dec(self):
        self.open_tag("classVarDec")

        kind_token = self.match('KEYWORD')
        kind_value = kind_token[1]

        if kind_value == 'static':
            kind = Kind.STATIC
        else:
            kind = Kind.FIELD

        type_token = self.match('KEYWORD' if self.peek()[0] == 'KEYWORD' else 'IDENTIFIER')
        type_ = type_token[1]

        name_token = self.match('IDENTIFIER')
        name = name_token[1]

        self.symbol_table.define(name, type_, kind)

        while self.peek() and self.peek()[1] == ',':
            self.match('SYMBOL', ',')

            name_token = self.match('IDENTIFIER')
            name = name_token[1]

            self.symbol_table.define(name, type_, kind)

        self.match('SYMBOL', ';')
        self.close_tag("classVarDec")

    def parse_subroutine(self):
        self.open_tag("subroutineDec")

        self.if_label_num = 0
        self.while_label_num = 0

        self.symbol_table.start_subroutine()

        subroutine_type_token = self.match('KEYWORD')
        subroutine_type = subroutine_type_token[1]

        if subroutine_type == 'method':
            self.symbol_table.define("this", self.class_name, Kind.ARG)

        self.match('KEYWORD' if self.peek()[0] == 'KEYWORD' else 'IDENTIFIER')

        subroutine_name_token = self.match('IDENTIFIER')
        subroutine_name = subroutine_name_token[1]

        function_name = f"{self.class_name}.{subroutine_name}"

        self.match('SYMBOL', '(')
        self.parse_parameter_list()
        self.match('SYMBOL', ')')

        self.open_tag("subroutineBody")
        self.match('SYMBOL', '{')

        num_locals = 0

        while self.peek() and self.peek()[1] == 'var':
            num_locals += self.parse_var_dec()

        self.vmWriter.writeFunction(function_name, num_locals)

        self.parse_statements()

        self.match('SYMBOL', '}')
        self.close_tag("subroutineBody")
        self.close_tag("subroutineDec")

    def parse_var_dec(self):
        self.open_tag("varDec")

        self.match('KEYWORD', 'var')
        kind = Kind.VAR
        count = 0

        type_token = self.match('KEYWORD' if self.peek()[0] == 'KEYWORD' else 'IDENTIFIER')
        type_ = type_token[1]

        name_token = self.match('IDENTIFIER')
        name = name_token[1]

        self.symbol_table.define(name, type_, kind)
        count += 1

        while self.peek() and self.peek()[1] == ',':
            self.match('SYMBOL', ',')

            name_token = self.match('IDENTIFIER')
            name = name_token[1]

            self.symbol_table.define(name, type_, kind)
            count += 1

        self.match('SYMBOL', ';')
        self.close_tag("varDec")

        return count

    def parse_parameter_list(self):
        self.open_tag("parameterList")

        kind = Kind.ARG

        if self.peek() and self.peek()[1] != ')':
            type_token = self.match('KEYWORD' if self.peek()[0] == 'KEYWORD' else 'IDENTIFIER')
            type_ = type_token[1]

            name_token = self.match('IDENTIFIER')
            name = name_token[1]

            self.symbol_table.define(name, type_, kind)

            while self.peek() and self.peek()[1] == ',':
                self.match('SYMBOL', ',')

                type_token = self.match('KEYWORD' if self.peek()[0] == 'KEYWORD' else 'IDENTIFIER')
                type_ = type_token[1]

                name_token = self.match('IDENTIFIER')
                name = name_token[1]

                self.symbol_table.define(name, type_, kind)

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

        label_true = f"IF_TRUE{self.if_label_num}"
        label_false = f"IF_FALSE{self.if_label_num}"
        label_end = f"IF_END{self.if_label_num}"
        self.if_label_num += 1

        self.match('KEYWORD', 'if')
        self.match('SYMBOL', '(')
        self.parse_expression()
        self.match('SYMBOL', ')')

        self.vmWriter.writeIf(label_true)
        self.vmWriter.writeGoto(label_false)
        self.vmWriter.writeLabel(label_true)

        self.match('SYMBOL', '{')
        self.parse_statements()
        self.match('SYMBOL', '}')

        if self.peek() and self.peek()[1] == 'else':
            self.vmWriter.writeGoto(label_end)
            self.vmWriter.writeLabel(label_false)

            self.match('KEYWORD', 'else')
            self.match('SYMBOL', '{')
            self.parse_statements()
            self.match('SYMBOL', '}')

            self.vmWriter.writeLabel(label_end)
        else:
            self.vmWriter.writeLabel(label_false)

        self.close_tag("ifStatement")

    def parse_while(self):
        self.open_tag("whileStatement")

        label_exp = f"WHILE_EXP{self.while_label_num}"
        label_end = f"WHILE_END{self.while_label_num}"
        self.while_label_num += 1

        self.vmWriter.writeLabel(label_exp)

        self.match('KEYWORD', 'while')
        self.match('SYMBOL', '(')
        self.parse_expression()

        self.vmWriter.writeArithmetic(Command.NOT)
        self.vmWriter.writeIf(label_end)

        self.match('SYMBOL', ')')
        self.match('SYMBOL', '{')
        self.parse_statements()

        self.vmWriter.writeGoto(label_exp)
        self.vmWriter.writeLabel(label_end)

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

        name_token = self.match('IDENTIFIER')
        var_name = name_token[1]

        is_array = False

        if self.peek() and self.peek()[1] == '[':
            is_array = True
            self.match('SYMBOL', '[')
            self.parse_expression()
            self.match('SYMBOL', ']')

        self.match('SYMBOL', '=')
        self.parse_expression()
        self.match('SYMBOL', ';')

        if not is_array:
            symbol = self.symbol_table.resolve(var_name)

            if symbol is not None:
                segment = self.kind_to_segment(symbol.kind)
                self.vmWriter.writePop(segment, symbol.index)

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