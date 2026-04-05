import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from JackTokenizer import JackTokenizer
from TokenToXML import generate_xml

CURR_DIR = os.path.dirname(__file__)


def test_numero_basico():
    filename = "TesteNumero"

    with open(filename + ".jack", "w", encoding="utf-8") as f:
        f.write("289")

    tokenizer = JackTokenizer(filename)

    assert tokenizer.tokens[0][0] == "INT_CONST"
    assert tokenizer.tokens[0][1] == "289"

    os.remove(filename + ".jack")


# Teste com múltiplos números (material da aula)
def test_multiplos_numeros():
    casos = [
        ("0", "0"),
        ("289", "289"),
        ("42", "42"),
        ("  123  ", "123"),  # com espaços
    ]

    for i, (entrada, esperado) in enumerate(casos):
        filename = f"TesteNumero_{i}"

        with open(filename + ".jack", "w", encoding="utf-8") as f:
            f.write(entrada)

        tokenizer = JackTokenizer(filename)

        assert tokenizer.tokens[0][0] == "INT_CONST"
        assert tokenizer.tokens[0][1] == esperado

        os.remove(filename + ".jack")


# Teste dois do material da aula, teste com string
def test_string_basica():
    filename = "TesteString"

    with open(filename + ".jack", "w", encoding="utf-8") as f:
        f.write('"hello"')

    tokenizer = JackTokenizer(filename)

    assert tokenizer.tokens[0][0] == "STR_CONST"
    assert tokenizer.tokens[0][1] == "hello"

    os.remove(filename + ".jack")

def test_string_vazia():
    filename = "TesteStringVazia"

    with open(filename + ".jack", "w", encoding="utf-8") as f:
        f.write('""')

    tokenizer = JackTokenizer(filename)

    assert tokenizer.tokens[0][0] == "STR_CONST"
    assert tokenizer.tokens[0][1] == ""

    os.remove(filename + ".jack")
def test_identificador_e_keyword():
    # Teste com identificador comum
    filename_id = "TesteIdentificador"

    with open(filename_id + ".jack", "w", encoding="utf-8") as f:
        f.write("minhaVar123")

    tokenizer = JackTokenizer(filename_id)

    assert tokenizer.tokens[0][0] == "IDENTIFIER"
    assert tokenizer.tokens[0][1] == "minhaVar123"

    os.remove(filename_id + ".jack")

    # Teste com palavra reservada
    filename_kw = "TesteKeyword"

    with open(filename_kw + ".jack", "w", encoding="utf-8") as f:
        f.write("function")

    tokenizer = JackTokenizer(filename_kw)

    assert tokenizer.tokens[0][0] == "KEYWORD"
    assert tokenizer.tokens[0][1] == "function"

    os.remove(filename_kw + ".jack")

def test_geracao_xml_square():

    nome_base = "Square"

    path_input = os.path.join(CURR_DIR, nome_base)
    subpasta_txml = os.path.join(CURR_DIR, "txml")

    path_resultado_gerado = os.path.join(CURR_DIR, nome_base + "T.xml")
    path_gabarito_oficial = os.path.join(subpasta_txml, nome_base + "T_GABARITO.xml")


    generate_xml(path_input)


    with open(path_resultado_gerado, "r", encoding="utf-8") as f:
        conteudo_gerado = f.read()

    with open(path_gabarito_oficial, "r", encoding="utf-8") as f:
        conteudo_esperado = f.read()

    assert conteudo_gerado == conteudo_esperado

    os.remove(path_resultado_gerado)