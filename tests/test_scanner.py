from JackTokenizer import JackTokenizer
import os

def test_numero_basico():
    filename = "TesteNumero"

    with open(filename + ".jack", "w", encoding="utf-8") as f:
        f.write("289")

    tokenizer = JackTokenizer(filename)

    assert tokenizer.tokens[0][0] == "INT_CONST"
    assert tokenizer.tokens[0][1] == "289"

    os.remove(filename + ".jack")