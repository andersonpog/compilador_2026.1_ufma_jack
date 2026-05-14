import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from JackTokenizer import JackTokenizer
from parser import Parser


def test_simple_functions(tmp_path):
    input_code = """
    class Main {

        function int soma(int x, int y) {
            return 30;
        }

        function void main() {
            var int d;
            return;
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

    expected = """function Main.soma 0
push constant 30
return
function Main.main 1
push constant 0
return
"""

    assert actual == expected