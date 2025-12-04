#!/usr/bin/env python3
"""
Example crawling script demonstrating different use cases.
Run this after setting up your environment and API key.
"""

import subprocess
import sys

def run_command(description, command):
    """Run a command and print the description."""
    print(f"\n{'='*60}")
    print(f"📌 {description}")
    print(f"{'='*60}")
    print(f"Command: {command}")
    print()
    
    response = input("Run this command? (y/n): ")
    if response.lower() == 'y':
        result = subprocess.run(command, shell=True)
        if result.returncode == 0:
            print("✅ Success!")
        else:
            print("❌ Command failed")
            return False
    else:
        print("⏭️  Skipped")
    return True

def main():
    """Main function with example crawling commands."""
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║     RAG Web Scraper - Example Crawling Demonstrations     ║
╚═══════════════════════════════════════════════════════════╝

This script will guide you through different crawling examples.
You can choose which ones to run.
    """)
    
    examples = [
        {
            "description": "Crawl Pydantic AI Documentation (Regular Site)",
            "command": "python insert_docs.py https://ai.pydantic.dev/ --collection pydantic_docs --max-depth 2"
        },
        {
            "description": "Crawl Python Tutorial (Regular Site)",
            "command": "python insert_docs.py https://docs.python.org/3/tutorial/ --collection python_tutorial --max-depth 2"
        },
        {
            "description": "Crawl from a .txt file (llms.txt format)",
            "command": "python insert_docs.py https://ai.pydantic.dev/llms-full.txt --collection pydantic_llms"
        },
        {
            "description": "Crawl from a sitemap",
            "command": "python insert_docs.py https://www.example.com/sitemap.xml --collection example_docs"
        },
        {
            "description": "Crawl with custom chunk size (smaller chunks)",
            "command": "python insert_docs.py https://docs.python.org/3/ --collection python_docs --chunk-size 500 --max-depth 1"
        },
        {
            "description": "Crawl with more concurrent connections (faster)",
            "command": "python insert_docs.py https://example.com/docs --collection fast_crawl --max-concurrent 20 --max-depth 2"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{'#'*60}")
        print(f"Example {i} of {len(examples)}")
        print(f"{'#'*60}")
        
        if not run_command(example["description"], example["command"]):
            continue_response = input("\nContinue with more examples? (y/n): ")
            if continue_response.lower() != 'y':
                break
    
    print("""
\n╔═══════════════════════════════════════════════════════════╗
║                    Examples Complete!                      ║
╚═══════════════════════════════════════════════════════════╝

Next steps:
1. Launch the Streamlit interface:
   streamlit run streamlit_app.py

2. Or query from command line:
   python rag_agent.py "Your question here" --collection <collection_name>

3. Check your ChromaDB:
   ls -la chroma_db/

Happy querying! 🚀
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrupted by user. Exiting...")
        sys.exit(0)
