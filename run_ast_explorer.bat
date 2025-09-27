@echo off
REM AST Explorer Launcher Script for Windows
REM This script ensures the virtual environment is activated before running the application

setlocal enabledelayedexpansion

echo AST Explorer Launcher
echo ================================

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%venv"
set "PYTHON_SCRIPT=%SCRIPT_DIR%ast_explorer.py"

REM Check if virtual environment exists
if not exist "%VENV_DIR%" (
    echo Error: Virtual environment not found at %VENV_DIR%
    echo Please create a virtual environment first:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

REM Check if activation script exists
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Error: Virtual environment activation script not found
    echo The virtual environment may be corrupted. Please recreate it.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

REM Check if required packages are installed
echo Checking dependencies...
python -c "import clang.cindex" >nul 2>&1
if errorlevel 1 (
    echo Error: clang module not found
    echo Installing requirements...
    pip install -r "%SCRIPT_DIR%requirements.txt"
    if errorlevel 1 (
        echo Failed to install requirements
        pause
        exit /b 1
    )
)

REM Check if main script exists
if not exist "%PYTHON_SCRIPT%" (
    echo Error: Main script not found at %PYTHON_SCRIPT%
    pause
    exit /b 1
)

REM Run the application
echo Starting AST Explorer...
python "%PYTHON_SCRIPT%" %*

REM Capture exit code
set "EXIT_CODE=%ERRORLEVEL%"

REM Deactivate virtual environment
call deactivate

echo AST Explorer exited with code %EXIT_CODE%
if %EXIT_CODE% neq 0 pause
exit /b %EXIT_CODE%