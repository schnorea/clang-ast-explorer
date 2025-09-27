#!/usr/bin/env python3
"""Quick theme detection test"""

import tkinter as tk
from tkinter import ttk

def detect_theme():
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Method 1: TTK Style
    try:
        style = ttk.Style()
        ttk_bg = style.lookup('TLabel', 'background')
        ttk_fg = style.lookup('TLabel', 'foreground')
        print(f"TTK Background: {ttk_bg}")
        print(f"TTK Foreground: {ttk_fg}")
    except Exception as e:
        print(f"TTK detection failed: {e}")
    
    # Method 2: Regular tk widget
    temp = tk.Text(root)
    tk_bg = temp.cget('bg')
    tk_fg = temp.cget('fg')
    print(f"TK Background: {tk_bg}")
    print(f"TK Foreground: {tk_fg}")
    
    # Determine theme
    def hex_to_rgb(hex_color):
        if hex_color.startswith('#'):
            hex_color = hex_color[1:]
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def is_dark(color):
        try:
            if color.startswith('#'):
                r, g, b = hex_to_rgb(color)
            else:
                temp_label = tk.Label()
                temp_label['bg'] = color
                actual = temp_label.cget('bg')
                temp_label.destroy()
                if actual.startswith('#'):
                    r, g, b = hex_to_rgb(actual)
                else:
                    return 'dark' in color.lower() or 'black' in color.lower()
            
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            return luminance < 0.5
        except:
            return False
    
    is_dark_theme = is_dark(tk_bg)
    print(f"Detected theme: {'Dark' if is_dark_theme else 'Light'}")
    
    root.destroy()

if __name__ == "__main__":
    detect_theme()