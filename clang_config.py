"""
Configuration module for clang library setup
"""

import os
import sys
import clang.cindex
from typing import List, Optional

def find_libclang_paths() -> List[str]:
    """Find potential libclang library paths on different systems"""
    paths = []
    
    # macOS paths
    if sys.platform == 'darwin':
        paths.extend([
            '/usr/local/opt/llvm/lib/libclang.dylib',
            '/opt/homebrew/opt/llvm/lib/libclang.dylib',
            '/usr/local/lib/libclang.dylib',
            '/usr/lib/libclang.dylib',
        ])
        
        # Try to find via brew
        try:
            import subprocess
            result = subprocess.run(['brew', '--prefix', 'llvm'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                brew_path = result.stdout.strip() + '/lib/libclang.dylib'
                paths.insert(0, brew_path)
        except:
            pass
    
    # Linux paths
    elif sys.platform.startswith('linux'):
        paths.extend([
            '/usr/lib/x86_64-linux-gnu/libclang-1.0.so',
            '/usr/lib/libclang.so',
            '/usr/local/lib/libclang.so',
            '/usr/lib/llvm-15/lib/libclang.so.1',
            '/usr/lib/llvm-14/lib/libclang.so.1',
            '/usr/lib/llvm-13/lib/libclang.so.1',
            '/usr/lib/llvm-12/lib/libclang.so.1',
            '/usr/lib/llvm-11/lib/libclang.so.1',
            '/usr/lib/llvm-10/lib/libclang.so.1',
        ])
    
    # Windows paths
    elif sys.platform.startswith('win'):
        paths.extend([
            'C:\\Program Files\\LLVM\\bin\\libclang.dll',
            'C:\\LLVM\\bin\\libclang.dll',
            'libclang.dll',
        ])
    
    return paths

def setup_libclang() -> bool:
    """Setup libclang library path. Returns True if successful."""
    
    # Check if already configured
    try:
        clang.cindex.Index.create()
        return True
    except clang.cindex.LibclangError:
        pass
    
    # Try to find and set library path
    paths = find_libclang_paths()
    
    for path in paths:
        if os.path.exists(path):
            try:
                clang.cindex.Config.set_library_file(path)
                # Test if it works
                clang.cindex.Index.create()
                print(f"Using libclang from: {path}")
                return True
            except Exception as e:
                continue
    
    # If nothing worked, show error message
    print("Error: Could not find libclang library!")
    print("Searched paths:")
    for path in paths:
        exists = "✓" if os.path.exists(path) else "✗"
        print(f"  {exists} {path}")
    
    print("\nTo fix this issue:")
    if sys.platform == 'darwin':
        print("  brew install llvm")
    elif sys.platform.startswith('linux'):
        print("  sudo apt-get install libclang-dev  # Ubuntu/Debian")
        print("  sudo yum install clang-devel       # CentOS/RHEL")
    elif sys.platform.startswith('win'):
        print("  Install LLVM from https://llvm.org/builds/")
    
    return False

# Auto-configure when module is imported
if not setup_libclang():
    print("Warning: libclang setup failed. The application may not work correctly.")
    print("Note: If using the 'clang' package (20.1.5), this warning can be ignored.")