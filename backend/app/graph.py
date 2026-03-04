import ast


def generate_call_graph(tree):

    call_graph = []
    functions = []
    recursive_functions = []

    class GraphAnalyzer(ast.NodeVisitor):

        def __init__(self):
            self.current_function = None

        def visit_FunctionDef(self, node):
            functions.append(node.name)
            self.current_function = node.name
            self.generic_visit(node)
            self.current_function = None

        def visit_Call(self, node):

            if isinstance(node.func, ast.Name):

                called = node.func.id

                if self.current_function:
                    call_graph.append({
                        "source": self.current_function,
                        "target": called
                    })

                if called == self.current_function:
                    recursive_functions.append(self.current_function)

            self.generic_visit(node)


    GraphAnalyzer().visit(tree)

    return functions, recursive_functions, call_graph