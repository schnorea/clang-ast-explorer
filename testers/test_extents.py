#!/usr/bin/env python3
"""
Test script to verify cursor extent functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ast_backend import ASTBackend

def test_cursor_extents():
    """Test cursor extent information for different AST nodes"""
    print("Testing Cursor Extents...")
    
    backend = ASTBackend()
    try:
            backend.parse_file('../test/long_short.cpp')
        print("✅ Parsed test/extent_test.cpp successfully")
        
        def print_cursor_info(cursor, depth=0):
            """Recursively print cursor extent information"""
            indent = "  " * depth
            
            # Get basic info
            kind = cursor.kind.name if cursor.kind else "Unknown"
            spelling = cursor.spelling or "<no name>"
            
            # Get extent information
            try:
                extent = cursor.extent
                if extent and extent.start.file and extent.end.file:
                    start_line = extent.start.line
                    start_col = extent.start.column
                    end_line = extent.end.line
                    end_col = extent.end.column
                    extent_info = f"({start_line},{start_col})-({end_line},{end_col})"
                else:
                    extent_info = "No extent"
            except:
                extent_info = "Extent error"
            
            # Print info for interesting nodes
            interesting_kinds = [
                'CLASS_DECL', 'FUNCTION_DECL', 'CXX_METHOD', 'CONSTRUCTOR',
                'NAMESPACE', 'VAR_DECL', 'TEMPLATE_TYPE_PARAMETER', 'FOR_STMT',
                'IF_STMT', 'COMPOUND_STMT'
            ]
            
            if any(kind_name in kind for kind_name in interesting_kinds):
                print(f"{indent}{kind}: '{spelling}' {extent_info}")
            
            # Recurse for children (limit depth to avoid too much output)
            if depth < 3:
                for child in cursor.get_children():
                    print_cursor_info(child, depth + 1)
        
        print("\nCursor Extent Information:")
        print_cursor_info(backend.translation_unit.cursor)
        
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    test_cursor_extents()