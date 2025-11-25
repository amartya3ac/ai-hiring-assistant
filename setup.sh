#!/bin/bash
# TalentScout Hiring Assistant - Setup and Run Script
# This script sets up the environment and runs the application

echo "=========================================="
echo "TalentScout Hiring Assistant Setup"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env and add your OPENAI_API_KEY"
    echo ""
    read -p "Press Enter after you've set your API key..."
fi

# Run tests
echo ""
echo "Running tests..."
python -m pytest tests.py -v

# Run the application
echo ""
echo "Starting TalentScout Hiring Assistant..."
streamlit run streamlit_app.py

echo ""
echo "Application closed."
