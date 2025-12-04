# Deployment Guide for Streamlit Cloud

This app is ready to deploy on Streamlit Cloud!

## Quick Deploy Steps

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io/
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app"
   - Select repository: `Dishant707/AI-Chat-Bot`
   - Branch: `main`
   - Main file path: `chatbot_with_url_scraping.py`

3. **Add Secrets (API Key)**
   - Click "Advanced settings"
   - In "Secrets" section, add:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```

4. **Deploy!**
   - Click "Deploy"
   - Wait 2-3 minutes for deployment

## Alternative: Deploy Other Apps

If you want to deploy a different app:
- **Simple Chat**: Use `streamlit_demo.py`
- **Context Chat**: Use `chatbot_with_context.py` (requires pre-scraped data)

## Troubleshooting

- **API Key Error**: Make sure you added `GEMINI_API_KEY` in Secrets
- **Import Errors**: Check that all packages are in `requirements.txt`
- **Slow Loading**: First deployment takes longer, subsequent updates are faster

## Your Deployed URL

After deployment, you'll get a URL like:
`https://dishant707-ai-chat-bot.streamlit.app`

Share this URL with anyone to use your chatbot! 🚀
