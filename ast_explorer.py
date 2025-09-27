#!/usr/bin/env python3
"""
Clang AST Explorer - Interactive GUI application for exploring C++ ASTs
"""

import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import clang.cindex
import clang_config  # This will auto-configure libclang
from ast_backend import ASTBackend
from ast_ui import ASTExplorerUI

class ASTExplorer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Clang AST Explorer")
        self.root.geometry("1200x800")
        
        # Initialize backend
        self.backend = ASTBackend()
        
        # Initialize UI
        self.ui = ASTExplorerUI(self.root, self.backend)
        
        # Setup menu
        self.setup_menu()
        
    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open C++ File", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Expand All", command=self.ui.expand_all)
        view_menu.add_command(label="Collapse All", command=self.ui.collapse_all)
        view_menu.add_separator()
        view_menu.add_command(label="Toggle Source Position (Left/Right)", command=self.ui.toggle_source_position)
        
        file_menu.add_separator()
        file_menu.add_command(label="Reload Current File", command=self.reload_file)
        
        # Add Tools menu for file monitoring
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_checkbutton(label="Auto-Monitor File Changes", 
                                   command=self.toggle_file_monitoring,
                                   variable=tk.BooleanVar(value=True))  # Default enabled
        
    def open_file(self):
        filename = filedialog.askopenfilename(
            title="Select C++ Source File",
            filetypes=[("C++ files", "*.cpp *.cc *.cxx"), ("C files", "*.c"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.backend.parse_file(filename)
                self.ui.populate_ast_tree()
                self.ui.update_status(f"Loaded: {filename}")
            except Exception as e:
                error_msg = str(e)
                if "Unknown template argument kind" in error_msg:
                    detailed_msg = (
                        f"Parse Error: {error_msg}\n\n"
                        f"This error suggests the C++ code uses template features "
                        f"that are newer than your libclang version supports.\n\n"
                        f"Suggestions:\n"
                        f"1. Try a simpler C++ file without complex templates\n"
                        f"2. Update your LLVM/clang installation\n"
                        f"3. Use a different C++ standard version\n\n"
                        f"Would you like to try parsing with relaxed settings?"
                    )
                    
                    if messagebox.askyesno("Parse Error", detailed_msg):
                        try:
                            # Try with more permissive settings
                            self.backend.parse_file(filename, args=['-std=c++11', '-w'])
                            self.ui.populate_ast_tree()
                            self.ui.update_status(f"Loaded with relaxed parsing: {filename}")
                            messagebox.showinfo("Success", "File parsed successfully with relaxed settings. Some advanced features may not be fully represented.")
                        except Exception as e2:
                            messagebox.showerror("Parse Failed", f"Even relaxed parsing failed: {str(e2)}")
                else:
                    messagebox.showerror("Error", f"Failed to parse file: {error_msg}")
    
    def reload_file(self):
        """Manually reload the current file"""
        if self.backend.current_file:
            self.ui._reload_current_file()
        else:
            messagebox.showinfo("No File", "No file is currently loaded to reload.")
    
    def toggle_file_monitoring(self):
        """Toggle file monitoring on/off"""
        if self.ui.monitoring_active:
            self.ui.stop_file_monitoring()
            self.ui.update_status("File monitoring disabled")
        else:
            if self.backend.current_file:
                self.ui.start_file_monitoring(self.backend.current_file)
            else:
                messagebox.showinfo("No File", "No file is currently loaded to monitor.")
    
    def run(self):
        # Load default file if available
        default_files = ["test/long_short.cpp", "test/long_division.cpp", "test/monitor_test.cpp"]
        for filename in default_files:
            try:
                self.backend.parse_file(filename)
                self.ui.populate_ast_tree()
                self.ui.update_status(f"Loaded: {filename}")
                break
            except:
                continue
        
        self.root.mainloop()

if __name__ == "__main__":
    app = ASTExplorer()
    app.run()