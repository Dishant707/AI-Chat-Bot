# How to Build & Customize the UI

## 🎨 Quick Start - Running the UI

### 1. Basic Setup

```bash
# Make sure you're in the project directory
cd /Users/dishant/Desktop/rag

# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not already done)
pip install -r requirements.txt

# Set up your API key in .env
GEMINI_API_KEY=your_api_key_here

# Launch the UI
streamlit run streamlit_app.py
```

The UI will open at: **http://localhost:8501**

---

## 🏗️ Understanding the UI Structure

The UI is built with **Streamlit** and consists of:

```
streamlit_app.py
├── Configuration Sidebar
│   ├── Model selection dropdown
│   ├── Context documents slider
│   ├── About section
│   └── Clear chat button
│
├── Main Chat Area
│   ├── Title & caption
│   ├── Chat history display
│   ├── Chat input box
│   └── Streaming responses
│
└── Backend Integration
    ├── RAG agent connection
    ├── ChromaDB queries
    └── Gemini API calls
```

---

## 🎨 UI Customization Guide

### 1. Change Page Title & Icon

Edit `streamlit_app.py`:

```python
st.set_page_config(
    page_title="My Custom RAG Bot",  # Change this
    page_icon="🔥",                   # Change emoji/icon
    layout="wide"                     # or "centered"
)
```

### 2. Customize Main Title

```python
st.title("🔥 My Custom Documentation Assistant")
st.caption("Powered by Google Gemini and Your Knowledge Base")
```

### 3. Modify Sidebar Options

Add more models:

```python
model_choice = st.selectbox(
    "Select Gemini Model",
    [
        "gemini-2.0-flash-exp",      # Fast & Free
        "gemini-1.5-flash",           # Stable
        "gemini-1.5-pro",             # Most capable
        "gemini-1.5-flash-8b"         # Ultra fast
    ],
    index=0
)
```

Add temperature control:

```python
temperature = st.slider(
    "Response Creativity",
    min_value=0.0,
    max_value=2.0,
    value=0.7,
    step=0.1,
    help="Higher = more creative, Lower = more focused"
)
```

### 4. Add Collection Selector

```python
# In sidebar
collection_name = st.text_input(
    "Collection Name",
    value="docs",
    help="Which ChromaDB collection to query"
)
```

### 5. Custom Color Scheme

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"
```

### 6. Add File Upload for Documents

```python
# In sidebar
st.header("📄 Upload Documents")
uploaded_file = st.file_uploader(
    "Upload a text/markdown file",
    type=['txt', 'md', 'pdf']
)

if uploaded_file:
    # Process uploaded file
    content = uploaded_file.read().decode()
    st.success(f"Uploaded: {uploaded_file.name}")
```

---

## 🚀 Advanced UI Features

### 1. Add Source Citations

Modify `streamlit_app.py` to show sources:

```python
async def process_question(question: str, deps: RAGDeps, n_results: int = 5):
    """Process question and return response with sources."""
    # Retrieve context
    context_data = retrieve_with_sources(deps, question, n_results)
    
    # Show sources in expander
    with st.expander("📚 Sources Used"):
        for i, source in enumerate(context_data['sources'], 1):
            st.markdown(f"{i}. [{source['url']}]({source['url']})")
    
    # Generate response
    async for text in generate_response_stream(question, context_data['context']):
        yield text
```

### 2. Add Export Chat History

```python
# In sidebar
if st.button("💾 Export Chat"):
    chat_export = "\n\n".join([
        f"**{msg['role'].title()}:** {msg['content']}"
        for msg in st.session_state.messages
    ])
    
    st.download_button(
        label="Download Chat",
        data=chat_export,
        file_name="chat_history.md",
        mime="text/markdown"
    )
```

### 3. Add Search Statistics

```python
# After retrieval
st.sidebar.metric(
    "Documents Retrieved",
    len(query_results['documents'][0]),
    delta=None
)

st.sidebar.metric(
    "Average Relevance",
    f"{avg_relevance:.2%}",
    delta=None
)
```

### 4. Add Progress Indicators

```python
with st.spinner("🔍 Searching knowledge base..."):
    context = retrieve(deps, question, n_results)

with st.spinner("🤖 Generating response..."):
    async for chunk in generate_response_stream(question, context):
        yield chunk
```

### 5. Add Suggested Questions

```python
st.markdown("### 💡 Suggested Questions")

col1, col2 = st.columns(2)

with col1:
    if st.button("❓ What is this about?"):
        st.session_state.suggested_q = "What is this documentation about?"

with col2:
    if st.button("📖 Getting started guide"):
        st.session_state.suggested_q = "How do I get started?"
```

---

## 🎯 Complete Enhanced UI Example

Create `streamlit_app_enhanced.py`:

```python
"""Enhanced Streamlit UI with additional features."""

from dotenv import load_dotenv
import streamlit as st
import asyncio
import os
import google.generativeai as genai
from datetime import datetime

from rag_agent import RAGDeps, retrieve
from utils import get_chroma_client

load_dotenv()

# Configure page
st.set_page_config(
    page_title="Advanced RAG Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
    }
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Check API key
if not os.getenv("GEMINI_API_KEY"):
    st.error("🔑 GEMINI_API_KEY not found!")
    st.info("Please set it in your .env file")
    st.stop()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_agent_deps():
    """Initialize agent dependencies."""
    return RAGDeps(
        chroma_client=get_chroma_client("./chroma_db"),
        collection_name="docs",
        embedding_model="all-MiniLM-L6-v2"
    )

async def generate_response_stream(question: str, context: str, model_name: str, temp: float):
    """Generate streaming response from Gemini."""
    system_prompt = """You are a helpful AI assistant. Answer questions based on the provided context.
If the context doesn't contain the answer, say so clearly."""
    
    full_prompt = f"""{system_prompt}

Context:
{context}

Question: {question}

Answer:"""
    
    model = genai.GenerativeModel(
        model_name,
        generation_config={"temperature": temp}
    )
    
    response = await model.generate_content_async(full_prompt, stream=True)
    
    async for chunk in response:
        if chunk.text:
            yield chunk.text

# Main app
async def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 Advanced RAG Assistant</h1>', unsafe_allow_html=True)
    st.markdown("Ask me anything about your documentation!")
    
    # Sidebar Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model selection
        model_choice = st.selectbox(
            "🤖 AI Model",
            ["gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-pro"],
            help="Select the Gemini model"
        )
        
        # Parameters
        n_results = st.slider(
            "📚 Context Documents",
            min_value=1,
            max_value=15,
            value=5,
            help="Number of relevant documents to retrieve"
        )
        
        temperature = st.slider(
            "🌡️ Creativity",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Higher = more creative responses"
        )
        
        st.divider()
        
        # Statistics
        st.header("📊 Statistics")
        if "messages" in st.session_state:
            st.metric("💬 Total Messages", len(st.session_state.messages))
            st.metric("🔄 Conversations", len([m for m in st.session_state.messages if m["role"] == "user"]))
        
        st.divider()
        
        # Actions
        st.header("🎯 Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        
        with col2:
            if st.button("💾 Export", use_container_width=True):
                if "messages" in st.session_state and st.session_state.messages:
                    export = f"# Chat Export - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                    for msg in st.session_state.messages:
                        export += f"**{msg['role'].upper()}:**\n{msg['content']}\n\n---\n\n"
                    st.download_button(
                        "📥 Download",
                        export,
                        f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        "text/markdown",
                        use_container_width=True
                    )
        
        st.divider()
        
        # About
        with st.expander("ℹ️ About"):
            st.markdown("""
            **RAG Assistant**
            - Powered by Google Gemini
            - ChromaDB vector search
            - Crawl4AI web scraping
            
            [Documentation](./README.md)
            """)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "agent_deps" not in st.session_state:
        st.session_state.agent_deps = get_agent_deps()
    
    # Suggested questions
    if not st.session_state.messages:
        st.markdown("### 💡 Try asking:")
        cols = st.columns(3)
        
        suggestions = [
            "What is this about?",
            "How do I get started?",
            "Show me examples"
        ]
        
        for col, suggestion in zip(cols, suggestions):
            with col:
                if st.button(suggestion, use_container_width=True):
                    st.session_state.suggested_q = suggestion
                    st.rerun()
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    prompt = st.chat_input("Ask me anything...")
    
    # Handle suggested question
    if "suggested_q" in st.session_state:
        prompt = st.session_state.suggested_q
        del st.session_state.suggested_q
    
    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # Show searching status
                with st.status("🔍 Searching knowledge base...", expanded=False) as status:
                    context = retrieve(st.session_state.agent_deps, prompt, n_results)
                    status.update(label="✅ Context retrieved!", state="complete")
                
                # Generate response
                async for chunk in generate_response_stream(
                    prompt, 
                    context,
                    model_choice,
                    temperature
                ):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
                # Add to history
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                message_placeholder.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🎨 UI Styling Options

### Create `.streamlit/config.toml` for themes:

**Dark Theme (Default):**
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"
```

**Light Theme:**
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

**Purple Theme:**
```toml
[theme]
primaryColor = "#9D4EDD"
backgroundColor = "#10002B"
secondaryBackgroundColor = "#240046"
textColor = "#E0AAFF"
font = "sans serif"
```

---

## 🚀 Running Different UI Versions

```bash
# Basic UI
streamlit run streamlit_app.py

# Enhanced UI (after creating the file above)
streamlit run streamlit_app_enhanced.py

# Custom port
streamlit run streamlit_app.py --server.port 8502

# Custom theme
streamlit run streamlit_app.py --theme.base "light"
```

---

## 📱 UI Features Checklist

- ✅ Chat interface with history
- ✅ Streaming responses
- ✅ Model selection
- ✅ Adjustable parameters
- ✅ Clear chat button
- ⬜ Export chat history (add with code above)
- ⬜ Show source citations (add with code above)
- ⬜ File upload (add with code above)
- ⬜ Suggested questions (add with code above)
- ⬜ Search statistics (add with code above)

---

## 🐛 Troubleshooting UI Issues

**UI won't start:**
```bash
# Make sure Streamlit is installed
pip install streamlit

# Check for errors
streamlit run streamlit_app.py --logger.level=debug
```

**API errors in UI:**
- Check `.env` file has `GEMINI_API_KEY`
- Verify API key is valid
- Check quota at https://aistudio.google.com/

**ChromaDB errors:**
- Ensure you've crawled documents first
- Check `chroma_db` folder exists
- Try deleting and re-crawling

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Components](https://streamlit.io/components)
- [Streamlit Gallery](https://streamlit.io/gallery)

---

**Your UI is ready! Start with the basic version and customize as needed! 🎨✨**
