# System Architecture

## 🏗️ How It Works

```
┌─────────────────────────────────────────────────────────────────────┐
│                         RAG System Flow                              │
└─────────────────────────────────────────────────────────────────────┘

Step 1: Web Scraping
┌──────────────┐
│   Website    │
│  Sitemap     │  ──────>  Crawl4AI  ──────>  Markdown
│  .txt File   │             (Playwright)        Content
└──────────────┘

Step 2: Processing & Storage
Markdown  ──>  Smart      ──>  Sentence      ──>  ChromaDB
Content        Chunking        Transformer        Vector DB
               (Headers)       (Embeddings)

Step 3: Query & Retrieval
User       ──>  Similarity  ──>  Top K       ──>  Context
Question        Search          Chunks           Retrieved

Step 4: Answer Generation
Context +   ──>  Google      ──>  Intelligent ──>  User
Question        Gemini           Answer           Response
                2.0 Flash
```

---

## 📦 Component Breakdown

### 1️⃣ **insert_docs.py** - The Crawler
```
┌─────────────────────────────────────┐
│         insert_docs.py              │
├─────────────────────────────────────┤
│ • Detects URL type                  │
│ • Crawls with Crawl4AI              │
│ • Chunks markdown by headers        │
│ • Embeds with SentenceTransformer   │
│ • Stores in ChromaDB                │
└─────────────────────────────────────┘
         │
         ├─> Regular Site: Recursive crawl
         ├─> Sitemap: Batch crawl all URLs
         └─> .txt: Direct fetch & chunk
```

### 2️⃣ **rag_agent.py** - The Brain
```
┌─────────────────────────────────────┐
│          rag_agent.py               │
├─────────────────────────────────────┤
│ • Receives user question            │
│ • Queries ChromaDB for context      │
│ • Constructs prompt with context    │
│ • Sends to Gemini 2.0 Flash         │
│ • Returns intelligent answer        │
└─────────────────────────────────────┘
```

### 3️⃣ **streamlit_app.py** - The Interface
```
┌─────────────────────────────────────┐
│        streamlit_app.py             │
├─────────────────────────────────────┤
│ • Beautiful web UI                  │
│ • Chat interface                    │
│ • Streaming responses               │
│ • Config sidebar                    │
│ • Chat history                      │
└─────────────────────────────────────┘
```

### 4️⃣ **utils.py** - The Helper
```
┌─────────────────────────────────────┐
│            utils.py                 │
├─────────────────────────────────────┤
│ • ChromaDB client management        │
│ • Collection operations             │
│ • Document insertion                │
│ • Query & retrieval                 │
│ • Result formatting                 │
└─────────────────────────────────────┘
```

---

## 🔄 Data Flow Example

### Example: User asks "What is Python?"

```
1. User Input
   └─> "What is Python?"

2. ChromaDB Query
   ├─> Embed question with SentenceTransformer
   ├─> Search vector database
   └─> Retrieve top 5 most relevant chunks

3. Retrieved Chunks (Example)
   ├─> Chunk 1: "Python is a high-level programming language..."
   ├─> Chunk 2: "Python features dynamic typing..."
   ├─> Chunk 3: "Python supports multiple paradigms..."
   ├─> Chunk 4: "Python has extensive standard library..."
   └─> Chunk 5: "Python is widely used for web development..."

4. Prompt Construction
   ├─> System: "You are a helpful assistant..."
   ├─> Context: [All 5 chunks with metadata]
   └─> Question: "What is Python?"

5. Gemini Processing
   ├─> Analyzes context + question
   ├─> Generates intelligent response
   └─> Streams back to user

6. User Sees
   └─> Comprehensive answer about Python based on crawled docs
```

---

## 🧩 Technology Stack

```
Frontend:
  └─> Streamlit (Web UI)

Backend Processing:
  ├─> Python 3.11+
  ├─> Crawl4AI (Web scraping)
  └─> Playwright (Browser automation)

AI/ML:
  ├─> Google Gemini 2.0 Flash (LLM)
  └─> SentenceTransformers (Embeddings)

Data Storage:
  └─> ChromaDB (Vector database)

Utilities:
  ├─> python-dotenv (Environment)
  └─> asyncio (Async operations)
```

---

## 🎯 Workflow Scenarios

### Scenario A: Crawl Documentation Site
```
python insert_docs.py https://docs.python.org/3/
    │
    ├─> Starts at homepage
    ├─> Finds all internal links
    ├─> Crawls recursively (depth=3)
    ├─> Extracts markdown from each page
    ├─> Chunks by headers (max 1000 chars)
    ├─> Embeds each chunk
    └─> Stores in ChromaDB collection 'docs'
```

### Scenario B: Query via Web UI
```
streamlit run streamlit_app.py
    │
    ├─> Launches at http://localhost:8501
    ├─> User types question
    ├─> Retrieves context from ChromaDB
    ├─> Sends to Gemini with context
    ├─> Streams response back
    └─> Displays in chat interface
```

### Scenario C: Command Line Query
```
python rag_agent.py "How do I use decorators?"
    │
    ├─> Loads ChromaDB collection
    ├─> Searches for relevant chunks
    ├─> Constructs prompt
    ├─> Calls Gemini API
    └─> Prints response to terminal
```

---

## 🔍 Chunking Strategy Visual

```
Original Document:
┌────────────────────────────────────┐
│ # Main Title (H1)                  │
│ Introduction paragraph...          │
│                                    │
│ ## Section 1 (H2)                  │
│ Content for section 1...           │
│                                    │
│ ### Subsection 1.1 (H3)            │
│ Details for subsection...          │
│                                    │
│ ## Section 2 (H2)                  │
│ Content for section 2...           │
└────────────────────────────────────┘

After Smart Chunking:
┌────────────────────────────────────┐
│ Chunk 1 (< 1000 chars)             │
│ # Main Title                       │
│ Introduction paragraph...          │
├────────────────────────────────────┤
│ Chunk 2 (< 1000 chars)             │
│ ## Section 1                       │
│ Content for section 1...           │
├────────────────────────────────────┤
│ Chunk 3 (< 1000 chars)             │
│ ### Subsection 1.1                 │
│ Details for subsection...          │
├────────────────────────────────────┤
│ Chunk 4 (< 1000 chars)             │
│ ## Section 2                       │
│ Content for section 2...           │
└────────────────────────────────────┘

Benefits:
✓ Preserves document structure
✓ Maintains context within chunks
✓ Headers included for better understanding
✓ Optimal size for retrieval
```

---

## 💾 ChromaDB Structure

```
chroma_db/
└─> Collection: "docs"
    ├─> Document ID: "chunk-0"
    │   ├─> Text: "# Python Tutorial\nPython is..."
    │   ├─> Embedding: [0.123, -0.456, 0.789, ...]
    │   └─> Metadata:
    │       ├─> source: "https://docs.python.org/tutorial"
    │       ├─> headers: "# Python Tutorial"
    │       ├─> char_count: 847
    │       └─> word_count: 142
    │
    ├─> Document ID: "chunk-1"
    │   └─> ... (similar structure)
    │
    └─> ... (more chunks)
```

---

## 🚀 Performance Characteristics

### Crawling Speed
```
Small site (<50 pages):   ~2-5 minutes
Medium site (50-200):     ~10-20 minutes  
Large site (200-1000):    ~30-60 minutes
Massive site (1000+):     ~1-3 hours
```

### Query Speed
```
Embedding generation:     ~0.1-0.3 seconds
Vector search:            ~0.05-0.2 seconds
Gemini API call:          ~1-3 seconds (streaming)
Total response time:      ~1.5-4 seconds
```

### Resource Usage
```
Memory (crawling):        ~500MB - 2GB
Memory (querying):        ~200MB - 500MB
Disk (per 1000 chunks):   ~50-100MB (ChromaDB)
```

---

## 🎛️ Configuration Matrix

| Parameter | Small Site | Medium Site | Large Site |
|-----------|------------|-------------|------------|
| max-depth | 2 | 3 | 4-5 |
| max-concurrent | 5 | 10 | 15-20 |
| chunk-size | 800 | 1000 | 1200 |
| n-results | 3-5 | 5-7 | 7-10 |

---

## 🔐 Security Considerations

1. **API Keys**: Stored in .env (gitignored)
2. **Rate Limits**: Gemini has quota limits (monitor usage)
3. **Web Scraping**: Respect robots.txt and ToS
4. **Data Privacy**: Documents stored locally in ChromaDB

---

## 📊 Comparison Table

| Aspect | This Project | Original |
|--------|-------------|----------|
| LLM Provider | Google Gemini | OpenAI |
| Cost | Free tier + cheap | Paid only |
| Agent Framework | Direct API | Pydantic AI |
| Complexity | Simple | More complex |
| Dependencies | Fewer | More |
| Setup Time | 5 minutes | 10 minutes |
| Streaming | Native | Via framework |

---

This architecture provides a robust, scalable, and cost-effective RAG system! 🎉
