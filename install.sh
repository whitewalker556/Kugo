#!/bin/bash
# Installation script for Kugo

set -e

echo "🚀 Installing Kugo - Hugo Front-end for KDE/Plasma"
echo "=================================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if Hugo is available
if ! command -v hugo &> /dev/null; then
    echo "⚠️  Hugo is not installed. Please install Hugo first:"
    echo "   Ubuntu/Debian: sudo apt install hugo"
    echo "   Or visit: https://gohugo.io/installation/"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "📦 Installing Python dependencies..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✓ Created virtual environment"
fi

# Activate virtual environment and install dependencies
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✓ Dependencies installed"

# Run tests
echo "🧪 Running tests..."
python test_kugo.py

if [ $? -eq 0 ]; then
    echo "✅ Installation successful!"
    echo ""
    echo "To run Kugo:"
    echo "  ./run_kugo.sh"
    echo "  or"
    echo "  source .venv/bin/activate && python main.py"
    echo ""
    echo "To install desktop entry (optional):"
    echo "  ./install_desktop.sh"
else
    echo "❌ Installation failed. Please check the errors above."
    exit 1
fi
