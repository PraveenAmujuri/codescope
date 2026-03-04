import ast


def analyze_code(code: str):
    tree = ast.parse(code)

    functions = []
    max_loop_depth = 0

    def visit(node, depth=0):
        nonlocal max_loop_depth

        if isinstance(node, (ast.For, ast.While)):
            depth += 1
            max_loop_depth = max(max_loop_depth, depth)

        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)

        for child in ast.iter_child_nodes(node):
            visit(child, depth)

    visit(tree)

    # Complexity estimation
    if max_loop_depth == 0:
        complexity = "O(1)"
    elif max_loop_depth == 1:
        complexity = "O(n)"
    elif max_loop_depth == 2:
        complexity = "O(n²)"
    elif max_loop_depth == 3:
        complexity = "O(n³)"
    else:
        complexity = f"O(n^{max_loop_depth})"

    return {
        "loop_depth": max_loop_depth,
        "functions": functions,
        "estimated_complexity": complexity
    }