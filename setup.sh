#!/bin/bash

# Setup script for RAG Web Scraper with Gemini

echo "🚀 Setting up RAG Web Scraper with Gemini..."
echo ""

# Check if Python 3.11+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Install Playwright browsers
echo "🎭 Installing Playwright browsers..."
playwright install
echo "✅ Playwright browsers installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your GEMINI_API_KEY"
    echo "   Get your API key from: https://aistudio.google.com/app/apikey"
else
    echo "ℹ️  .env file already exists"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Edit .env file and add your GEMINI_API_KEY"
echo "3. Crawl a website: python insert_docs.py <URL>"
echo "4. Launch the web interface: streamlit run streamlit_app.py"
echo ""
echo "For more information, see README.md"
