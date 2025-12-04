"""Gemini chatbot with URL scraping capability"""

import streamlit as st
import google.generativeai as genai
from pathlib import Path
import json
import os
import re
from datetime import datetime
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def scrape_url(url):
    """Scrape a URL and return the content."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get title
        title = soup.find('title')
        title = title.get_text() if title else url
        
        # Get main content
        main_content = soup.find('main') or soup.find('article') or soup.body
        
        if main_content:
            text = main_content.get_text(separator='\n', strip=True)
        else:
            text = soup.get_text(separator='\n', strip=True)
        
        # Clean up text
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        text = '\n'.join(lines)
        
        return {
            'success': True,
            'url': url,
            'title': title,
            'content': text[:15000],  # Limit to 15k chars
            'length': len(text)
        }
    
    except Exception as e:
        return {
            'success': False,
            'url': url,
            'error': str(e)
        }


def extract_urls_from_message(message):
    """Extract URLs from user message."""
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    urls = re.findall(url_pattern, message)
    return urls


def generate_response_stream(question, context=None, model_name="gemini-2.5-flash"):
    """Generate streaming response from Gemini."""
    model = genai.GenerativeModel(model_name)
    
    if context:
        prompt = f"""Use the following context from a scraped webpage to answer the user's question.

CONTEXT:
{context}

---

User Question: {question}

Answer based on the context provided. If the answer isn't in the context, say so."""
    else:
        prompt = question
    
    response = model.generate_content(prompt, stream=True)
    
    full_response = ""
    for chunk in response:
        if chunk.text:
            full_response += chunk.text
            yield chunk.text
    
    return full_response


def main():
    st.set_page_config(
        page_title="Gemini Chat with URL Scraping",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Gemini Chat with URL Scraping")
    st.caption("Ask questions or paste a URL to scrape and analyze")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Model selection
        model_choice = st.selectbox(
            "Select Model:",
            ["gemini-2.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-pro"]
        )
        
        st.markdown("---")
        
        st.header("💡 How to use")
        st.markdown("""
        **Paste a URL in your message:**
        - "What's on https://example.com?"
        - "Scrape https://docs.python.org and tell me about it"
        - "Analyze this website: https://github.com"
        
        **Or just chat normally:**
        - Ask any question without URLs
        """)
        
        st.markdown("---")
        
        # Scraped URLs history
        if 'scraped_urls' in st.session_state and st.session_state.scraped_urls:
            st.header("📚 Scraped URLs")
            for url_data in st.session_state.scraped_urls[-5:]:  # Show last 5
                st.text(f"• {url_data['title'][:30]}...")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.scraped_urls = []
            st.rerun()
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "scraped_urls" not in st.session_state:
        st.session_state.scraped_urls = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question or paste a URL..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Check for URLs in the message
        urls = extract_urls_from_message(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # If URLs found, scrape them first
            scraped_content = None
            if urls:
                with st.spinner(f"🕷️ Scraping {len(urls)} URL(s)..."):
                    scraped_data = []
                    for url in urls:
                        result = scrape_url(url)
                        if result['success']:
                            scraped_data.append(result)
                            st.session_state.scraped_urls.append(result)
                            st.success(f"✅ Scraped: {result['title']}")
                        else:
                            st.error(f"❌ Failed to scrape {url}: {result['error']}")
                    
                    # Combine scraped content
                    if scraped_data:
                        scraped_content = "\n\n---\n\n".join([
                            f"URL: {data['url']}\nTitle: {data['title']}\n\n{data['content']}"
                            for data in scraped_data
                        ])
            
            # Stream the response
            try:
                for chunk in generate_response_stream(prompt, scraped_content, model_choice):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                message_placeholder.error(error_msg)
                full_response = error_msg
            
            # Add assistant message to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
