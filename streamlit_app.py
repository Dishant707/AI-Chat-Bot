"""Streamlit web interface for the RAG agent with Gemini."""

from dotenv import load_dotenv
import streamlit as st
import asyncio
import os
import google.generativeai as genai

from rag_agent import RAGDeps, retrieve
from utils import get_chroma_client

load_dotenv()

# Check for Gemini API key
if not os.getenv("GEMINI_API_KEY"):
    st.error("Error: GEMINI_API_KEY environment variable not set.")
    st.info("Please create a .env file with your Gemini API key or set it in your environment.")
    st.stop()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def get_agent_deps():
    """Initialize agent dependencies."""
    return RAGDeps(
        chroma_client=get_chroma_client("./chroma_db"),
        collection_name="docs",
        embedding_model="all-MiniLM-L6-v2"
    )


async def generate_response_stream(question: str, context: str, model_name: str = "gemini-2.0-flash-exp"):
    """Generate streaming response from Gemini.
    
    Args:
        question: User's question
        context: Retrieved context from ChromaDB
        model_name: Gemini model to use
        
    Yields:
        Text chunks from the streaming response
    """
    system_prompt = """You are a helpful assistant that answers questions based on the provided documentation.
Use the context information provided to answer the user's question accurately.
If the documentation doesn't contain the answer, clearly state that the information isn't available 
in the current documentation and provide your best general knowledge response."""
    
    full_prompt = f"""{system_prompt}

{context}

User Question: {question}

Please provide a comprehensive answer based on the context above."""
    
    # Initialize Gemini model
    model = genai.GenerativeModel(model_name)
    
    # Generate streaming response
    response = await model.generate_content_async(
        full_prompt,
        stream=True
    )
    
    async for chunk in response:
        if chunk.text:
            yield chunk.text


async def process_question(question: str, deps: RAGDeps, n_results: int = 5):
    """Process user question and return response with context retrieval.
    
    Args:
        question: User's question
        deps: RAG dependencies
        n_results: Number of context results to retrieve
        
    Returns:
        Generator for streaming response
    """
    # Retrieve context
    context = retrieve(deps, question, n_results=n_results)
    
    # Generate and stream response
    async for text in generate_response_stream(question, context):
        yield text


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~ Main Function with UI Creation ~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

async def main():
    st.set_page_config(
        page_title="RAG Agent with Gemini",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 ChromaDB Crawl4AI RAG Agent with Gemini")
    st.caption("Powered by Google Gemini 2.0 Flash and Crawl4AI")

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        model_choice = st.selectbox(
            "Select Gemini Model",
            ["gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-pro"],
            index=0
        )
        
        n_results = st.slider(
            "Number of context documents",
            min_value=1,
            max_value=10,
            value=5,
            help="Number of relevant documents to retrieve from ChromaDB"
        )
        
        st.divider()
        
        st.markdown("### 📚 About")
        st.markdown("""
        This RAG (Retrieval-Augmented Generation) agent:
        - Retrieves relevant context from ChromaDB
        - Uses Google Gemini for intelligent responses
        - Powered by Crawl4AI for web scraping
        """)
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "agent_deps" not in st.session_state:
        st.session_state.agent_deps = get_agent_deps()
        st.session_state.model_choice = model_choice

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything about the documentation..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response with streaming
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # Process question and stream response
                async for chunk in process_question(
                    prompt, 
                    st.session_state.agent_deps,
                    n_results=n_results
                ):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                
                # Display final response without cursor
                message_placeholder.markdown(full_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
                
            except Exception as e:
                error_message = f"Error: {str(e)}"
                message_placeholder.error(error_message)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_message}
                )


if __name__ == "__main__":
    asyncio.run(main())
