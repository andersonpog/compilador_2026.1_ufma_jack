import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from JackTokenizer import JackTokenizer
from parser import Parser


def test_funcao_simples_com_variavel(tmp_path):
    input_code = """
    class Main {

        function int funcao() {
            var int d;
            return d;
        }
    }
    """

    jack_file = tmp_path / "Main.jack"
    jack_file.write_text(input_code)

    filename_without_extension = str(jack_file.with_suffix(""))

    tokenizer = JackTokenizer(filename_without_extension)
    tokens = tokenizer.tokens

    parser = Parser(tokens)
    parser.parse_class()

    actual = parser.get_vm_output()

    expected = """function Main.funcao 1
push local 0
return
"""

    assert actual == expected