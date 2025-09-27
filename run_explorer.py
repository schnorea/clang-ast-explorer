#!/usr/bin/env python3
"""
Simple launcher for the AST Explorer application
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ast_explorer import ASTExplorer
    
    if __name__ == "__main__":
        app = ASTExplorer()
        app.run()
        
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you have installed the requirements:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error running application: {e}")
    sys.exit(1)