import ast

def parse_python(code):
    return ast.parse(code)