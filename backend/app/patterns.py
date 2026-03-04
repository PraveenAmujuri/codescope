import ast


def detect_patterns(tree):

    patterns = []

    class PatternAnalyzer(ast.NodeVisitor):

        def visit_For(self, node):

            has_start = False
            has_end = False

            for child in ast.walk(node):

                if isinstance(child, ast.Name):
                    if child.id in ["start", "left"]:
                        has_start = True
                    if child.id in ["end", "right"]:
                        has_end = True

            if has_start and has_end:
                patterns.append("Sliding Window")
            else:
                patterns.append("Linear Iteration")

            self.generic_visit(node)


        def visit_While(self, node):

            has_left = False
            has_right = False
            has_mid = False

            for child in ast.walk(node):

                if isinstance(child, ast.Name):

                    if child.id == "left":
                        has_left = True

                    if child.id == "right":
                        has_right = True

                    if child.id == "mid":
                        has_mid = True

            if has_left and has_right and has_mid:
                patterns.append("Binary Search")

            elif has_left and has_right:
                patterns.append("Two Pointer")

            self.generic_visit(node)


        def visit_FunctionDef(self, node):

            recursive_calls = 0

            for child in ast.walk(node):

                if isinstance(child, ast.Call):

                    if isinstance(child.func, ast.Name):

                        if child.func.id == node.name:
                            recursive_calls += 1

            if recursive_calls >= 2:
                patterns.append("Divide and Conquer")

            self.generic_visit(node)


    PatternAnalyzer().visit(tree)

    return list(set(patterns))