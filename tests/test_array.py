import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from JackTokenizer import JackTokenizer
from parser import Parser


def test_array(tmp_path):
    input_code = """
    class Main {
        function void main () {
            var Array v;
            let v[2] = v[3] + 42;
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

    expected = """function Main.main 1
push constant 2
push local 0
add
push constant 3
push local 0
add
pop pointer 1
push that 0
push constant 42
add
pop temp 0
pop pointer 1
push temp 0
pop that 0
push constant 0
return
"""

    assert actual == expected