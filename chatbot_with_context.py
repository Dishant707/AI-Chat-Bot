"""Gemini chatbot with scraped data as context"""

import streamlit as st
import google.generativeai as genai
from pathlib import Path
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def load_scraped_data(file_path):
    """Load scraped data from JSON, markdown, or text file."""
    path = Path(file_path)
    
    if not path.exists():
        return None
    
    if path.suffix == '.json':
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Combine all content
            context = "\n\n".join([
                f"Source: {item['url']}\nTitle: {item['title']}\n{item['content']}"
                for item in data
            ])
            return context
    
    elif path.suffix in ['.md', '.txt']:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    return None


def generate_response_with_context(question, context, model_name="gemini-2.5-flash"):
    """Generate response using Gemini with scraped data as context."""
    
    system_prompt = f"""You are a helpful AI assistant. Use the following context from scraped web pages to answer questions accurately.

If the answer is in the context, cite it. If not, say you don't have that information in the provided context.

CONTEXT:
{context[:10000]}  # Limit to first 10k chars to avoid token limits

---

Answer the user's question based on the above context."""

    model = genai.GenerativeModel(model_name)
    
    # Combine system prompt with user question
    full_prompt = f"{system_prompt}\n\nUser Question: {question}"
    
    response = model.generate_content(full_prompt)
    return response.text


def main():
    st.set_page_config(
        page_title="Gemini Chat with Scraped Data",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Gemini Chat with Scraped Knowledge")
    st.caption("Ask questions based on your scraped website data")
    
    # Sidebar for file selection
    with st.sidebar:
        st.header("📚 Knowledge Base")
        
        # Get all scraped files
        scraped_files = list(Path('.').glob('scraped_data_*.*'))
        
        if not scraped_files:
            st.error("No scraped data files found! Run simple_scraper.py first.")
            st.stop()
        
        file_options = {f.name: str(f) for f in scraped_files}
        selected_file = st.selectbox(
            "Select scraped data file:",
            options=list(file_options.keys())
        )
        
        # Model selection
        model_choice = st.selectbox(
            "Select Model:",
            ["gemini-2.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-pro"]
        )
        
        if st.button("🔄 Reload Data"):
            st.rerun()
    
    # Load context
    if 'context' not in st.session_state or selected_file != st.session_state.get('current_file'):
        context_path = file_options[selected_file]
        st.session_state.context = load_scraped_data(context_path)
        st.session_state.current_file = selected_file
        
        if st.session_state.context:
            st.sidebar.success(f"✅ Loaded {len(st.session_state.context)} characters")
        else:
            st.sidebar.error("❌ Failed to load data")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about the scraped content..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = generate_response_with_context(
                        prompt, 
                        st.session_state.context,
                        model_choice
                    )
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Clear chat button
    if st.sidebar.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


if __name__ == "__main__":
    main()
