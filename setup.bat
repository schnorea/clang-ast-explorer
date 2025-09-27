@echo off
REM AST Explorer Setup Script for Windows
REM This script sets up the virtual environment and installs dependencies

setlocal enabledelayedexpansion

echo AST Explorer Setup
echo ==================

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%venv"

REM Check if Python is available
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: python not found
    echo Please install Python 3.6 or higher and add it to PATH
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%i"
echo Found Python %PYTHON_VERSION%

REM Check if virtual environment already exists
if exist "%VENV_DIR%" (
    echo Virtual environment already exists
    set /p "RECREATE=Do you want to recreate it? (y/N): "
    if /i "!RECREATE!"=="y" (
        echo Removing existing virtual environment...
        rmdir /s /q "%VENV_DIR%"
    ) else (
        echo Using existing virtual environment
    )
)

REM Create virtual environment if it doesn't exist
if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements...
if exist "%SCRIPT_DIR%requirements.txt" (
    pip install -r "%SCRIPT_DIR%requirements.txt"
    if errorlevel 1 (
        echo Failed to install requirements
        pause
        exit /b 1
    )
) else (
    echo requirements.txt not found
    pause
    exit /b 1
)

REM Test clang import
echo Testing clang installation...
python -c "import clang.cindex; print('Clang import successful')" >nul 2>&1
if errorlevel 1 (
    echo Warning: clang module import failed
    echo You may need to install libclang separately
    echo See the README for platform-specific instructions
)

REM Deactivate virtual environment
call deactivate

echo.
echo Setup complete!
echo.
echo To run the AST Explorer:
echo   run_ast_explorer.bat      (Windows)
echo   ./run_ast_explorer.sh     (Unix/Linux/macOS)
echo.
echo Or manually:
echo   venv\Scripts\activate
echo   python ast_explorer.py
pause