"""Simple Streamlit demo without ChromaDB - Just Gemini Chat"""

from dotenv import load_dotenv
import streamlit as st
import asyncio
import os
import google.generativeai as genai

load_dotenv()

# Check for Gemini API key
if not os.getenv("GEMINI_API_KEY"):
    st.error("🔑 GEMINI_API_KEY environment variable not set.")
    st.info("Please add your Gemini API key to the .env file")
    st.code("GEMINI_API_KEY=your_key_here")
    st.markdown("[Get your API key here](https://aistudio.google.com/app/apikey)")
    st.stop()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


async def generate_response_stream(question: str, model_name: str = "gemini-2.5-flash"):
    """Generate streaming response from Gemini."""
    model = genai.GenerativeModel(model_name)
    
    response = await model.generate_content_async(
        question,
        stream=True
    )
    
    async for chunk in response:
        if chunk.text:
            yield chunk.text


async def main():
    st.set_page_config(
        page_title="Gemini Chat Demo",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Google Gemini Chat Demo")
    st.caption("Simple chat with Gemini 2.5 Flash")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        model_choice = st.selectbox(
            "Select Gemini Model",
            ["gemini-2.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-pro"],
            index=0
        )
        
        st.divider()
        
        st.markdown("### 📚 About")
        st.markdown("""
        This is a simple demo of Google Gemini.
        
        **Note:** This version doesn't include:
        - ChromaDB (requires Python 3.11/3.12)
        - Web scraping
        - RAG functionality
        
        To use the full version, install Python 3.11 or 3.12.
        """)
        
        st.divider()
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                async for chunk in generate_response_stream(prompt, model_choice):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
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
