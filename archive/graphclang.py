import clang.cindex
clang.cindex.Config.set_library_file('/usr/local/opt/llvm/lib/libclang.dylib')

def find_binary_operator(cursor):
    """Extract the actual operator from a BINARY_OPERATOR cursor"""
    if cursor.kind != clang.cindex.CursorKind.BINARY_OPERATOR:
        return None
        
    tokens = list(cursor.get_tokens())
    
    # Common binary operators (order matters for multi-char operators)
    operators = ['==', '!=', '<=', '>=', '<<', '>>', '&&', '||', 
                '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=',
                '<', '>', '+', '-', '*', '/', '%', '&', '|', '^', '=']
    
    # Look for multi-character operators first
    for i in range(len(tokens) - 1):
        two_char = tokens[i].spelling + tokens[i + 1].spelling
        if two_char in operators:
            return two_char
    
    # Then look for single-character operators
    for token in tokens:
        if token.spelling in operators:
            return token.spelling
    
    return None

def analyze_dependencies(filename):
    index = clang.cindex.Index.create()
    tu = index.parse(filename)
    
    data_deps = []
    compute_deps = []
    control_deps = []
    what_when = []

    
    def visit_node(node, indent=0):

        # print("\n***********************************")
        # if node.pretty_printed:
        #     try:
        #         node.pretty_printed()
        #     except Exception as e:
        #         print(f"Error pretty printing node: {e}")

        print(f"{node.location.line}:{node.location.column}{' ' * indent}Visiting node: nk {node.kind} - ns {node.spelling} - nd {node.displayname}  ")
        # print(dir(node))
        # print("***********************************")

        if node.kind == clang.cindex.CursorKind.INTEGER_LITERAL:
            print(f"Integer literal found: {node.spelling} at {node.location.line}:{node.location.column}")
            tokens = list(node.get_tokens())
            if tokens:
                print(f"Token text: {tokens[0].spelling}")

        if node.kind == clang.cindex.CursorKind.BINARY_OPERATOR:
            operator = find_binary_operator(node)
            print(f"Binary operator found: '{operator}' (spelling: '{node.spelling}') at {node.location.line}:{node.location.column}")
            tokens = list(node.get_tokens())
            if tokens:
                print(f"All tokens: {[t.spelling for t in tokens]}")
                print(f"Extracted operator: {operator}")
                what_when.append({'action':'bin_op', 'operation': operator, 'when': f"{node.location.line}:{node.location.column}"})

        if node.kind == clang.cindex.CursorKind.CONDITIONAL_OPERATOR:
            print(f"Conditional operator found: {node.spelling} at {node.location.line}:{node.location.column}")
            tokens = list(node.get_tokens())
            if tokens:
                print(f"Token text: {[t.spelling for t in tokens]}")

        # Check for data dependencies
        if node.kind == clang.cindex.CursorKind.VAR_DECL:
            data_deps.append(node.spelling)
            what_when.append({'action':'declared', 'var': node.spelling, 'when': f"{node.location.line}:{node.location.column}"})
            
        # Check for compute dependencies
        elif node.kind == clang.cindex.CursorKind.CALL_EXPR:
            compute_deps.append(node.spelling)
            
        # Check for control flow
        elif node.kind in [clang.cindex.CursorKind.IF_STMT, 
                         clang.cindex.CursorKind.FOR_STMT,
                         clang.cindex.CursorKind.WHILE_STMT]:
            print(f"Control flow statement found: {node.spelling} at {node.location.line}:{node.location.column}")
            control_deps.append(node.spelling)
            
        for child in node.get_children():
            visit_node(child, indent + 4)
            
    visit_node(tu.cursor)
    return data_deps, compute_deps, control_deps

if __name__ == "__main__":
    filename = "/Users/aussie/projects/2025/EnergyPlus/EnergyPlus-8.9.0/long_division.cpp"  # Replace with your C/C++ source file
    filename = "/Users/aussie/projects/2025/EnergyPlus/EnergyPlus-8.9.0/long_short.cpp"  # Replace with your C/C++ source file
    filename = "test_simple.cpp"
    
    data_deps, compute_deps, control_deps = analyze_dependencies(filename)
    
    print("Data Dependencies:", data_deps)
    print("Compute Dependencies:", compute_deps)
    print("Control Dependencies:", control_deps)