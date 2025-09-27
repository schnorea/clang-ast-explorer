#!/usr/bin/env python3
"""
Test Reverse Navigation - Click source code to find AST nodes
"""

import sys
import os

# Add parent directory to path to import AST explorer modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import clang_config
from ast_backend import ASTBackend

def test_reverse_navigation():
    """Test the reverse navigation functionality"""
    print("Reverse Navigation Test")
    print("======================")
    
    # Create backend and parse a test file
    backend = ASTBackend()
    test_file = '../test/long_short.cpp'
    
    print(f"Parsing {test_file}...")
    try:
        backend.parse_file(test_file)
        print("✅ File parsed successfully")
    except Exception as e:
        print(f"❌ Error parsing file: {e}")
        return
    
    # Test finding nodes at specific locations
    test_locations = [
        (1, 1),    # First line
        (5, 10),   # Somewhere in the middle
        (10, 1),   # Another line
        (20, 5),   # Further down
        (100, 1),  # Beyond file end (should return None)
    ]
    
    print(f"\nTesting node lookup at various locations:")
    print("-" * 50)
    
    for line, col in test_locations:
        print(f"Location ({line}, {col}):", end=" ")
        
        try:
            node = backend.find_node_at_location(line, col)
            if node:
                print(f"✅ Found {node.cursor.kind.name}: '{node.cursor.spelling}'")
                
                # Show some details about the found node
                extent = node.cursor.extent
                if extent and extent.start and extent.end:
                    start_line = extent.start.line
                    start_col = extent.start.column
                    end_line = extent.end.line
                    end_col = extent.end.column
                    print(f"   Extent: ({start_line},{start_col}) -> ({end_line},{end_col})")
                else:
                    print("   No extent information")
            else:
                print("❌ No node found")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n🎉 Reverse navigation test completed!")
    print(f"Now run the AST Explorer and try the enhanced clicking:")
    print(f"  ✨ Hover over source lines to see hover highlighting")
    print(f"  👆 Click on source code lines to select AST nodes")
    print(f"  🌲 Watch the AST tree automatically expand and highlight!")

if __name__ == "__main__":
    test_reverse_navigation()