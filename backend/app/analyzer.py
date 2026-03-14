from app.parsers.parser_router import parse_code
from app.treesitter_analyzer import analyze_treesitter 
import ast

def analyze_python_advanced(tree):
    stats = {
        "loop_depth": 0,
        "patterns": set(),
        "functions": [],
        "recursive_functions": [],
        "heatmap": [],
        "complexity_override": None
    }

    def is_recursive_python(node, func_name):
        for child in ast.walk(node):
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                if child.func.id == func_name:
                    return True
        return False

    # Recursive walker for Python AST
    def walk_python(node, current_depth, current_func=None):
        # 1. Track Functions & Recursion
        if isinstance(node, ast.FunctionDef):
            stats["functions"].append(node.name)
            current_func = node.name
            if is_recursive_python(node, node.name):
                stats["recursive_functions"].append(node.name)
                stats["patterns"].add("Recursion")

        # 2. Loop Analysis & Heatmap
        if isinstance(node, (ast.For, ast.While)):
            current_depth += 1
            stats["loop_depth"] = max(stats["loop_depth"], current_depth)
            
            stats["heatmap"].append({
                "line": node.lineno,
                "severity": "medium" if current_depth <= 1 else "high",
                "message": f"Loop detected (Depth: {current_depth})"
            })

            # 3. Advanced Pattern Scoring (Structural)
            # Detect Backtracking: Recursion inside a loop
            if current_func and is_recursive_python(node, current_func):
                stats["patterns"].add("Backtracking")
                stats["complexity_override"] = "O(2^n) or O(n!)"

            # Detect Sliding Window / Two Pointer logic
            # (Checking for index modifications or comparisons)
            for child in ast.walk(node):
                if isinstance(child, ast.BinOp) and isinstance(child.op, (ast.Add, ast.Sub)):
                    if not "Backtracking" in stats["patterns"]:
                        stats["patterns"].add("Sliding Window")

        for child in ast.iter_child_nodes(node):
            walk_python(child, current_depth, current_func)

    walk_python(tree, 0)
    
    # Complexity Calculation
    depth = stats["loop_depth"]

    # Recursion without loops → O(n)
    if stats["recursive_functions"] and depth == 0:
        complexity = "O(n)"
    else:
        complexity = stats["complexity_override"] or (
            "O(1)" if depth == 0 else "O(n)" if depth == 1 else f"O(n^{depth})"
        )

    return {
        "loop_depth": depth,
        "estimated_complexity": complexity,
        "patterns": list(stats["patterns"]),
        "functions": stats["functions"],
        "recursive_functions": stats["recursive_functions"],
        "heatmap": stats["heatmap"]
    }

# def analyze_code(code: str, language="python"):
#     tree, lang_obj = parse_code(code, language)

#     if language == "python":
#         return analyze_python_advanced(tree)
#     else:
#         return analyze_treesitter(tree, lang_obj)
from app.graph import generate_python_flow, format_treesitter_flow

def analyze_code(code: str, language="python"):
    tree, lang_obj = parse_code(code, language)

    if language == "python":
        analysis = analyze_python_advanced(tree)
        # Python uses the visitor in graph.py
        analysis["flow_data"] = generate_python_flow(tree)
        return analysis
    else:
        # Tree-sitter (C++, Java, JS) already built flow_data internally
        analysis = analyze_treesitter(tree, lang_obj)
        # Just ensure the key exists for the frontend
        if "flow_data" not in analysis:
            analysis["flow_data"] = {"nodes": [], "edges": []}
        return analysis
    