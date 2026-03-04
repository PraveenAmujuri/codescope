import ast


def generate_heatmap(tree):

    heatmap = []

    class HeatmapAnalyzer(ast.NodeVisitor):

        def visit_For(self, node):

            heatmap.append({
                "line": node.lineno,
                "severity": "medium",
                "message": "Loop detected (O(n))"
            })

            self.generic_visit(node)


        def visit_While(self, node):

            heatmap.append({
                "line": node.lineno,
                "severity": "medium",
                "message": "While loop detected"
            })

            self.generic_visit(node)


        def visit_Call(self, node):

            if isinstance(node.func, ast.Name):

                if node.func.id in ["sort", "sorted"]:

                    heatmap.append({
                        "line": node.lineno,
                        "severity": "low",
                        "message": "Sorting operation (O(n log n))"
                    })

            self.generic_visit(node)


        def visit_FunctionDef(self, node):

            for child in ast.walk(node):

                if isinstance(child, ast.Call):

                    if isinstance(child.func, ast.Name):

                        if child.func.id == node.name:

                            heatmap.append({
                                "line": node.lineno,
                                "severity": "high",
                                "message": "Recursive function"
                            })

            self.generic_visit(node)


    HeatmapAnalyzer().visit(tree)

    return heatmap