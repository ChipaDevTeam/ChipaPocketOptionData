#!/bin/bash

# Installation script for ChipaPocketOptionData

echo "================================================"
echo "ChipaPocketOptionData Installation"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

required_version="3.8"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.8 or higher is required"
    exit 1
fi

echo "✓ Python version is compatible"
echo ""

# Create virtual environment (optional)
read -p "Create virtual environment? (recommended) [y/N]: " create_venv
if [ "$create_venv" = "y" ] || [ "$create_venv" = "Y" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo "✓ Virtual environment created and activated"
else
    echo "Skipping virtual environment creation"
fi
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -e .

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo ""

# Install optional dependencies
read -p "Install development dependencies? [y/N]: " install_dev
if [ "$install_dev" = "y" ] || [ "$install_dev" = "Y" ]; then
    echo "Installing development dependencies..."
    pip install -e ".[dev]"
    echo "✓ Development dependencies installed"
fi
echo ""

# Create .env file from template
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo "⚠️  Please edit .env and add your SSIDs"
else
    echo ".env file already exists, skipping..."
fi
echo ""

# Run tests
echo "Running basic tests..."
python tests/test_basic.py

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo "✓ Installation completed successfully!"
    echo "================================================"
    echo ""
    echo "Next steps:"
    echo "1. Edit .env and add your PocketOption demo SSIDs"
    echo "2. Check examples/ directory for usage examples"
    echo "3. Read docs/QUICK_START.md to get started"
    echo ""
    if [ "$create_venv" = "y" ] || [ "$create_venv" = "Y" ]; then
        echo "To activate the virtual environment later, run:"
        echo "  source venv/bin/activate"
        echo ""
    fi
else
    echo ""
    echo "⚠️ Installation completed but some tests failed"
    echo "This might be expected if BinaryOptionsToolsV2 is not installed"
fi
