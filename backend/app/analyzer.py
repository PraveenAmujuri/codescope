import ast


def analyze_code(code: str):
    tree = ast.parse(code)

    loops = 0
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While)):
            loops += 1

        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)

    complexity = "O(n)"

    if loops >= 2:
        complexity = "O(n²)"

    return {
        "loops": loops,
        "functions": functions,
        "estimated_complexity": complexity
    }