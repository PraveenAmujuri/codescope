def analyze_code(code: str, language="python"):
    tree = parse_code(code, language)
    
    if language == "python":
        # Keep your existing AST logic
        return analyze_python_ast(tree)
    else:
        # Use Tree-sitter Query logic for others
        return analyze_treesitter_generic(tree, language)