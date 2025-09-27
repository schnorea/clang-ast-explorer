"""
AST Backend - Core logic for parsing and managing clang AST data
"""

import clang_config  # This will auto-configure libclang
import clang.cindex
from typing import Dict, List, Any, Optional

class ASTNode:
    """Wrapper class for clang cursor with additional metadata"""
    def __init__(self, cursor: clang.cindex.Cursor, parent=None, index=0):
        self.cursor = cursor
        self.parent = parent
        self.index = index
        self.children = []
        self.expanded = True
        
    @property
    def display_name(self):
        """Generate a display name for the tree view"""
        kind_name = self.cursor.kind.name
        spelling = self.cursor.spelling or ""
        display_name = self.cursor.displayname or ""
        
        # Create a meaningful display string
        if spelling:
            return f"{kind_name}: {spelling}"
        elif display_name:
            return f"{kind_name}: {display_name}"
        else:
            return kind_name
    
    @property
    def location_str(self):
        """Get location as string"""
        loc = self.cursor.location
        if loc.file:
            return f"{loc.file.name}:{loc.line}:{loc.column}"
        return f"<built-in>:{loc.line}:{loc.column}"
    
    def get_detailed_info(self) -> Dict[str, Any]:
        """Get detailed information about this cursor"""
        cursor = self.cursor
        info = {}
        
        try:
            info['Kind'] = cursor.kind.name if hasattr(cursor.kind, 'name') else str(cursor.kind)
        except:
            info['Kind'] = "<unknown>"
            
        try:
            info['Spelling'] = cursor.spelling or "<none>"
        except:
            info['Spelling'] = "<error>"
            
        try:
            info['Display Name'] = cursor.displayname or "<none>"
        except:
            info['Display Name'] = "<error>"
            
        try:
            info['Location'] = self.location_str
        except:
            info['Location'] = "<unknown>"
            
        try:
            info['Type'] = str(cursor.type.spelling) if cursor.type else "<none>"
        except:
            info['Type'] = "<error>"
            
        try:
            info['Is Definition'] = cursor.is_definition()
        except:
            info['Is Definition'] = "<error>"
            
        try:
            info['Is Declaration'] = cursor.is_declaration()
        except:
            info['Is Declaration'] = "<error>"
        
        # Add cursor-specific information with error handling
        try:
            if hasattr(cursor.kind, 'name') and cursor.kind == clang.cindex.CursorKind.VAR_DECL:
                try:
                    info['Storage Class'] = cursor.storage_class.name if cursor.storage_class else "<none>"
                except:
                    info['Storage Class'] = "<error>"
                    
            elif hasattr(cursor.kind, 'name') and cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL:
                try:
                    info['Result Type'] = cursor.result_type.spelling if cursor.result_type else "<none>"
                except:
                    info['Result Type'] = "<error>"
                try:
                    info['Arguments'] = len(list(cursor.get_arguments()))
                except:
                    info['Arguments'] = "<error>"
                    
            elif hasattr(cursor.kind, 'name') and cursor.kind == clang.cindex.CursorKind.INTEGER_LITERAL:
                try:
                    tokens = list(cursor.get_tokens())
                    if tokens:
                        info['Value'] = tokens[0].spelling
                except:
                    info['Value'] = "<error>"
                    
            elif hasattr(cursor.kind, 'name') and cursor.kind == clang.cindex.CursorKind.BINARY_OPERATOR:
                try:
                    info['Operator'] = self._extract_binary_operator()
                except:
                    info['Operator'] = "<error>"
        except:
            pass
            
        # Add token information for all cursors with error handling
        try:
            tokens = list(cursor.get_tokens())
            if tokens:
                info['Tokens'] = [t.spelling for t in tokens[:10]]  # Limit to first 10 tokens
                if len(tokens) > 10:
                    info['Tokens'].append('...')
        except:
            info['Tokens'] = "<error>"
        
        return info
    
    def _extract_binary_operator(self) -> str:
        """Extract the actual operator from a BINARY_OPERATOR cursor"""
        if self.cursor.kind != clang.cindex.CursorKind.BINARY_OPERATOR:
            return ""
            
        tokens = list(self.cursor.get_tokens())
        
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
        
        return ""

class ASTBackend:
    """Backend for managing clang AST parsing and data"""
    
    def __init__(self):
        self.index = clang.cindex.Index.create()
        self.translation_unit = None
        self.root_node = None
        self.current_file = None
        
    def parse_file(self, filename: str, args: list = None):
        """Parse a C++ file and build the AST tree"""
        self.current_file = filename
        
        # Use the same simple approach as graphclang.py - no custom args by default
        if args is None:
            args = []
        
        try:
            # Use the same simple approach as graphclang.py
            self.translation_unit = self.index.parse(filename, args=args)
            
            if not self.translation_unit:
                raise Exception(f"Failed to create translation unit for {filename}")
            
            # Don't check diagnostics - just like graphclang.py approach
            # Let it proceed even with warnings/errors
            
            # Build our tree structure with error handling
            self.root_node = self._build_tree(self.translation_unit.cursor)
            
        except Exception as e:
            if "Unknown template argument kind" in str(e):
                # Try with different C++ standards
                for std in ['c++20', 'c++14', 'c++11']:
                    try:
                        alt_args = [f'-std={std}'] + [arg for arg in args if not arg.startswith('-std=')]
                        self.translation_unit = self.index.parse(
                            filename, 
                            args=alt_args,
                            options=clang.cindex.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES
                        )
                        if self.translation_unit:
                            self.root_node = self._build_tree(self.translation_unit.cursor)
                            print(f"Successfully parsed with {std} standard")
                            return
                    except:
                        continue
                        
                # If all standards fail, provide helpful error message
                raise Exception(f"Failed to parse {filename}: {str(e)}\n\n"
                              f"This error often occurs when:\n"
                              f"1. The C++ code uses features newer than your libclang version\n"
                              f"2. Template instantiation issues\n"
                              f"3. Missing include paths\n\n"
                              f"Try:\n"
                              f"- Using a simpler C++ file\n"
                              f"- Updating your LLVM/clang installation\n"
                              f"- Adding necessary include paths")
            else:
                raise
        
    def _build_tree(self, cursor: clang.cindex.Cursor, parent=None, index=0) -> ASTNode:
        """Recursively build tree of ASTNode objects"""
        try:
            node = ASTNode(cursor, parent, index)
            
            # Safely iterate through children
            try:
                for i, child in enumerate(cursor.get_children()):
                    try:
                        child_node = self._build_tree(child, node, i)
                        node.children.append(child_node)
                    except Exception as e:
                        # Create an error node for problematic children
                        error_cursor = type('ErrorCursor', (), {
                            'kind': clang.cindex.CursorKind.UNEXPOSED_EXPR,
                            'spelling': f"<Error: {str(e)}>",
                            'displayname': f"<Parse Error>",
                            'location': child.location if hasattr(child, 'location') else None,
                            'type': None,
                            'is_definition': lambda: False,
                            'is_declaration': lambda: False,
                            'get_children': lambda: [],
                            'get_tokens': lambda: [],
                        })()
                        error_node = ASTNode(error_cursor, node, i)
                        node.children.append(error_node)
                        print(f"Warning: Skipped problematic node at child {i}: {str(e)}")
            except Exception as e:
                print(f"Warning: Could not iterate children of {cursor.kind}: {str(e)}")
                
            return node
            
        except Exception as e:
            print(f"Warning: Could not create node for cursor {cursor.kind}: {str(e)}")
            # Return a minimal error node
            error_cursor = type('ErrorCursor', (), {
                'kind': clang.cindex.CursorKind.UNEXPOSED_EXPR,
                'spelling': f"<Error: {str(e)}>",
                'displayname': f"<Parse Error>",
                'location': None,
                'type': None,
                'is_definition': lambda: False,
                'is_declaration': lambda: False,
                'get_children': lambda: [],
                'get_tokens': lambda: [],
            })()
            return ASTNode(error_cursor, parent, index)
    
    def find_node_by_path(self, path: List[int]) -> Optional[ASTNode]:
        """Find a node by its path (list of child indices)"""
        if not self.root_node or not path:
            return self.root_node
            
        current = self.root_node
        for index in path:
            if index < len(current.children):
                current = current.children[index]
            else:
                return None
        return current
    
    def get_node_path(self, node: ASTNode) -> List[int]:
        """Get the path to a node (list of child indices from root)"""
        path = []
        current = node
        while current.parent:
            path.insert(0, current.index)
            current = current.parent
        return path
    
    def search_nodes(self, predicate) -> List[ASTNode]:
        """Search for nodes matching a predicate function"""
        results = []
        
        def visit(node):
            if predicate(node):
                results.append(node)
            for child in node.children:
                visit(child)
                
        if self.root_node:
            visit(self.root_node)
        return results
    
    def get_nodes_by_kind(self, kind: clang.cindex.CursorKind) -> List[ASTNode]:
        """Get all nodes of a specific cursor kind"""
        return self.search_nodes(lambda node: node.cursor.kind == kind)
    
    def get_variables(self) -> List[ASTNode]:
        """Get all variable declarations"""
        return self.get_nodes_by_kind(clang.cindex.CursorKind.VAR_DECL)
    
    def get_functions(self) -> List[ASTNode]:
        """Get all function declarations"""
        return self.get_nodes_by_kind(clang.cindex.CursorKind.FUNCTION_DECL)