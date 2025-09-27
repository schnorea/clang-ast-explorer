#!/usr/bin/env python3
"""
Test script to verify theme detection in the source code viewer
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the parent directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ast_ui import SourceCodeViewer

def test_theme_detection():
    """Test the theme detection functionality"""
    print("Testing Source Code Viewer Theme Detection...")
    
    # Create a test window
    root = tk.Tk()
    root.title("Theme Detection Test")
    root.geometry("800x600")
    
    # Create source code viewer
    viewer = SourceCodeViewer(root)
    viewer.frame.pack(fill='both', expand=True)
    
    print(f"Detected theme: {'Dark' if viewer.is_dark_theme else 'Light'}")
    print(f"Background color: {viewer.bg_color}")
    print(f"Foreground color: {viewer.fg_color}")
    print(f"Keyword color: {viewer.keyword_color}")
    print(f"Comment color: {viewer.comment_color}")
    print(f"String color: {viewer.string_color}")
    
    # Load a test file to see the theme in action
    if os.path.exists('../test/test_viewer.cpp'):
        viewer.load_file('../test/test_viewer.cpp')
        print("Loaded ../test/test_viewer.cpp for theme preview")
    else:
        # Create some sample code
        viewer.text.config(state='normal')
        sample_code = '''// This is a comment
#include <iostream>
#include <string>

int main() {
    std::string message = "Hello, World!";  // String literal
    int number = 42;  // Number
    std::cout << message << " Number: " << number << std::endl;
    return 0;
}'''
        viewer.text.insert('1.0', sample_code)
        viewer._apply_syntax_highlighting()
        viewer.text.config(state='disabled')
        print("Created sample code for theme preview")
    
    print("\nTheme-aware source code viewer is ready!")
    print("The colors should now match your system's dark/light theme preference.")
    
    root.mainloop()

if __name__ == "__main__":
    test_theme_detection()