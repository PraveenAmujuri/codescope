import ast


def analyze_code(code: str):
    tree = ast.parse(code)

    functions = []
    recursive_functions = []
    max_loop_depth = 0

    class Analyzer(ast.NodeVisitor):
        def __init__(self):
            self.current_function = None
            self.depth = 0

        def visit_FunctionDef(self, node):
            functions.append(node.name)
            self.current_function = node.name
            self.generic_visit(node)
            self.current_function = None

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name):
                if node.func.id == self.current_function:
                    recursive_functions.append(self.current_function)
            self.generic_visit(node)

        def visit_For(self, node):
            self.depth += 1
            global max_loop_depth
            max_loop_depth = max(max_loop_depth, self.depth)
            self.generic_visit(node)
            self.depth -= 1

        def visit_While(self, node):
            self.depth += 1
            global max_loop_depth
            max_loop_depth = max(max_loop_depth, self.depth)
            self.generic_visit(node)
            self.depth -= 1


    analyzer = Analyzer()
    analyzer.visit(tree)

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
        "functions": functions,
        "recursive_functions": recursive_functions,
        "loop_depth": max_loop_depth,
        "estimated_complexity": complexity
    }