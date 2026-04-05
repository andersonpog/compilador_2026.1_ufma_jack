import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from JackTokenizer import JackTokenizer


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