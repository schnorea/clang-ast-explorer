#!/usr/bin/env python3
"""
Test script to verify all scrollbars are properly themed
"""

import tkinter as tk
from tkinter import ttk

def test_scrollbar_theming():
    """Create a test window to compare themed vs unthemed scrollbars"""
    root = tk.Tk()
    root.title("Scrollbar Theming Test")
    root.geometry("800x600")
    
    # Create a notebook to show different examples
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)
    
    # TAB 1: TTK Themed Scrollbars (CORRECT)
    frame1 = ttk.Frame(notebook)
    notebook.add(frame1, text="✅ TTK Themed (Correct)")
    
    text_frame1 = ttk.Frame(frame1)
    text_frame1.pack(fill='both', expand=True, padx=10, pady=10)
    
    text1 = tk.Text(text_frame1, font=('Consolas', 10))
    v_scroll1 = ttk.Scrollbar(text_frame1, orient="vertical", command=text1.yview)
    h_scroll1 = ttk.Scrollbar(text_frame1, orient="horizontal", command=text1.xview)
    text1.configure(yscrollcommand=v_scroll1.set, xscrollcommand=h_scroll1.set)
    
    text1.grid(row=0, column=0, sticky='nsew')
    v_scroll1.grid(row=0, column=1, sticky='ns')
    h_scroll1.grid(row=1, column=0, sticky='ew')
    
    text_frame1.grid_rowconfigure(0, weight=1)
    text_frame1.grid_columnconfigure(0, weight=1)
    
    # Add sample content
    sample_text = """This text widget uses TTK themed scrollbars.
The scrollbars should match your system theme (dark/light mode).

This is how the AST Explorer windows should look:
- AST Structure (already correct)
- Node Information (now fixed)
- Interactive Console (now fixed) 
- Source Code Viewer (now fixed)

""" + "\n".join([f"Line {i}: Sample content for scrolling test" for i in range(50)])
    
    text1.insert('1.0', sample_text)
    
    # TAB 2: ScrolledText (INCORRECT - for comparison)
    frame2 = ttk.Frame(notebook)
    notebook.add(frame2, text="❌ ScrolledText (Old)")
    
    import scrolledtext
    text2 = scrolledtext.ScrolledText(frame2, font=('Consolas', 10))
    text2.pack(fill='both', expand=True, padx=10, pady=10)
    text2.insert('1.0', sample_text.replace("TTK themed", "default"))
    
    ttk.Label(root, text="Compare the scrollbar appearance between the two tabs").pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    test_scrollbar_theming()