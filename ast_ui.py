"""
AST UI - User interface components for the AST Explorer
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import code
import sys
import os
import time
from io import StringIO
from typing import Dict, Any, Optional
from ast_backend import ASTBackend, ASTNode

class ASTTreeView:
    """Tree view widget for displaying the AST structure"""
    
    def __init__(self, parent, backend: ASTBackend, on_select_callback=None):
        self.backend = backend
        self.on_select_callback = on_select_callback
        self.node_map = {}  # Maps tree item ids to ASTNode objects
        
        # Create frame and tree
        self.frame = ttk.Frame(parent)
        self.tree = ttk.Treeview(self.frame, selectmode='browse')
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self._on_tree_select)
        
    def populate(self):
        """Populate the tree with AST data"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.node_map.clear()
        
        if not self.backend.root_node:
            return
            
        # Add root and its children
        self._add_node_to_tree("", self.backend.root_node, open=True)
        
    def _add_node_to_tree(self, parent_id: str, node: ASTNode, open: bool = False):
        """Recursively add nodes to the tree"""
        item_id = self.tree.insert(parent_id, "end", text=node.display_name, open=open)
        self.node_map[item_id] = node
        
        # Add children
        for child in node.children:
            self._add_node_to_tree(item_id, child, open=False)
            
    def _on_tree_select(self, event):
        """Handle tree selection"""
        selection = self.tree.selection()
        if selection and self.on_select_callback:
            item_id = selection[0]
            node = self.node_map.get(item_id)
            if node:
                self.on_select_callback(node)
                
    def expand_all(self):
        """Expand all tree items"""
        def expand_item(item_id):
            self.tree.item(item_id, open=True)
            for child in self.tree.get_children(item_id):
                expand_item(child)
                
        for item in self.tree.get_children():
            expand_item(item)
            
    def collapse_all(self):
        """Collapse all tree items"""
        def collapse_item(item_id):
            self.tree.item(item_id, open=False)
            for child in self.tree.get_children(item_id):
                collapse_item(child)
                
        for item in self.tree.get_children():
            self.tree.item(item, open=True)  # Keep root open
            for child in self.tree.get_children(item):
                collapse_item(child)

class ASTInfoPanel:
    """Panel for displaying detailed information about selected AST node"""
    
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        
        # Create text widget with themed scrollbar
        text_frame = ttk.Frame(self.frame)
        text_frame.pack(fill='both', expand=True)
        
        self.text = tk.Text(
            text_frame, 
            wrap=tk.WORD, 
            state='disabled',
            font=('Consolas', 10)
        )
        
        # Create themed scrollbars
        v_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text.yview)
        h_scrollbar = ttk.Scrollbar(text_frame, orient="horizontal", command=self.text.xview)
        self.text.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and text widget
        self.text.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configure grid weights
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
    def update_info(self, node: ASTNode):
        """Update the info panel with node details"""
        self.text.config(state='normal')
        self.text.delete(1.0, tk.END)
        
        info = node.get_detailed_info()
        
        # Format and display the information
        for key, value in info.items():
            self.text.insert(tk.END, f"{key}: ", "bold")
            self.text.insert(tk.END, f"{value}\n")
            
        # Configure tag for bold text
        self.text.tag_configure("bold", font=('Consolas', 10, 'bold'))
        
        self.text.config(state='disabled')
        
    def clear(self):
        """Clear the info panel"""
        self.text.config(state='normal')
        self.text.delete(1.0, tk.END)
        self.text.config(state='disabled')

class SourceCodeViewer:
    """Panel for displaying source code with syntax highlighting and AST node highlighting"""
    
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.current_file = None
        self.file_lines = []
        
        # Detect system theme colors
        self._setup_theme_colors()
        
        # Create text widget with themed scrollbar
        text_frame = ttk.Frame(self.frame)
        text_frame.pack(fill='both', expand=True)
        
        self.text = tk.Text(
            text_frame,
            wrap=tk.NONE,  # No word wrapping for code
            state='disabled',
            font=('Consolas', 10),
            bg=self.bg_color,
            fg=self.fg_color,
            insertbackground=self.fg_color,  # Cursor color
            selectbackground=self.select_bg_color,
            selectforeground=self.select_fg_color
        )
        
        # Create themed scrollbars
        v_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text.yview)
        h_scrollbar = ttk.Scrollbar(text_frame, orient="horizontal", command=self.text.xview)
        self.text.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and text widget using grid for better control
        self.text.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configure grid weights
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
        # Configure highlighting tags with theme-aware colors
        self._configure_syntax_tags()
        
        # Line number variables
        self.current_highlight_line = None
    
    def _setup_theme_colors(self):
        """Detect system theme and set appropriate colors"""
        # First try to detect macOS dark mode specifically
        import subprocess
        import platform
        
        macos_dark_mode = False
        if platform.system() == "Darwin":  # macOS
            try:
                result = subprocess.run(
                    ["defaults", "read", "-g", "AppleInterfaceStyle"], 
                    capture_output=True, text=True, timeout=2
                )
                macos_dark_mode = result.returncode == 0 and "Dark" in result.stdout
            except:
                pass
        
        # Try to use ttk style system for theme detection
        try:
            style = ttk.Style()
            # Get the background color from ttk theme
            ttk_bg = style.lookup('TLabel', 'background')
            ttk_fg = style.lookup('TLabel', 'foreground')
            
            if ttk_bg and ttk_fg:
                system_bg = ttk_bg
                system_fg = ttk_fg
            else:
                # Fallback to tk widget
                temp_widget = tk.Text(self.frame)
                system_bg = temp_widget.cget('bg')
                system_fg = temp_widget.cget('fg')
                temp_widget.destroy()
        except:
            # Fallback to tk widget
            temp_widget = tk.Text(self.frame)
            system_bg = temp_widget.cget('bg')
            system_fg = temp_widget.cget('fg')
            temp_widget.destroy()
        
        # Determine if we're in dark mode by checking background brightness
        def hex_to_rgb(hex_color):
            """Convert hex color to RGB tuple"""
            if hex_color.startswith('#'):
                hex_color = hex_color[1:]
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def is_dark_color(color):
            """Determine if a color is dark"""
            try:
                if color.startswith('#'):
                    r, g, b = hex_to_rgb(color)
                else:
                    # Handle system color names - convert to actual color
                    temp = tk.Label()
                    temp['bg'] = color  
                    actual_color = temp.cget('bg')
                    temp.destroy()
                    if actual_color.startswith('#'):
                        r, g, b = hex_to_rgb(actual_color)
                    else:
                        # Common dark colors
                        dark_colors = ['black', 'gray10', 'gray20', 'gray30', 'darkgray', 
                                     'SystemWindowText', 'SystemButtonFace']
                        return any(dark in color.lower() for dark in ['black', 'dark', 'gray1', 'gray2', 'gray3'])
                
                # Calculate luminance using standard formula
                luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
                return luminance < 0.5
            except:
                # If all else fails, assume light theme
                return False
        
        # Use macOS detection if available, otherwise use color analysis
        self.is_dark_theme = macos_dark_mode or is_dark_color(system_bg)
        
        if self.is_dark_theme:
            # Dark theme colors - use system colors as base
            self.bg_color = system_bg if not macos_dark_mode else '#1E1E1E'
            self.fg_color = system_fg if not macos_dark_mode else '#D4D4D4'
            self.select_bg_color = '#4472C4'
            self.select_fg_color = '#FFFFFF'
            self.highlight_bg = '#3A3A00'  # Dark yellow for highlighting
            self.highlight_fg = '#FFFF99'
            self.line_highlight_bg = '#2D3748'  # Dark blue-gray for line highlighting
            self.keyword_color = '#569CD6'  # Light blue for keywords
            self.comment_color = '#6A9955'  # Green for comments
            self.string_color = '#CE9178'   # Light orange for strings
            self.number_color = '#B5CEA8'   # Light green for numbers
        else:
            # Light theme colors - use system colors as base
            self.bg_color = system_bg if system_bg != 'systemWindowBackgroundColor' else '#FFFFFF'
            self.fg_color = system_fg if system_fg != 'systemTextColor' else '#000000'
            self.select_bg_color = '#4472C4'
            self.select_fg_color = '#FFFFFF'
            self.highlight_bg = '#FFFF99'  # Yellow for highlighting
            self.highlight_fg = '#000000'
            self.line_highlight_bg = '#E6F3FF'  # Light blue for line highlighting
            self.keyword_color = '#0000FF'  # Blue for keywords
            self.comment_color = '#008000'  # Green for comments
            self.string_color = '#A31515'   # Dark red for strings
            self.number_color = '#FF6600'   # Orange for numbers
    
    def _configure_syntax_tags(self):
        """Configure syntax highlighting tags with theme-appropriate colors"""
        self.text.tag_configure("highlight", 
                               background=self.highlight_bg, 
                               foreground=self.highlight_fg)
        self.text.tag_configure("highlight_line", 
                               background=self.line_highlight_bg, 
                               foreground=self.fg_color)
        self.text.tag_configure("keyword", 
                               foreground=self.keyword_color, 
                               font=('Consolas', 10, 'bold'))
        self.text.tag_configure("comment", 
                               foreground=self.comment_color, 
                               font=('Consolas', 10, 'italic'))
        self.text.tag_configure("string", 
                               foreground=self.string_color)
        self.text.tag_configure("number", 
                               foreground=self.number_color)
        
    def load_file(self, filename: str):
        """Load and display a source file"""
        try:
            self.current_file = filename
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                self.file_lines = content.splitlines()
            
            self.text.config(state='normal')
            self.text.delete(1.0, tk.END)
            
            # Add line numbers and content
            for i, line in enumerate(self.file_lines, 1):
                line_text = f"{i:4d}: {line}\n"
                self.text.insert(tk.END, line_text)
            
            # Apply basic syntax highlighting
            self._apply_syntax_highlighting()
            
            self.text.config(state='disabled')
            return True
            
        except Exception as e:
            self.text.config(state='normal')
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, f"Error loading file '{filename}': {str(e)}")
            self.text.config(state='disabled')
            return False
    
    def highlight_location(self, line: int, column: int = None, end_line: int = None, end_column: int = None):
        """Highlight a specific location in the source code"""
        if not self.current_file or line < 1 or line > len(self.file_lines):
            return
        
        self.text.config(state='normal')
        
        # Clear previous highlights
        self.text.tag_remove("highlight", 1.0, tk.END)
        self.text.tag_remove("highlight_line", 1.0, tk.END)
        
        # Calculate text widget position (accounting for line numbers)
        # Line numbers are "nnnn: " format, so 6 characters
        start_pos = f"{line}.{6 + (column - 1 if column else 0)}"
        
        if end_line and end_column:
            # Highlight specific range
            end_pos = f"{end_line}.{6 + (end_column - 1)}"
            self.text.tag_add("highlight", start_pos, end_pos)
        elif column:
            # Highlight from column to end of word/token
            # Try to find end of current token
            line_content = self.file_lines[line - 1]
            if column <= len(line_content):
                # Find end of current word/token
                end_col = column
                while end_col <= len(line_content) and line_content[end_col - 1].isalnum():
                    end_col += 1
                end_pos = f"{line}.{6 + (end_col - 1)}"
                self.text.tag_add("highlight", start_pos, end_pos)
            else:
                # Just highlight the line
                self.text.tag_add("highlight_line", f"{line}.0", f"{line}.end")
        else:
            # Highlight entire line
            self.text.tag_add("highlight_line", f"{line}.0", f"{line}.end")
        
        # Scroll to make the highlighted area visible
        self.text.see(start_pos)
        
        self.text.config(state='disabled')
        self.current_highlight_line = line
    
    def clear_highlight(self):
        """Clear all highlighting"""
        self.text.config(state='normal')
        self.text.tag_remove("highlight", 1.0, tk.END)
        self.text.tag_remove("highlight_line", 1.0, tk.END)
        self.text.config(state='disabled')
        self.current_highlight_line = None
    
    def _apply_syntax_highlighting(self):
        """Apply basic C++ syntax highlighting"""
        content = self.text.get(1.0, tk.END)
        
        # C++ keywords
        keywords = [
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
            'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
            'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
            'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while',
            'class', 'private', 'protected', 'public', 'friend', 'inline', 'operator',
            'overload', 'template', 'this', 'virtual', 'bool', 'false', 'true',
            'namespace', 'using', 'try', 'catch', 'throw', 'new', 'delete'
        ]
        
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            # Skip line number prefix when analyzing
            if len(line) > 6 and line[4:6] == ': ':
                code_part = line[6:]  # Skip "nnnn: " prefix
                start_col = 6
                
                # Highlight keywords
                words = code_part.split()
                col = start_col
                for word in words:
                    word_start = line.find(word, col - start_col + start_col)
                    if word_start != -1 and word.strip('(){}[];,') in keywords:
                        start_pos = f"{line_num}.{word_start}"
                        end_pos = f"{line_num}.{word_start + len(word)}"
                        self.text.tag_add("keyword", start_pos, end_pos)
                    col = word_start + len(word) if word_start != -1 else col
                
                # Highlight comments
                if '//' in code_part:
                    comment_start = code_part.find('//')
                    start_pos = f"{line_num}.{start_col + comment_start}"
                    end_pos = f"{line_num}.end"
                    self.text.tag_add("comment", start_pos, end_pos)
                
                # Highlight strings (basic)
                in_string = False
                i = 0
                while i < len(code_part):
                    if code_part[i] == '"' and (i == 0 or code_part[i-1] != '\\'):
                        if not in_string:
                            string_start = i
                            in_string = True
                        else:
                            start_pos = f"{line_num}.{start_col + string_start}"
                            end_pos = f"{line_num}.{start_col + i + 1}"
                            self.text.tag_add("string", start_pos, end_pos)
                            in_string = False
                    i += 1

class InteractiveConsole:
    """Interactive Python console for AST exploration"""
    
    def __init__(self, parent, backend: ASTBackend):
        self.backend = backend
        self.selected_node = None
        
        # Command history management
        self.command_history = []
        self.history_index = 0
        self.current_input = ""  # Store current input when navigating history
        
        self.frame = ttk.Frame(parent)
        
        # Create text widget for console output with themed scrollbar
        output_frame = ttk.Frame(self.frame)
        output_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        self.output = tk.Text(
            output_frame,
            height=8,
            font=('Consolas', 9),
            state='disabled'
        )
        
        # Create themed scrollbars
        v_scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.output.yview)
        h_scrollbar = ttk.Scrollbar(output_frame, orient="horizontal", command=self.output.xview)
        self.output.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and text widget using grid
        self.output.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configure grid weights
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)
        
        # Create entry widget for input
        input_frame = ttk.Frame(self.frame)
        input_frame.pack(fill='x', padx=2, pady=2)
        
        ttk.Label(input_frame, text=">>> ").pack(side='left')
        self.input_entry = ttk.Entry(input_frame, font=('Consolas', 9))
        self.input_entry.pack(fill='x', expand=True, side='left')
        self.input_entry.bind('<Return>', self._execute_command)
        
        # Bind arrow keys for history navigation
        self.input_entry.bind('<Up>', self._history_up)
        self.input_entry.bind('<Down>', self._history_down)
        self.input_entry.bind('<KeyPress>', self._on_key_press)
        
        # Setup console environment
        self.console_globals = {
            'backend': self.backend,
            'clang': __import__('clang.cindex'),
            'selected': None,
            'root': None,
            'find_by_kind': self._find_by_kind,
            'find_vars': self._find_vars,
            'find_funcs': self._find_funcs,
            'help_ast': self._help_ast,
            'reparse_file': self._reparse_file,
            'parse_with_args': self._parse_with_args,
        }
        
        # Show welcome message
        self._write_output("=== AST Explorer Console ===\n")
        self._write_output("💡 Tip: Use ↑/↓ arrow keys for command history\n")
        self._write_output("Available objects:\n")
        self._write_output("  backend - AST backend instance\n")
        self._write_output("  selected - Currently selected node\n")
        self._write_output("  root - Root AST node\n")
        self._write_output("Available functions:\n")
        self._write_output("  find_by_kind(kind) - Find nodes by cursor kind\n")
        self._write_output("  find_vars() - Find all variable declarations\n")
        self._write_output("  find_funcs() - Find all function declarations\n")
        self._write_output("  reparse_file(filename) - Reparse a file with default settings\n")
        self._write_output("  parse_with_args(filename, args) - Parse with custom arguments\n")
        self._write_output("  help_ast() - Show detailed help\n")
        self._write_output("Type help_ast() for more information.\n\n")
        
    def update_selected_node(self, node: ASTNode):
        """Update the selected node in console context"""
        self.selected_node = node
        self.console_globals['selected'] = node
        
    def update_root_node(self, node: ASTNode):
        """Update the root node in console context"""
        self.console_globals['root'] = node
        
    def _execute_command(self, event):
        """Execute a Python command"""
        command = self.input_entry.get().strip()
        if not command:
            return
        
        # Add command to history (avoid duplicates of the last command)
        if not self.command_history or self.command_history[-1] != command:
            self.command_history.append(command)
            # Limit history size to 100 commands
            if len(self.command_history) > 100:
                self.command_history.pop(0)
        
        # Reset history navigation
        self.history_index = len(self.command_history)
        self.current_input = ""
            
        self.input_entry.delete(0, tk.END)
        self._write_output(f">>> {command}\n")
        
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # Execute the command
            result = eval(command, self.console_globals)
            output = sys.stdout.getvalue()
            
            if output:
                self._write_output(output)
            if result is not None:
                self._write_output(f"{result}\n")
                
        except Exception as e:
            # Try exec for statements
            try:
                sys.stdout = StringIO()
                exec(command, self.console_globals)
                output = sys.stdout.getvalue()
                if output:
                    self._write_output(output)
            except Exception as e2:
                self._write_output(f"Error: {str(e2)}\n")
        finally:
            sys.stdout = old_stdout
            
        self._write_output("\n")
        
    def _write_output(self, text: str):
        """Write text to console output"""
        self.output.config(state='normal')
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.config(state='disabled')
    
    def _history_up(self, event):
        """Navigate up in command history (previous command)"""
        if not self.command_history:
            return "break"  # Prevent default behavior
        
        # Store current input if we're at the end of history
        if self.history_index == len(self.command_history):
            self.current_input = self.input_entry.get()
        
        # Move up in history
        if self.history_index > 0:
            self.history_index -= 1
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.command_history[self.history_index])
        
        return "break"  # Prevent default up arrow behavior
    
    def _history_down(self, event):
        """Navigate down in command history (next command)"""
        if not self.command_history:
            return "break"
        
        # Move down in history
        if self.history_index < len(self.command_history):
            self.history_index += 1
            self.input_entry.delete(0, tk.END)
            
            if self.history_index == len(self.command_history):
                # Back to current input
                self.input_entry.insert(0, self.current_input)
            else:
                # Show history command
                self.input_entry.insert(0, self.command_history[self.history_index])
        
        return "break"  # Prevent default down arrow behavior
    
    def _on_key_press(self, event):
        """Handle key presses to reset history navigation when typing"""
        # Reset history navigation when user starts typing (except for arrow keys)
        if event.keysym not in ['Up', 'Down', 'Return']:
            self.history_index = len(self.command_history)
            self.current_input = ""
        
    def _find_by_kind(self, kind_name: str):
        """Find nodes by cursor kind name"""
        if not self.backend.root_node:
            return []
            
        # Convert string to cursor kind
        try:
            kind = getattr(__import__('clang.cindex').cindex.CursorKind, kind_name)
            return self.backend.get_nodes_by_kind(kind)
        except AttributeError:
            return f"Unknown cursor kind: {kind_name}"
            
    def _find_vars(self):
        """Find all variable declarations"""
        return self.backend.get_variables()
        
    def _find_funcs(self):
        """Find all function declarations"""
        return self.backend.get_functions()
        
    def _reparse_file(self, filename: str):
        """Reparse a file with default settings"""
        try:
            self.backend.parse_file(filename)
            return f"Successfully reparsed: {filename}"
        except Exception as e:
            return f"Failed to reparse {filename}: {str(e)}"
    
    def _parse_with_args(self, filename: str, args: list):
        """Parse a file with custom arguments"""
        try:
            self.backend.parse_file(filename, args)
            return f"Successfully parsed {filename} with args: {args}"
        except Exception as e:
            return f"Failed to parse {filename} with args {args}: {str(e)}"
    
    def _help_ast(self):
        """Show detailed help information"""
        help_text = """
AST Explorer Console Help:

Console Features:
  ↑/↓ arrows - Navigate command history (up to 100 commands)
  Enter - Execute command
  Tab completion - Available in Python expressions

Objects:
  backend - The AST backend instance with parsed data
  selected - Currently selected AST node (ASTNode object)
  root - Root AST node of the translation unit
  clang - The clang.cindex module

Node Properties (for selected or any ASTNode):
  .cursor - The underlying clang cursor
  .children - List of child nodes
  .parent - Parent node
  .display_name - Display name for tree
  .location_str - Location as string
  .get_detailed_info() - Get detailed info dictionary

Cursor Properties (for node.cursor):
  .kind - Cursor kind (e.g., CursorKind.VAR_DECL)
  .spelling - Cursor spelling
  .displayname - Display name
  .location - Source location
  .type - Type information
  
Functions:
  find_by_kind('KIND_NAME') - Find nodes by kind (e.g., 'VAR_DECL')
  find_vars() - Find all variable declarations
  find_funcs() - Find all function declarations
  reparse_file('filename') - Reparse a file with default settings
  parse_with_args('filename', ['-std=c++17', '-w']) - Parse with custom args

Examples:
  selected.cursor.spelling  # Get name of selected node
  len(find_vars())          # Count variable declarations
  [n.cursor.spelling for n in find_vars()]  # List variable names
  selected.get_detailed_info()  # Get all info about selected node
  
  # Try different parsing options:
  parse_with_args('file.cpp', ['-std=c++11'])
  parse_with_args('file.cpp', ['-std=c++20', '-w'])
  parse_with_args('file.cpp', ['-std=c++17', '-I/usr/include'])
"""
        return help_text

class ASTExplorerUI:
    """Main UI class that coordinates all components"""
    
    def __init__(self, root: tk.Tk, backend: ASTBackend):
        self.root = root
        self.backend = backend
        self.source_on_left = True  # Default position for source viewer
        
        # File monitoring attributes
        self.current_file_path = None
        self.last_modified_time = None
        self.file_check_interval = 1000  # Check every 1 second
        self.monitoring_active = False
        self.dialog_showing = False  # Prevent multiple dialogs
        self.last_dialog_time = 0    # Track when last dialog was shown
        
        # Create main horizontal paned window
        self.main_horizontal_paned = ttk.PanedWindow(root, orient='horizontal')
        self.main_horizontal_paned.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create source code viewer
        self.source_frame = ttk.LabelFrame(self.main_horizontal_paned, text="Source Code", padding=5)
        self.source_viewer = SourceCodeViewer(self.source_frame)
        self.source_viewer.frame.pack(fill='both', expand=True)
        
        # Create vertical paned window for the three main panels
        self.ast_panels_paned = ttk.PanedWindow(self.main_horizontal_paned, orient='vertical')
        
        # Top frame (50% - AST Tree View)
        tree_frame = ttk.LabelFrame(self.ast_panels_paned, text="AST Structure", padding=5)
        self.ast_tree = ASTTreeView(tree_frame, backend, self._on_node_select)
        self.ast_tree.frame.pack(fill='both', expand=True)
        
        # Middle frame (25% - Node Information)
        info_frame = ttk.LabelFrame(self.ast_panels_paned, text="Node Information", padding=5)
        self.info_panel = ASTInfoPanel(info_frame)
        self.info_panel.frame.pack(fill='both', expand=True)
        
        # Bottom frame (25% - Interactive Console)
        console_frame = ttk.LabelFrame(self.ast_panels_paned, text="Interactive Console", padding=5)
        self.console = InteractiveConsole(console_frame, backend)
        self.console.frame.pack(fill='both', expand=True)
        
        # Add frames to vertical paned window
        self.ast_panels_paned.add(tree_frame, weight=2)  # 50%
        self.ast_panels_paned.add(info_frame, weight=1)  # 25%
        self.ast_panels_paned.add(console_frame, weight=1)  # 25%
        
        # Add panels to horizontal paned window (source on left by default)
        self.main_horizontal_paned.add(self.source_frame, weight=1)  # 33%
        self.main_horizontal_paned.add(self.ast_panels_paned, weight=2)  # 67%
        
        # Status bar
        self.status_bar = ttk.Label(root, text="Ready", relief='sunken', anchor='w')
        self.status_bar.pack(fill='x', side='bottom')
        
    def _on_node_select(self, node: ASTNode):
        """Handle node selection from tree view"""
        self.info_panel.update_info(node)
        self.console.update_selected_node(node)
        
        # Highlight corresponding source code location
        self._highlight_source_location(node)
        
    def populate_ast_tree(self):
        """Populate the AST tree view"""
        self.ast_tree.populate()
        if self.backend.root_node:
            self.console.update_root_node(self.backend.root_node)
            
        # Load source file in viewer
        if self.backend.current_file:
            self.source_viewer.load_file(self.backend.current_file)
            
            # Start monitoring the file for changes
            self.start_file_monitoring(self.backend.current_file)
    
    def _highlight_source_location(self, node: ASTNode):
        """Highlight the source location of the selected AST node using its full extent"""
        try:
            cursor = node.cursor
            extent = cursor.extent
            
            if extent and extent.start.file and extent.end.file:
                # Check if the extent is in the current file
                current_file = os.path.abspath(self.backend.current_file) if self.backend.current_file else None
                start_file = os.path.abspath(extent.start.file.name) if extent.start.file.name else None
                end_file = os.path.abspath(extent.end.file.name) if extent.end.file.name else None
                
                if (current_file and start_file and end_file and 
                    current_file == start_file and current_file == end_file):
                    # Highlight the full extent of the cursor
                    self.source_viewer.highlight_location(
                        extent.start.line, extent.start.column,
                        extent.end.line, extent.end.column
                    )
                else:
                    # Clear highlight if extent spans different files
                    self.source_viewer.clear_highlight()
            else:
                # Fallback to using basic location if extent is not available
                location = cursor.location
                if location and location.file:
                    current_file = os.path.abspath(self.backend.current_file) if self.backend.current_file else None
                    node_file = os.path.abspath(location.file.name) if location.file.name else None
                    
                    if current_file and node_file and current_file == node_file:
                        # Highlight just the start location
                        self.source_viewer.highlight_location(location.line, location.column)
                    else:
                        self.source_viewer.clear_highlight()
                else:
                    self.source_viewer.clear_highlight()
        except Exception as e:
            # If there's any error getting extent/location info, just clear highlight
            self.source_viewer.clear_highlight()
    
    def toggle_source_position(self):
        """Toggle source viewer between left and right positions"""
        self.source_on_left = not self.source_on_left
        
        # Remove panels from current positions
        self.main_horizontal_paned.forget(self.source_frame)
        self.main_horizontal_paned.forget(self.ast_panels_paned)
        
        # Re-add in new positions
        if self.source_on_left:
            self.main_horizontal_paned.add(self.source_frame, weight=1)
            self.main_horizontal_paned.add(self.ast_panels_paned, weight=2)
        else:
            self.main_horizontal_paned.add(self.ast_panels_paned, weight=2)
            self.main_horizontal_paned.add(self.source_frame, weight=1)
            
    def expand_all(self):
        """Expand all tree items"""
        self.ast_tree.expand_all()
        
    def collapse_all(self):
        """Collapse all tree items"""
        self.ast_tree.collapse_all()
        
    def update_status(self, message: str):
        """Update status bar"""
        self.status_bar.config(text=message)
    
    def start_file_monitoring(self, file_path: str):
        """Start monitoring a file for changes"""
        self.current_file_path = os.path.abspath(file_path)
        try:
            self.last_modified_time = os.path.getmtime(self.current_file_path)
            self.monitoring_active = True
            self.dialog_showing = False  # Reset dialog state
            self.last_dialog_time = 0    # Reset dialog timing
            self._schedule_file_check()
            self.update_status(f"Monitoring: {os.path.basename(file_path)}")
        except OSError:
            self.update_status(f"Error: Cannot monitor {file_path}")
    
    def stop_file_monitoring(self):
        """Stop monitoring the current file"""
        self.monitoring_active = False
        self.current_file_path = None
        self.last_modified_time = None
        self.dialog_showing = False  # Reset dialog state
        self.last_dialog_time = 0    # Reset dialog timing
    
    def _schedule_file_check(self):
        """Schedule the next file check"""
        if self.monitoring_active:
            self.root.after(self.file_check_interval, self._check_file_changes)
    
    def _check_file_changes(self):
        """Check if the monitored file has changed"""
        if not self.monitoring_active or not self.current_file_path:
            return
        
        try:
            current_modified_time = os.path.getmtime(self.current_file_path)
            
            # Use a more robust comparison - check if change is significant (> 0.1 seconds)
            if abs(current_modified_time - self.last_modified_time) > 0.1:
                # File has been modified significantly
                self._handle_file_change()
                self.last_modified_time = current_modified_time
                
        except OSError:
            # File might have been deleted or moved
            self._handle_file_deleted()
            return
        
        # Schedule next check
        self._schedule_file_check()
    
    def _handle_file_change(self):
        """Handle when the monitored file has changed"""
        # Prevent multiple dialogs for the same change
        if self.dialog_showing:
            return
        
        current_time = time.time()
        # Only show dialog if at least 2 seconds have passed since last dialog
        if current_time - self.last_dialog_time < 2.0:
            return
            
        self.dialog_showing = True
        self.last_dialog_time = current_time
        
        try:
            filename = os.path.basename(self.current_file_path)
            
            # Show dialog asking user if they want to reload
            message = (f"The file '{filename}' has been modified externally.\n\n"
                      f"Would you like to reload and re-parse the updated file?")
            
            if messagebox.askyesno("File Changed", message, icon='question'):
                self._reload_current_file()
            else:
                # User chose not to reload, show status
                self.update_status(f"File changed but not reloaded: {filename}")
                
        finally:
            # Always reset dialog flag
            self.dialog_showing = False
    
    def _handle_file_deleted(self):
        """Handle when the monitored file has been deleted"""
        filename = os.path.basename(self.current_file_path) if self.current_file_path else "Unknown"
        
        messagebox.showwarning("File Deleted", 
                             f"The monitored file '{filename}' has been deleted or moved.\n"
                             f"File monitoring has been stopped.")
        
        self.stop_file_monitoring()
        self.update_status(f"File deleted: {filename}")
    
    def _reload_current_file(self):
        """Reload and re-parse the current file"""
        if not self.current_file_path:
            return
        
        try:
            # Re-parse the file
            self.backend.parse_file(self.current_file_path)
            
            # Update all UI components
            self.populate_ast_tree()
            
            # Reload source code viewer
            self.source_viewer.load_file(self.current_file_path)
            
            # Clear info panel and console output
            self.info_panel.clear()
            
            filename = os.path.basename(self.current_file_path)
            self.update_status(f"Reloaded: {filename}")
            
        except Exception as e:
            filename = os.path.basename(self.current_file_path) if self.current_file_path else "Unknown"
            error_msg = f"Failed to reload '{filename}': {str(e)}"
            messagebox.showerror("Reload Error", error_msg)
            self.update_status(f"Reload failed: {filename}")