#!/usr/bin/env python3
"""
Test script to verify the installation and basic functionality.
Run this after setup to ensure everything is working correctly.
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.11+"""
    version = sys.version_info
    print("🐍 Checking Python version...")
    print(f"   Found: Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 11:
        print("   ✅ Python version is compatible")
        return True
    else:
        print("   ❌ Python 3.11+ is required")
        return False

def check_env_file():
    """Check if .env file exists and has API key"""
    print("\n🔐 Checking environment configuration...")
    
    if not os.path.exists('.env'):
        print("   ❌ .env file not found")
        print("   Run: cp .env.example .env")
        return False
    
    print("   ✅ .env file exists")
    
    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("   ⚠️  GEMINI_API_KEY not set in .env")
        print("   Please add your Gemini API key to .env file")
        return False
    
    print("   ✅ GEMINI_API_KEY is configured")
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        ('google.generativeai', 'google-generativeai'),
        ('chromadb', 'chromadb'),
        ('crawl4ai', 'Crawl4AI'),
        ('streamlit', 'streamlit'),
        ('dotenv', 'python-dotenv'),
        ('sentence_transformers', 'sentence-transformers'),
    ]
    
    all_installed = True
    
    for module_name, package_name in required_packages:
        try:
            __import__(module_name)
            print(f"   ✅ {package_name}")
        except ImportError:
            print(f"   ❌ {package_name} not installed")
            all_installed = False
    
    if not all_installed:
        print("\n   Run: pip install -r requirements.txt")
    
    return all_installed

def check_playwright():
    """Check if Playwright browsers are installed"""
    print("\n🎭 Checking Playwright installation...")
    
    try:
        from playwright.sync_api import sync_playwright
        print("   ✅ Playwright package installed")
        
        # Try to launch a browser to check if browsers are installed
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                browser.close()
            print("   ✅ Playwright browsers installed")
            return True
        except Exception as e:
            print("   ⚠️  Playwright browsers may not be installed")
            print("   Run: playwright install")
            return False
            
    except ImportError:
        print("   ❌ Playwright not installed")
        return False

def check_project_files():
    """Check if all project files exist"""
    print("\n📁 Checking project files...")
    
    required_files = [
        'insert_docs.py',
        'rag_agent.py',
        'streamlit_app.py',
        'utils.py',
        'requirements.txt',
        '.env.example',
        'README.md',
    ]
    
    all_exist = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} missing")
            all_exist = False
    
    return all_exist

def test_gemini_connection():
    """Test connection to Gemini API"""
    print("\n🤖 Testing Gemini API connection...")
    
    try:
        import google.generativeai as genai
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key or api_key == 'your_gemini_api_key_here':
            print("   ⏭️  Skipping (API key not configured)")
            return None
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        response = model.generate_content("Say 'Hello, RAG!'")
        
        if response.text:
            print("   ✅ Gemini API connection successful")
            print(f"   Response: {response.text[:50]}...")
            return True
        else:
            print("   ❌ Gemini API returned empty response")
            return False
            
    except Exception as e:
        print(f"   ❌ Gemini API connection failed: {str(e)}")
        return False

def test_chromadb():
    """Test ChromaDB initialization"""
    print("\n🗃️  Testing ChromaDB...")
    
    try:
        from utils import get_chroma_client, get_or_create_collection
        
        # Create a test collection
        client = get_chroma_client("./test_chroma_db")
        collection = get_or_create_collection(client, "test_collection")
        
        print("   ✅ ChromaDB initialized successfully")
        
        # Clean up
        import shutil
        if os.path.exists("./test_chroma_db"):
            shutil.rmtree("./test_chroma_db")
        
        return True
        
    except Exception as e:
        print(f"   ❌ ChromaDB test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║         RAG Web Scraper - Installation Test               ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    results = {
        'Python Version': check_python_version(),
        'Environment File': check_env_file(),
        'Dependencies': check_dependencies(),
        'Playwright': check_playwright(),
        'Project Files': check_project_files(),
        'Gemini API': test_gemini_connection(),
        'ChromaDB': test_chromadb(),
    }
    
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v is True)
    skipped = sum(1 for v in results.values() if v is None)
    failed = sum(1 for v in results.values() if v is False)
    total = len(results)
    
    for test, result in results.items():
        if result is True:
            status = "✅ PASS"
        elif result is None:
            status = "⏭️  SKIP"
        else:
            status = "❌ FAIL"
        print(f"{status:12} {test}")
    
    print("="*60)
    print(f"Results: {passed} passed, {failed} failed, {skipped} skipped out of {total} tests")
    print("="*60)
    
    if failed > 0:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Install Playwright: playwright install")
        print("3. Configure .env: cp .env.example .env && edit .env")
        print("4. Add your GEMINI_API_KEY to .env")
    else:
        print("\n✅ All tests passed! Your installation is ready.")
        print("\n🚀 Next steps:")
        print("1. Crawl a website: python insert_docs.py <URL>")
        print("2. Launch interface: streamlit run streamlit_app.py")
        print("3. See examples: python examples.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user.")
        sys.exit(1)
