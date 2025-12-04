# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Run Setup Script

```bash
cd /Users/dishant/Desktop/rag
./setup.sh
```

Or manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
cp .env.example .env
```

### Step 2: Get Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key

### Step 3: Configure Environment

Edit `.env` file:

```bash
nano .env
# or
code .env
```

Add your API key:

```env
GEMINI_API_KEY=your_actual_api_key_here
MODEL_CHOICE=gemini-2.0-flash-exp
```

### Step 4: Crawl a Website

Example with Python documentation:

```bash
python insert_docs.py https://docs.python.org/3/tutorial/ --collection python_tutorial
```

This will:
- Crawl the website recursively
- Extract and chunk the content
- Store it in ChromaDB for retrieval

### Step 5: Launch the Web Interface

```bash
streamlit run streamlit_app.py
```

Open your browser to [http://localhost:8501](http://localhost:8501)

### Step 6: Ask Questions!

Type your questions in the chat interface and get intelligent answers based on the crawled documentation.

---

## 📝 Example Questions to Try

After crawling Python docs:
- "How do I create a class in Python?"
- "What are Python decorators?"
- "Explain list comprehensions"

After crawling your own docs:
- Ask specific questions about your documentation
- Request code examples
- Get explanations of concepts

---

## 🎯 Tips for Best Results

1. **Crawl Quality Documentation**: The better the source, the better the answers
2. **Adjust Context Size**: Use 3-5 documents for focused answers, 7-10 for comprehensive ones
3. **Use Clear Questions**: Be specific in your queries
4. **Check Source URLs**: The response shows which documents were used

---

## 🔧 Common Commands

### Crawl a Regular Website
```bash
python insert_docs.py https://example.com/docs
```

### Crawl from Sitemap
```bash
python insert_docs.py https://example.com/sitemap.xml
```

### Crawl Markdown File
```bash
python insert_docs.py https://example.com/docs.txt
```

### Use Custom Collection
```bash
python insert_docs.py <URL> --collection my_docs
```

### Query from Command Line
```bash
python rag_agent.py "Your question here" --collection my_docs
```

---

## 📊 Project Files Overview

| File | Purpose |
|------|---------|
| `insert_docs.py` | Crawls websites and stores in ChromaDB |
| `rag_agent.py` | RAG logic with Gemini |
| `streamlit_app.py` | Web interface |
| `utils.py` | Helper functions |
| `requirements.txt` | Python dependencies |
| `.env` | Your API keys (don't commit!) |
| `README.md` | Full documentation |

---

## 🆘 Need Help?

- Check `README.md` for detailed documentation
- Ensure your Gemini API key is valid
- Make sure you've run `playwright install`
- Try reducing `--max-concurrent` if crawling fails

---

**Ready to build your intelligent documentation assistant! 🤖✨**
