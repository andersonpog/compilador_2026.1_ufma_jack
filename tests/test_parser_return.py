from parser import Parser


def test_return_sem_expressao():
    tokens = [
        ("KEYWORD", "return"),
        ("SYMBOL", ";")
    ]

    parser = Parser(tokens)
    parser.parse_return()

    actual = parser.get_vm_output()

    expected = "push constant 0\nreturn\n"

    assert actual == expected


def test_return_com_expressao():
    tokens = [
        ("KEYWORD", "return"),
        ("INT_CONST", "10"),
        ("SYMBOL", ";")
    ]

    parser = Parser(tokens)
    parser.parse_return()

    actual = parser.get_vm_output()

    expected = "push constant 10\nreturn\n"

    assert actual == expected