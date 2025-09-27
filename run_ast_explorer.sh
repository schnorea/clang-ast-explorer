#!/bin/bash

# AST Explorer Launcher Script
# This script ensures the virtual environment is activated before running the application

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
PYTHON_SCRIPT="$SCRIPT_DIR/ast_explorer.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}AST Explorer Launcher${NC}"
echo "================================"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${RED}Error: Virtual environment not found at $VENV_DIR${NC}"
    echo "Please create a virtual environment first:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Check if activation script exists
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo -e "${RED}Error: Virtual environment activation script not found${NC}"
    echo "The virtual environment may be corrupted. Please recreate it."
    exit 1
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

# Check if required packages are installed
echo -e "${YELLOW}Checking dependencies...${NC}"
python -c "import clang.cindex" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: clang module not found${NC}"
    echo "Installing requirements..."
    pip install -r "$SCRIPT_DIR/requirements.txt"
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to install requirements${NC}"
        exit 1
    fi
fi

# Check if main script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo -e "${RED}Error: Main script not found at $PYTHON_SCRIPT${NC}"
    exit 1
fi

# Run the application
echo -e "${GREEN}Starting AST Explorer...${NC}"
python "$PYTHON_SCRIPT" "$@"

# Capture exit code
EXIT_CODE=$?

# Deactivate virtual environment
deactivate

echo -e "${GREEN}AST Explorer exited with code $EXIT_CODE${NC}"
exit $EXIT_CODE