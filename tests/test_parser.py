import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from JackTokenizer import JackTokenizer
from parser import Parser

CURR_DIR = os.path.dirname(__file__)

def test_parse_term_integer():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "term_test")

    tokenizer = JackTokenizer(file_path)
    tokens = tokenizer.tokens

    parser = Parser(tokens)
    parser.parse_term()
    xml = parser.get_xml()

    assert "<term>" in xml
    assert "<integerConstant> 10 </integerConstant>" in xml


# Colocando o teste para expressões conforme aula
def test_parse_expression():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "expression_test")

    tokenizer = JackTokenizer(file_path)
    tokens = tokenizer.tokens

    parser = Parser(tokens)
    parser.parse_expression()
    xml = parser.get_xml()

    assert "<expression>" in xml
    assert "<symbol> + </symbol>" in xml


# Colocando o teste para letStatement conforme aula
def test_parse_let():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "let_test")

    tokenizer = JackTokenizer(file_path)
    tokens = tokenizer.tokens

    parser = Parser(tokens)
    parser.parse_let()
    xml = parser.get_xml()

    assert "<letStatement>" in xml
    assert "<keyword> let </keyword>" in xml

def test_parse_if():
    current_dir = os.path.dirname(__file__)
    # Removido a subpasta, apontando direto para o arquivo na mesma pasta
    file_path = os.path.join(current_dir, "if_test")

    tokenizer = JackTokenizer(file_path)
    parser = Parser(tokenizer.tokens)
    
    parser.parse_if()
    xml = parser.get_xml()

    # Verificações básicas de estrutura exigidas pela gramática
    assert "<ifStatement>" in xml
    assert "<keyword> if </keyword>" in xml
    assert "<keyword> else </keyword>" in xml
    assert "<symbol> { </symbol>" in xml

def test_parse_while():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "while_test")

    tokenizer = JackTokenizer(file_path)
    parser = Parser(tokenizer.tokens)
    
    parser.parse_while()
    xml = parser.get_xml()

    assert "<whileStatement>" in xml
    assert "<symbol> ( </symbol>" in xml
    assert "<symbol> ) </symbol>" in xml

def test_parse_class():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "class_test")

    tokenizer = JackTokenizer(file_path)
    parser = Parser(tokenizer.tokens)
    
    parser.parse_class() # Inicia o processo do topo
    xml = parser.get_xml()

    assert "<class>" in xml
    assert "<classVarDec>" in xml
    assert "<subroutineDec>" in xml
    assert "<subroutineBody>" in xml

def test_geracao_xml_square():

    nome_base = "Square"

    path_input = os.path.join(CURR_DIR, nome_base)
    subpasta_xml = os.path.join(CURR_DIR, "xml")

    tokenizer = JackTokenizer(path_input)
    parser = Parser(tokenizer.tokens)
    
    parser.parse_class() # Inicia o processo do topo
    xml = parser.get_xml()

    path_gabarito_oficial = os.path.join(subpasta_xml, nome_base + ".xml")

    with open(path_gabarito_oficial, "r", encoding="utf-8") as f:
        conteudo_esperado = f.read()

    assert xml == conteudo_esperado

def test_geracao_xml_main():

    nome_base = "Main"

    path_input = os.path.join(CURR_DIR, nome_base)
    subpasta_xml = os.path.join(CURR_DIR, "xml")

    tokenizer = JackTokenizer(path_input)
    parser = Parser(tokenizer.tokens)
    
    parser.parse_class() # Inicia o processo do topo
    xml = parser.get_xml()

    path_gabarito_oficial = os.path.join(subpasta_xml, nome_base + ".xml")

    with open(path_gabarito_oficial, "r", encoding="utf-8") as f:
        conteudo_esperado = f.read()

    assert xml == conteudo_esperado

def test_geracao_xml_square_game():

    nome_base = "SquareGame"

    path_input = os.path.join(CURR_DIR, nome_base)
    subpasta_xml = os.path.join(CURR_DIR, "xml")

    tokenizer = JackTokenizer(path_input)
    parser = Parser(tokenizer.tokens)
    
    parser.parse_class() # Inicia o processo do topo
    xml = parser.get_xml()

    path_gabarito_oficial = os.path.join(subpasta_xml, nome_base + ".xml")

    with open(path_gabarito_oficial, "r", encoding="utf-8") as f:
        conteudo_esperado = f.read()

    assert xml == conteudo_esperado