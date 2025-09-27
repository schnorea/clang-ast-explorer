#!/usr/bin/env python3
"""
Test script to demonstrate the command history functionality
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import clang_config
from ast_backend import ASTBackend
from ast_ui import InteractiveConsole

def test_console_history():
    """Create a simple window to test the console history feature"""
    root = tk.Tk()
    root.title("Console History Test")
    root.geometry("600x400")
    
    # Create backend
    backend = ASTBackend()
    try:
        backend.parse_file('../test/long_short.cpp')
    except:
        print("Note: File parsing failed, but console will still work")
    
    # Create console
    console = InteractiveConsole(root, backend)
    console.frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Add instruction label
    instruction = tk.Label(root, 
        text="Try typing commands and use ↑/↓ arrow keys to navigate history!\n"
             "Example commands: help_ast(), len(backend.command_history), 2+2",
        bg='lightblue', 
        pady=5,
        font=('Arial', 10))
    instruction.pack(fill='x', padx=10, pady=5)
    
    # Focus on the input entry
    console.input_entry.focus_set()
    
    print("🎯 Console History Test Window Opened")
    print("Try these features:")
    print("  1. Type some commands and press Enter")
    print("  2. Use ↑ arrow key to go back through history")
    print("  3. Use ↓ arrow key to go forward through history")
    print("  4. Type help_ast() for detailed help")
    
    root.mainloop()

if __name__ == "__main__":
    test_console_history()