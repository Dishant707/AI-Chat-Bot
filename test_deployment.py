"""Simple Streamlit test to check deployment"""

import streamlit as st
import os

st.title("🔍 Deployment Diagnostics")

st.write("## Environment Check")

# Check for API key
api_key_env = os.getenv("GEMINI_API_KEY")
api_key_secrets = None

try:
    api_key_secrets = st.secrets.get("GEMINI_API_KEY")
except Exception as e:
    st.error(f"Secrets error: {str(e)}")

st.write("### API Key Status:")
if api_key_env:
    st.success(f"✅ Found in environment variables: {api_key_env[:20]}...")
else:
    st.warning("❌ Not found in environment variables")

if api_key_secrets:
    st.success(f"✅ Found in Streamlit secrets: {api_key_secrets[:20]}...")
else:
    st.error("❌ Not found in Streamlit secrets")

st.write("### Python Info:")
import sys
st.code(f"Python version: {sys.version}")

st.write("### Installed Packages:")
try:
    import google.generativeai
    st.success("✅ google-generativeai installed")
except ImportError:
    st.error("❌ google-generativeai NOT installed")

try:
    import requests
    st.success("✅ requests installed")
except ImportError:
    st.error("❌ requests NOT installed")

try:
    from bs4 import BeautifulSoup
    st.success("✅ beautifulsoup4 installed")
except ImportError:
    st.error("❌ beautifulsoup4 NOT installed")

st.write("---")
st.write("If you see errors above, check your Streamlit Cloud settings!")
