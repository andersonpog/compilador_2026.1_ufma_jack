from parser import Parser


def test_if_com_else():
    tokens = [
        ("KEYWORD", "if"),
        ("SYMBOL", "("),
        ("KEYWORD", "false"),
        ("SYMBOL", ")"),

        ("SYMBOL", "{"),
        ("KEYWORD", "return"),
        ("INT_CONST", "10"),
        ("SYMBOL", ";"),
        ("SYMBOL", "}"),

        ("KEYWORD", "else"),

        ("SYMBOL", "{"),
        ("KEYWORD", "return"),
        ("INT_CONST", "20"),
        ("SYMBOL", ";"),
        ("SYMBOL", "}"),
    ]

    parser = Parser(tokens)

    parser.parse_if()

    actual = parser.get_vm_output()

    expected = (
        "push constant 0\n"
        "if-goto IF_TRUE0\n"
        "goto IF_FALSE0\n"
        "label IF_TRUE0\n"
        "push constant 10\n"
        "return\n"
        "goto IF_END0\n"
        "label IF_FALSE0\n"
        "push constant 20\n"
        "return\n"
        "label IF_END0\n"
    )

    assert actual == expected