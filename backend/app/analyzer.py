import ast
from app.complexity import detect_complexity
from app.graph import generate_call_graph
from app.patterns import detect_patterns

def analyze_code(code: str):

    tree = ast.parse(code)

    complexity, loop_depth = detect_complexity(tree)

    functions, recursive_functions, call_graph = generate_call_graph(tree)

    patterns = detect_patterns(tree)

    return {
        "functions": functions,
        "recursive_functions": recursive_functions,
        "loop_depth": loop_depth,
        "call_graph": call_graph,
        "patterns": patterns,
        "estimated_complexity": complexity
    }