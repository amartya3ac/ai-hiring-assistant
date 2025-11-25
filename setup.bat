@echo off
REM TalentScout Hiring Assistant - Setup and Run Script (Windows)
REM This script sets up the environment and runs the application

echo.
echo ==========================================
echo TalentScout Hiring Assistant Setup
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo. Python found: %PYTHON_VERSION%

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo.
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit .env and add your OPENAI_API_KEY
    echo.
    pause
)

REM Run tests
echo.
echo Running tests...
python -m pytest tests.py -v

REM Run the application
echo.
echo Starting TalentScout Hiring Assistant...
echo Open your browser at http://localhost:8501
echo.
streamlit run streamlit_app.py

echo.
echo Application closed.
pause
