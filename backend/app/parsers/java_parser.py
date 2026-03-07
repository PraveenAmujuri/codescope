from tree_sitter_languages import get_parser

def parse_java(code):

    parser = get_parser("java")
    tree = parser.parse(bytes(code, "utf8"))

    return tree