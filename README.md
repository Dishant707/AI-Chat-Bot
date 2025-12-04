# Web Scraper & RAG Agent with Google Gemini

An intelligent documentation crawler and retrieval-augmented generation (RAG) system, powered by **Crawl4AI**, **ChromaDB**, and **Google Gemini 2.0 Flash**. This project enables you to crawl, chunk, and vectorize documentation from any website, `.txt`/Markdown pages, or sitemap, and interact with the knowledge base using a Streamlit interface.

---

## ✨ Features

- **🕷️ Flexible documentation crawling:** Handles regular websites, `.txt`/Markdown pages (llms.txt), and sitemaps
- **⚡ Parallel and recursive crawling:** Efficiently gathers large doc sites with memory-adaptive batching
- **📝 Smart chunking:** Hierarchical Markdown chunking by headers, ensuring chunks are optimal for vector search
- **🗃️ Vector database integration:** Stores chunks and metadata in ChromaDB for fast semantic retrieval
- **🤖 Gemini-powered RAG:** Query your documentation with Google Gemini 2.0 Flash for intelligent responses
- **🎨 Streamlit interface:** Beautiful web UI for interactive question-answering
- **🔧 Extensible:** Modular design for easy customization and extension

---

## 📋 Prerequisites

- Python 3.11+
- Google Gemini API key (for LLM-powered search)
- Crawl4AI/Playwright and other dependencies in `requirements.txt`
- Streamlit for the web interface

---

## 🚀 Installation

### 1. Clone or Navigate to the Repository

```bash
cd /Users/dishant/Desktop/rag
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
playwright install
```

### 4. Set Up Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
MODEL_CHOICE=gemini-2.0-flash-exp
```

**Get your Gemini API key:**
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy and paste it into your `.env` file

---

## 📖 Usage

### 1. Crawling and Inserting Documentation

The main entry point for crawling and vectorizing documentation is `insert_docs.py`.

#### Supported URL Types

- **Regular documentation sites:** Recursively crawls all internal links
- **Markdown or .txt pages (such as llms.txt):** Fetches and chunks Markdown content
- **Sitemaps (`sitemap.xml`):** Batch-crawls all URLs listed in the sitemap

#### Basic Usage

```bash
python insert_docs.py <URL> [OPTIONS]
```

#### Examples

**Crawl a regular documentation site:**
```bash
python insert_docs.py https://ai.pydantic.dev/ --collection pydantic_docs
```

**Crawl a .txt/Markdown file:**
```bash
python insert_docs.py https://ai.pydantic.dev/llms-full.txt --collection pydantic_docs
```

**Crawl from a sitemap:**
```bash
python insert_docs.py https://ai.pydantic.dev/sitemap.xml --collection pydantic_docs
```

#### Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `url` | URL to crawl (required) | - |
| `--collection` | ChromaDB collection name | `docs` |
| `--db-dir` | Directory for ChromaDB data | `./chroma_db` |
| `--embedding-model` | Embedding model for vectors | `all-MiniLM-L6-v2` |
| `--chunk-size` | Maximum characters per chunk | `1000` |
| `--max-depth` | Recursion depth for regular URLs | `3` |
| `--max-concurrent` | Max parallel browser sessions | `10` |
| `--batch-size` | ChromaDB insertion batch size | `100` |

#### Chunking Strategy

- Splits content hierarchically: `#` → `##` → `###` headers
- If a chunk is still too large, splits by character count
- All chunks are less than the specified `--chunk-size`
- Each chunk includes metadata: source URL, headers, word/char counts

---

### 2. Running the Streamlit RAG Interface

After crawling and inserting docs, launch the Streamlit app for interactive Q&A:

```bash
streamlit run streamlit_app.py
```

The interface will be available at [http://localhost:8501](http://localhost:8501)

**Features:**
- 💬 Interactive chat interface
- 🎛️ Adjustable context retrieval settings
- 🔄 Real-time streaming responses from Gemini
- 📊 Clear chat history option
- 🎨 Beautiful, user-friendly UI

---

### 3. Using the RAG Agent from Command Line

You can also query your documentation directly from the command line:

```bash
python rag_agent.py "What is Pydantic AI?" --collection pydantic_docs
```

**Arguments:**
- First argument: Your question (required)
- `--collection`: ChromaDB collection name (default: `docs`)
- `--db-dir`: ChromaDB directory (default: `./chroma_db`)
- `--embedding-model`: Embedding model (default: `all-MiniLM-L6-v2`)
- `--n-results`: Number of context documents (default: `5`)
- `--model`: Gemini model to use (default: `gemini-2.0-flash-exp`)

---

## 📁 Project Structure

```
rag/
├── insert_docs.py          # Main crawler script
├── rag_agent.py            # RAG agent with Gemini
├── streamlit_app.py        # Web interface
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .env                    # Your actual environment variables (create this)
├── README.md               # This file
└── chroma_db/              # ChromaDB storage (created automatically)
```

---

## 🔧 Advanced Usage & Customization

### Tune Chunking

Adjust `--chunk-size` based on your use case:
- Smaller chunks (500-800): Better for precise retrieval
- Larger chunks (1000-1500): More context per retrieval

### Change Embedding Model

Use different embedding models with `--embedding-model`:
```bash
python insert_docs.py <URL> --embedding-model sentence-transformers/all-mpnet-base-v2
```

### Crawling Large Sites

For large sites, adjust these parameters:
```bash
python insert_docs.py <URL> --max-depth 5 --max-concurrent 20
```

### Multiple Collections

Organize different documentation sets into separate collections:
```bash
python insert_docs.py https://docs.python.org --collection python_docs
python insert_docs.py https://docs.djangoproject.com --collection django_docs
```

Then query specific collections:
```bash
streamlit run streamlit_app.py  # Edit code to specify collection
# or
python rag_agent.py "Your question" --collection python_docs
```

---

## 🐛 Troubleshooting

### Missing Dependencies
```bash
pip install -r requirements.txt
playwright install
```

### Gemini API Errors
- Ensure your API key is valid and has quota
- Check that `GEMINI_API_KEY` is set in `.env`
- Try using `gemini-1.5-flash` if `gemini-2.0-flash-exp` has issues

### Crawling Issues
- Reduce `--max-concurrent` if you encounter memory issues
- Increase `--max-depth` if not all pages are being crawled
- Some sites may block automated crawling - respect robots.txt

### ChromaDB Issues
- Delete the `chroma_db` directory and re-crawl if you encounter errors
- Ensure you have write permissions in the project directory

---

## 🎯 Comparison with Original Project

This project is adapted from the [ottomator-agents](https://github.com/coleam00/ottomator-agents) repository, with the following key changes:

| Feature | Original | This Version |
|---------|----------|--------------|
| **LLM** | OpenAI GPT | Google Gemini 2.0 Flash |
| **Agent Framework** | Pydantic AI | Direct Gemini API |
| **API Cost** | Paid (OpenAI) | Free tier available (Gemini) |
| **Streaming** | Via Pydantic AI | Native Gemini streaming |
| **Setup** | OpenAI account required | Google account required |

---

## 📝 Example Workflow

1. **Crawl documentation:**
   ```bash
   python insert_docs.py https://docs.example.com --collection example_docs
   ```

2. **Launch Streamlit interface:**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Ask questions in the web interface and get intelligent responses!**

---

## 🤝 Contributing

Feel free to open issues or submit pull requests for improvements!

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

- Original project: [ottomator-agents](https://github.com/coleam00/ottomator-agents) by Cole Medin
- Powered by [Crawl4AI](https://github.com/unclecode/crawl4ai)
- Vector database: [ChromaDB](https://www.trychroma.com/)
- LLM: [Google Gemini](https://ai.google.dev/)

---

## 📚 Additional Resources

- [Google Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Crawl4AI Documentation](https://crawl4ai.com/mkdocs/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Happy Scraping! 🚀**
