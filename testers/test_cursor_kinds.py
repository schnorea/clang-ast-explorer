#!/usr/bin/env python3
"""
Test Available Cursor Kinds - Check what cursor kinds appear in parsed C++ files
"""

import sys
import os
from collections import defaultdict

# Add parent directory to path to import AST explorer modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import clang_config
from ast_backend import ASTBackend

def collect_cursor_kinds(node, cursor_kinds):
    """Recursively collect all cursor kinds found in the AST"""
    cursor_kinds[node.cursor.kind.name] += 1
    
    for child in node.children:
        collect_cursor_kinds(child, cursor_kinds)

def test_cursor_kinds():
    """Test what cursor kinds are available in our test files"""
    print("Available Cursor Kinds Test")
    print("=" * 40)
    
    # Test files to parse
    test_files = [
        '../test/long_short.cpp',
        '../test/long_division.cpp',
        '../test/extent_test.cpp',
        '../test/comprehensive_test.cpp'
    ]
    
    all_cursor_kinds = defaultdict(int)
    
    backend = ASTBackend()
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\nParsing {test_file}...")
            try:
                backend.parse_file(test_file)
                if backend.root_node:
                    file_cursor_kinds = defaultdict(int)
                    collect_cursor_kinds(backend.root_node, file_cursor_kinds)
                    
                    print(f"  Found {len(file_cursor_kinds)} different cursor kinds")
                    
                    # Add to overall counts
                    for kind, count in file_cursor_kinds.items():
                        all_cursor_kinds[kind] += count
                        
            except Exception as e:
                print(f"  Error parsing {test_file}: {e}")
        else:
            print(f"  {test_file} not found")
    
    print(f"\n" + "=" * 40)
    print(f"SUMMARY: Found {len(all_cursor_kinds)} different cursor kinds across all files")
    print("=" * 40)
    
    # Sort by frequency (most common first)
    sorted_kinds = sorted(all_cursor_kinds.items(), key=lambda x: x[1], reverse=True)
    
    print(f"{'Cursor Kind':<35} {'Count':<10}")
    print("-" * 45)
    
    for kind, count in sorted_kinds:
        print(f"{kind:<35} {count:<10}")
    
    print(f"\n" + "=" * 40)
    print("RECOMMENDATIONS:")
    print("=" * 40)
    
    # Check for some specific kinds we documented
    documented_kinds = [
        'FUNCTION_DECL', 'VAR_DECL', 'PARM_DECL', 'CLASS_DECL', 'STRUCT_DECL',
        'ENUM_DECL', 'TYPEDEF_DECL', 'CXX_METHOD', 'CONSTRUCTOR', 'DESTRUCTOR',
        'COMPOUND_STMT', 'IF_STMT', 'FOR_STMT', 'WHILE_STMT', 'RETURN_STMT',
        'BINARY_OPERATOR', 'UNARY_OPERATOR', 'CALL_EXPR', 'DECL_REF_EXPR',
        'INTEGER_LITERAL', 'STRING_LITERAL', 'DECL_STMT'
    ]
    
    found_documented = []
    missing_documented = []
    
    for kind in documented_kinds:
        if kind in all_cursor_kinds:
            found_documented.append(kind)
        else:
            missing_documented.append(kind)
    
    print(f"✅ Found {len(found_documented)} of {len(documented_kinds)} documented kinds in test files")
    
    if missing_documented:
        print(f"\n❌ Missing documented kinds (need more complex test files):")
        for kind in missing_documented:
            print(f"   - {kind}")
        
        print(f"\n💡 To see more cursor kinds, try adding test files with:")
        print("   - C++ classes (for CXX_METHOD, CONSTRUCTOR, DESTRUCTOR)")
        print("   - Templates (for template-related cursors)")
        print("   - Enums (for ENUM_DECL, ENUM_CONSTANT_DECL)")
        print("   - Preprocessor directives (for MACRO_DEFINITION, INCLUSION_DIRECTIVE)")
        print("   - More complex control flow (switch statements, do-while, etc.)")

if __name__ == "__main__":
    test_cursor_kinds()