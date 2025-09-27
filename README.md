# Clang AST Explorer

A comprehensive, interactive GUI application for exploring and analyzing C++ Abstract Syntax Trees (ASTs) using libclang. This professional-grade tool provides real-time visualization of C++ code structure with advanced features for developers, researchers, and educators.

![Version](https://img.shields.io/badge/version-2.1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-brightgreen)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

### 🌟 Core Functionality

- **Interactive AST Visualization**: Navigate through C++ AST nodes in an intuitive tree structure
- **Four-Panel Interface**: Synchronized views showing AST structure, node details, source code, and interactive console
- **Real-time Source Highlighting**: Automatically highlights the full extent of selected AST nodes in the source code
- **Comprehensive Node Information**: Detailed information about each AST node including type, location, and properties

### 🎨 User Interface

- **System Theme Integration**: Automatically matches macOS dark/light mode preferences
- **Responsive Layout**: Resizable panels with configurable source code viewer position (left/right)
- **Professional Appearance**: Consistent theming across all components including scrollbars
- **Status Bar**: Real-time feedback about application state and operations

### 🔍 Advanced Analysis

- **Interactive Console**: Python REPL with access to AST backend for custom analysis
- **Command History**: Navigate previous console commands with ↑/↓ arrow keys
- **Node Search**: Find specific AST node types, functions, and variables
- **Extent Highlighting**: Shows complete source range for complex constructs (classes, functions, templates)
- **Reverse Navigation**: Click on source code lines to automatically select corresponding AST nodes

### 📁 File Management

- **Auto File Monitoring**: Automatically detects external file changes and offers to reload
- **Smart Debouncing**: Prevents multiple reload dialogs for rapid file changes
- **Error Recovery**: Graceful handling of parsing errors with fallback options
- **Multiple File Support**: Easy switching between different C++ source files

### 🛠️ Developer Tools

- **Template Support**: Handles complex C++ templates with error recovery
- **Multiple C++ Standards**: Configurable parsing with different C++ standard versions
- **Diagnostic Information**: Detailed error reporting and parsing diagnostics
- **Extensible Architecture**: Modular design for easy feature additions

## Quick Start

### 🚀 One-Command Setup

**macOS/Linux:**
```bash
git clone https://github.com/your-username/clang-explorer.git
cd clang-explorer
./setup.sh && ./run_ast_explorer.sh
```

**Windows:**
```cmd
git clone https://github.com/your-username/clang-explorer.git
cd clang-explorer
setup.bat && run_ast_explorer.bat
```

### Prerequisites

- Python 3.8+ 
- libclang (LLVM/Clang development libraries)
- tkinter (usually included with Python)

### Detailed Installation

#### macOS

```bash
# Install LLVM/Clang via Homebrew
brew install llvm

# Clone the repository
git clone <repository-url>
cd clang-explorer

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run setup script
./setup.sh
```

### Alternative Setup
```bash
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### Manual Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Unix/Linux/macOS
# or
venv\Scripts\activate     # Windows
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Make sure you have LLVM installed with libclang:
```bash
# On macOS with Homebrew
brew install llvm

# On Ubuntu/Debian
sudo apt-get install libclang-dev

# On CentOS/RHEL
sudo yum install clang-devel
```

4. Update the libclang path in `ast_explorer.py` if needed:
```python
clang.cindex.Config.set_library_file('/path/to/your/libclang.dylib')
```

## Usage

### Running the Application

**With Virtual Environment (Recommended):**

```bash
./run_ast_explorer.sh     # Unix/Linux/macOS
run_ast_explorer.bat      # Windows
```

**Using Makefile (if available):**
```bash
make run                  # Run the application
```

**Manual:**
```bash
source venv/bin/activate  # Activate virtual environment
python ast_explorer.py   # Run the application
```

### Using the Interface

1. **File Menu**: Open C++ source files for analysis
2. **AST Tree View** (Top 50%): 
   - Click on nodes to select them and highlight source code
   - Expand/collapse nodes to navigate the structure
   - Use View menu to expand/collapse all nodes
3. **Source Code Viewer**: 
   - Click on any line to select the corresponding AST node (reverse navigation)
   - Automatic syntax highlighting and extent visualization
3. **Node Information** (Middle 25%):
   - Shows detailed information about the selected node
   - Includes location, type, tokens, and cursor-specific data
4. **Interactive Console** (Bottom 25%):
   - Execute Python commands to explore the AST
   - **Command History**: Use ↑/↓ arrow keys to navigate through previous commands
   - Access to `backend`, `selected`, `root` objects
   - Helper functions for common operations

### Console Commands

The interactive console provides several helpful objects and functions:

**Console Features:**
- **Command History**: Use ↑/↓ arrow keys to navigate through up to 100 previous commands
- **Auto-completion**: Python expressions support tab completion
- **Error handling**: Safe execution with detailed error messages

```python
# Available objects
backend    # AST backend instance
selected   # Currently selected node
root       # Root AST node
clang      # clang.cindex module

# Helper functions
find_by_kind('VAR_DECL')    # Find nodes by cursor kind
find_vars()                 # Find all variable declarations
find_funcs()                # Find all function declarations
help_ast()                  # Show detailed help

# Examples
selected.cursor.spelling           # Get name of selected node
len(find_vars())                   # Count variables
[n.cursor.spelling for n in find_vars()]  # List variable names
selected.get_detailed_info()       # Get all node information
```

## 📁 Project Structure

```
clang-explorer/
├── 🚀 Core Application
│   ├── ast_explorer.py           # Main application with menus  
│   ├── ast_backend.py            # AST parsing engine
│   ├── ast_ui.py                 # Four-panel GUI implementation
│   ├── run_explorer.py           # Primary entry point
│   └── clang_config.py           # libclang configuration
├── ⚙️ Setup & Configuration  
│   ├── requirements.txt          # Python dependencies
│   ├── setup.sh / setup.bat      # Cross-platform setup scripts
│   ├── run_ast_explorer.sh/.bat  # Cross-platform run scripts
│   └── Makefile                  # Build automation
├── 📚 Documentation
│   ├── README.md                 # This file
│   ├── PROJECT_STATUS.md         # Development status
│   ├── FILE_MONITORING.md        # File monitoring features
│   └── THEME_IMPLEMENTATION.md   # UI theming details
├── 📂 test/                      # C++ example and test files
│   ├── long_short.cpp            # Primary demo file
│   ├── extent_test.cpp           # Complex AST structures
│   └── monitor_test.cpp          # File monitoring testing
└── 🧪 testers/                   # Python test and demo utilities
    ├── test_theme.py             # Theme detection testing
    ├── file_monitor_demo.py      # Auto file modification demo
    └── rapid_test.py             # Dialog debouncing tests
```

## Architecture

The application is built with a professional modular architecture:

- **`ast_explorer.py`**: Main application entry point and menu handling
- **`ast_backend.py`**: Core AST parsing and data management
- **`ast_ui.py`**: Four-panel user interface components
- **`run_explorer.py`**: Simple launcher script
- **`clang_config.py`**: Cross-platform libclang detection

### Key Classes

- **`ASTExplorer`**: Main application controller
- **`ASTBackend`**: Manages clang parsing and AST data
- **`ASTNode`**: Wrapper for clang cursors with additional metadata
- **`ASTExplorerUI`**: Main UI coordinator
- **`ASTTreeView`**: Tree widget for AST display
- **`ASTInfoPanel`**: Information display panel
- **`InteractiveConsole`**: Python console for AST exploration

## Customization

The modular design makes it easy to customize:

### Adding New Node Information

Edit `ASTNode.get_detailed_info()` in `ast_backend.py`:

```python
def get_detailed_info(self) -> Dict[str, Any]:
    # Add new cursor kind handling
    if cursor.kind == clang.cindex.CursorKind.YOUR_KIND:
        info['Custom Field'] = your_custom_extraction()
    return info
```

### Adding Console Functions

Add functions to `InteractiveConsole.__init__()` in `ast_ui.py`:

```python
self.console_globals.update({
    'your_function': self._your_function,
})
```

### Modifying UI Layout

Adjust the paned window weights in `ASTExplorerUI.__init__()`:

```python
self.main_paned.add(tree_frame, weight=3)    # Larger tree view
self.main_paned.add(info_frame, weight=1)    # Smaller info panel
self.main_paned.add(console_frame, weight=2) # Larger console
```

## 📋 Example Files & Testing

The repository includes comprehensive test files and utilities:

### 📂 C++ Test Files (`test/` directory)
- **`long_short.cpp`**: Basic C++ constructs and data types
- **`long_division.cpp`**: Mathematical algorithms and functions
- **`extent_test.cpp`**: Complex structures for extent highlighting
- **`monitor_test.cpp`**: Simple file for file monitoring testing

### 🧪 Python Test Utilities (`testers/` directory)
- **`test_theme.py`**: System theme detection and UI theming tests
- **`test_console_history.py`**: Interactive console command history testing
- **`test_extents.py`**: AST extent highlighting verification
- **`file_monitor_demo.py`**: Automated file modification demonstration
- **`rapid_test.py`**: Dialog debouncing and performance testing
- **`quick_theme_test.py`**: Quick theme detection utilities

### Running Tests
```bash
# Activate virtual environment
source venv/bin/activate

# Run individual test utilities
cd testers/
python test_theme.py              # Test theme detection
python file_monitor_demo.py       # Demo file monitoring
python rapid_test.py              # Test dialog debouncing
```

## Development Commands

If you have `make` available, you can use these convenient commands:

```bash
make help     # Show available commands
make setup    # Set up virtual environment and dependencies  
make run      # Run the AST Explorer
make clean    # Clean up generated files and virtual environment
make install  # Install/reinstall dependencies
make test     # Test with sample files
```

## Troubleshooting

### Common Issues

1. **"Unknown template argument kind" errors**:
   - Try simpler C++ files without complex templates
   - Use relaxed parsing option when prompted
   - Update LLVM/Clang version

2. **libclang not found**:
   - Ensure LLVM is installed: `brew install llvm`
   - Check `clang_config.py` for proper path detection

3. **Theme issues**:
   - Restart application after changing system theme
   - Check system appearance settings

4. **File monitoring not working**:
   - Verify file permissions
   - Check if file is on network drive (may have limitations)

### Performance Tips

- Use smaller C++ files for initial exploration
- Disable file monitoring for very large files if needed
- Close unused panels if working on low-memory systems

## Contributing

The application uses a modular architecture making it easy to add new features:

- **New UI panels**: Add to `ast_ui.py`
- **Additional analysis**: Extend `ast_backend.py`
- **Menu features**: Update `ast_explorer.py`
- **Theme support**: Modify theme detection in `SourceCodeViewer`

## 🌟 What's New (September 2025)

### 🎯 Recent Updates
- **Reverse Navigation**: Click source code lines to automatically select corresponding AST nodes
- **Professional Project Structure**: Organized into logical directories (`test/`, `testers/`)
- **Cross-Platform Support**: Setup and run scripts for Windows, macOS, and Linux
- **Enhanced Documentation**: Comprehensive guides for all features
- **Improved Testing**: Dedicated test utilities with automated demos
- **Theme System**: Full system theme integration with dark/light mode support
- **File Monitoring**: Smart file change detection with debouncing
- **Command History**: Interactive console with full command history navigation

### 🏆 Production Ready Features
- ✅ Four-panel professional interface
- ✅ Real-time AST visualization  
- ✅ System theme integration
- ✅ File monitoring with smart debouncing
- ✅ Interactive Python console with history
- ✅ Source code extent highlighting
- ✅ Comprehensive error handling
- ✅ Cross-platform compatibility
- ✅ Modular, extensible architecture
- ✅ Complete documentation and test suite

## 🤝 Contributing

We welcome contributions! The modular architecture makes it easy to add features:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Run tests**: Test your changes with the provided utilities
4. **Submit a pull request**: Describe your changes and improvements

### Development Areas
- **New UI panels**: Extend `ast_ui.py` with additional visualization panels
- **Analysis features**: Add new AST analysis functions to `ast_backend.py`
- **Export options**: Add file export capabilities (JSON, XML, dot format)
- **Language support**: Extend to other clang-supported languages

## 📄 License

This project is open source under the MIT License. See LICENSE file for details.

## 🙏 Acknowledgments

- Built using [libclang](https://clang.llvm.org/doxygen/group__CINDEX.html) for robust C++ parsing
- GUI implemented with Python tkinter for cross-platform compatibility
- Inspired by the need for better C++ code understanding tools
- Designed for educational, research, and development use

## 🎯 Use Cases

This application excels in:

### 🎓 Educational
- **Teaching compiler internals** and AST concepts
- **Demonstrating C++ language features** and their AST representation
- **Compiler design courses** with hands-on AST exploration

### 🛠️ Development  
- **Debugging complex template instantiations** and metaprogramming
- **Understanding legacy code** structure and relationships
- **Code analysis** for refactoring and optimization
- **Language tool development** and AST processing

### 🔬 Research
- **Language feature analysis** and comparison
- **Code pattern recognition** and metrics collection
- **AST-based tooling development** and prototyping

---

**Ready to explore C++ like never before?** 🚀 Get started with the one-command setup above!