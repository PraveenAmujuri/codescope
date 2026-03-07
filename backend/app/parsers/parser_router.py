from tree_sitter_languages import get_language, get_parser
import ast

def parse_code(code, language):
    if language == "python":
        return ast.parse(code), None
    
    # Standardize language names for tree-sitter
    ts_map = {"js": "javascript", "cpp": "cpp", "java": "java", "javascript": "javascript"}
    target_lang = ts_map.get(language, language)
    
    lang_obj = get_language(target_lang)
    parser = get_parser(target_lang)
    tree = parser.parse(bytes(code, "utf8"))
    
    return tree, lang_obj