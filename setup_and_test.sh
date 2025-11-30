#!/bin/bash

echo "=========================================="
echo "Setting up Selenium Test Environment"
echo "=========================================="

# Setup Python virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run tests
echo ""
echo "=========================================="
echo "Running tests..."
echo "=========================================="
pytest -m "UI or API" -v

# Generate Allure test reports
echo ""
echo "=========================================="
echo "Generating Allure reports..."
echo "=========================================="
allure serve allure-results
