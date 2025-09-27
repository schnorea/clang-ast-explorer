#!/bin/bash

# AST Explorer Setup Script
# This script sets up the virtual environment and installs dependencies

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}AST Explorer Setup${NC}"
echo "=================="

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

# Check if Python 3 is available
echo -e "${YELLOW}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 not found${NC}"
    echo "Please install Python 3.6 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}Found Python $PYTHON_VERSION${NC}"

# Check if virtual environment already exists
if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment already exists${NC}"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Removing existing virtual environment...${NC}"
        rm -rf "$VENV_DIR"
    else
        echo -e "${GREEN}Using existing virtual environment${NC}"
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create virtual environment${NC}"
        exit 1
    fi
    echo -e "${GREEN}Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install requirements
echo -e "${YELLOW}Installing requirements...${NC}"
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    pip install -r "$SCRIPT_DIR/requirements.txt"
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to install requirements${NC}"
        exit 1
    fi
else
    echo -e "${RED}requirements.txt not found${NC}"
    exit 1
fi

# Test clang import
echo -e "${YELLOW}Testing clang installation...${NC}"
python -c "import clang.cindex; print('Clang import successful')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Warning: clang module import failed${NC}"
    echo "You may need to install libclang separately:"
    echo "  macOS: brew install llvm"
    echo "  Ubuntu: sudo apt-get install libclang-dev"
    echo "  CentOS: sudo yum install clang-devel"
fi

# Deactivate virtual environment
deactivate

echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo "To run the AST Explorer:"
echo -e "  ${BLUE}./run_ast_explorer.sh${NC}     (Unix/Linux/macOS)"
echo -e "  ${BLUE}run_ast_explorer.bat${NC}      (Windows)"
echo ""
echo "Or manually:"
echo -e "  ${BLUE}source venv/bin/activate${NC}"
echo -e "  ${BLUE}python ast_explorer.py${NC}"