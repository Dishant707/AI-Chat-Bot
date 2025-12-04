#!/usr/bin/env python3
"""
Quick UI demo script - Shows how to launch and test the UI
"""

import subprocess
import sys
import os
from pathlib import Path

def check_setup():
    """Check if basic setup is complete."""
    print("\n" + "="*60)
    print("🎨 UI Setup Checker")
    print("="*60 + "\n")
    
    checks = []
    
    # Check .env file
    if os.path.exists('.env'):
        print("✅ .env file exists")
        checks.append(True)
    else:
        print("❌ .env file not found")
        print("   Run: cp .env.example .env")
        checks.append(False)
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit is installed")
        checks.append(True)
    except ImportError:
        print("❌ Streamlit not installed")
        print("   Run: pip install streamlit")
        checks.append(False)
    
    # Check if chromadb exists
    if os.path.exists('chroma_db'):
        print("✅ ChromaDB directory exists")
        checks.append(True)
    else:
        print("⚠️  ChromaDB directory not found")
        print("   You'll need to crawl documents first:")
        print("   python insert_docs.py <URL>")
        checks.append(False)
    
    # Check streamlit_app.py
    if os.path.exists('streamlit_app.py'):
        print("✅ streamlit_app.py exists")
        checks.append(True)
    else:
        print("❌ streamlit_app.py not found")
        checks.append(False)
    
    print("\n" + "="*60)
    
    if all(checks[:2]):  # At least .env and streamlit
        return True
    else:
        return False

def show_ui_options():
    """Show UI launching options."""
    print("\n" + "="*60)
    print("🚀 UI Launch Options")
    print("="*60 + "\n")
    
    print("1. Basic UI (Recommended for first time)")
    print("   streamlit run streamlit_app.py")
    print()
    print("2. UI on custom port")
    print("   streamlit run streamlit_app.py --server.port 8502")
    print()
    print("3. UI with light theme")
    print("   streamlit run streamlit_app.py --theme.base light")
    print()
    print("4. UI in browser mode (no menu)")
    print("   streamlit run streamlit_app.py --server.headless true")
    print()

def main():
    """Main demo function."""
    print("""
╔═══════════════════════════════════════════════════════════╗
║           RAG Web Scraper - UI Demo & Launcher           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Check setup
    if not check_setup():
        print("\n⚠️  Please complete the setup first!")
        print("\nQuick setup:")
        print("1. cp .env.example .env")
        print("2. Add GEMINI_API_KEY to .env")
        print("3. pip install -r requirements.txt")
        print("4. python insert_docs.py <URL>  # Crawl some docs first")
        return
    
    # Show options
    show_ui_options()
    
    print("="*60)
    print("\n💡 Tips:")
    print("   • The UI will open at http://localhost:8501")
    print("   • Press Ctrl+C to stop the server")
    print("   • Edit streamlit_app.py to customize")
    print("   • See UI_GUIDE.md for customization examples")
    print()
    
    # Ask to launch
    response = input("Would you like to launch the UI now? (y/n): ")
    
    if response.lower() == 'y':
        print("\n🚀 Launching Streamlit UI...")
        print("   Opening at http://localhost:8501")
        print("   Press Ctrl+C to stop\n")
        
        try:
            subprocess.run(["streamlit", "run", "streamlit_app.py"])
        except KeyboardInterrupt:
            print("\n\n👋 UI stopped. See you next time!")
        except FileNotFoundError:
            print("\n❌ Streamlit not found. Install it with:")
            print("   pip install streamlit")
    else:
        print("\n👍 No problem! Run this when you're ready:")
        print("   streamlit run streamlit_app.py")
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled. Goodbye!")
        sys.exit(0)
