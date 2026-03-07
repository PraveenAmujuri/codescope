from tree_sitter_languages import get_parser

def parse_js(code):

    parser = get_parser("javascript")
    tree = parser.parse(bytes(code, "utf8"))

    return tree