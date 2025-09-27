# Makefile for AST Explorer
# Simple commands for common development tasks

.PHONY: help setup run clean test install

help:
	@echo "AST Explorer - Available commands:"
	@echo ""
	@echo "  make setup    - Set up virtual environment and install dependencies"
	@echo "  make run      - Run the AST Explorer application"
	@echo "  make clean    - Clean up generated files and virtual environment"
	@echo "  make install  - Install/reinstall dependencies"
	@echo "  make test     - Test the application with sample files"
	@echo "  make help     - Show this help message"
	@echo ""

setup:
	@echo "Setting up AST Explorer..."
	./setup.sh

run:
	@echo "Running AST Explorer..."
	./run_ast_explorer.sh

clean:
	@echo "Cleaning up..."
	rm -rf venv/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	@echo "Cleanup complete"

install:
	@echo "Installing/reinstalling dependencies..."
	@if [ -d "venv" ]; then \
		source venv/bin/activate && pip install -r requirements.txt; \
	else \
		echo "Virtual environment not found. Run 'make setup' first."; \
	fi

test:
	@echo "Testing AST Explorer with sample files..."
	@if [ -d "venv" ]; then \
		source venv/bin/activate && python -c "from ast_backend import ASTBackend; backend = ASTBackend(); backend.parse_file('long_short.cpp'); print('✓ Sample file parsed successfully')"; \
	else \
		echo "Virtual environment not found. Run 'make setup' first."; \
	fi