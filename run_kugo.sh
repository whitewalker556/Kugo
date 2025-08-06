#!/bin/bash
# Runner script for Kugo

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run ./install.sh first."
    exit 1
fi

echo "🚀 Starting Kugo..."
source .venv/bin/activate
python main.py
