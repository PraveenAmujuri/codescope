import ast


def detect_complexity(tree):

    max_loop_depth = 0

    class LoopAnalyzer(ast.NodeVisitor):

        def __init__(self):
            self.depth = 0

        def visit_For(self, node):
            nonlocal max_loop_depth
            self.depth += 1
            max_loop_depth = max(max_loop_depth, self.depth)
            self.generic_visit(node)
            self.depth -= 1

        def visit_While(self, node):
            nonlocal max_loop_depth
            self.depth += 1
            max_loop_depth = max(max_loop_depth, self.depth)
            self.generic_visit(node)
            self.depth -= 1


    LoopAnalyzer().visit(tree)

    if max_loop_depth == 0:
        return "O(1)", max_loop_depth
    elif max_loop_depth == 1:
        return "O(n)", max_loop_depth
    elif max_loop_depth == 2:
        return "O(n²)", max_loop_depth
    else:
        return f"O(n^{max_loop_depth})", max_loop_depth