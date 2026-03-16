@echo off
setlocal enabledelayedexpansion

echo --- Installing Repo-Agent ---

:: 1. Check if python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.
    pause
    exit /b 1
)

:: 2. Create virtual environment if it doesn't exist
if not exist "env" (
    echo Creating virtual environment...
    python -m venv env
)

:: 3. Install requirements
echo Installing dependencies...
call env\Scripts\activate.bat
pip install -r requirements.txt

:: 4. Create a global command script (ra.bat)
:: We'll create it in the current directory and suggest the user adds this directory to their PATH
echo @echo off>ra.bat
echo set REPO_AGENT_DIR=%~dp0>>ra.bat
echo call "%%REPO_AGENT_DIR%%env\Scripts\activate.bat">>ra.bat
echo python "%%REPO_AGENT_DIR%%scripts\cli.py" %%*>>ra.bat

echo.
echo --- Installation Complete ---
echo To use repo-agent from anywhere:
echo 1. Add this directory to your PATH: %~dp0
echo 2. Or run it directly using: %~dp0ra.bat
echo.
echo You can now run 'ra' in this directory.
pause
