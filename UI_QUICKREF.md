# UI Quick Reference Card

## 🎨 Building the UI - Super Quick Guide

### ⚡ 3 Steps to Launch

```bash
# Step 1: Setup (one-time)
./setup.sh

# Step 2: Get API Key & Configure
# Visit: https://aistudio.google.com/app/apikey
# Add to .env: GEMINI_API_KEY=your_key

# Step 3: Launch UI
streamlit run streamlit_app.py
```

**Done! Opens at http://localhost:8501** ✨

---

## 🎯 UI File Structure

```
streamlit_app.py          ← Main UI file (edit this!)
├── Imports & Setup
├── get_agent_deps()      ← Connects to ChromaDB
├── generate_response()   ← Calls Gemini
└── main()                ← UI layout

UI_GUIDE.md              ← Full customization guide
launch_ui.py             ← Quick launcher script
.streamlit/config.toml   ← Theme settings (create this)
```

---

## 🛠️ Common Customizations

### 1. Change Title (Line ~80)
```python
st.title("🤖 Your Custom Title Here")
```

### 2. Add More Models (Line ~95)
```python
model_choice = st.selectbox(
    "Select Model",
    ["gemini-2.0-flash-exp", "gemini-1.5-pro", "gemini-1.5-flash-8b"]
)
```

### 3. Change Colors
Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#0E1117"
```

### 4. Add Button in Sidebar (Line ~110)
```python
if st.button("🎯 My Button"):
    # Your code here
    st.success("Button clicked!")
```

---

## 🎨 UI Components Available

### Input Widgets
```python
st.text_input("Label")           # Text box
st.slider("Label", 0, 10)        # Slider
st.selectbox("Label", options)   # Dropdown
st.checkbox("Label")             # Checkbox
st.button("Label")               # Button
st.file_uploader("Label")        # File upload
```

### Display Widgets
```python
st.write("Text")                 # Any content
st.markdown("**Bold**")          # Markdown
st.success("Success!")           # Green box
st.error("Error!")               # Red box
st.info("Info")                  # Blue box
st.warning("Warning")            # Yellow box
st.metric("Label", value)        # Metric card
```

### Layout
```python
st.sidebar                       # Sidebar
st.columns(2)                    # Columns
st.expander("Label")             # Collapsible
st.tabs(["Tab1", "Tab2"])        # Tabs
st.container()                   # Container
```

---

## 🚀 Launch Commands

```bash
# Basic launch
streamlit run streamlit_app.py

# Custom port
streamlit run streamlit_app.py --server.port 8502

# Light theme
streamlit run streamlit_app.py --theme.base light

# Auto-reload on changes
streamlit run streamlit_app.py --server.runOnSave true

# No browser auto-open
streamlit run streamlit_app.py --server.headless true

# Use launch script
python launch_ui.py
```

---

## 📝 UI State Management

```python
# Initialize state (runs once)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Update state
st.session_state.messages.append(new_message)

# Read state
for msg in st.session_state.messages:
    st.write(msg)

# Clear state
if st.button("Clear"):
    st.session_state.messages = []
    st.rerun()  # Refresh UI
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| UI won't start | `pip install streamlit` |
| API errors | Check `.env` has `GEMINI_API_KEY` |
| No documents found | Run `python insert_docs.py <URL>` first |
| Port in use | Use different port: `--server.port 8502` |
| UI not updating | Clear cache: `streamlit cache clear` |
| Import errors | `pip install -r requirements.txt` |

---

## 🎯 Example Modifications

### Add Export Button
```python
# In sidebar (around line 120)
if st.button("💾 Export Chat"):
    chat_text = "\n\n".join([
        f"{m['role']}: {m['content']}"
        for m in st.session_state.messages
    ])
    st.download_button(
        "Download",
        chat_text,
        "chat.txt"
    )
```

### Add Statistics
```python
# In sidebar (around line 110)
st.metric(
    "Total Messages",
    len(st.session_state.messages)
)
```

### Add File Upload
```python
# In sidebar (around line 100)
uploaded = st.file_uploader("Upload File", type=['txt', 'md'])
if uploaded:
    content = uploaded.read().decode()
    st.success(f"Loaded: {uploaded.name}")
```

---

## 📱 UI Features Checklist

Current Features:
- ✅ Chat interface
- ✅ Streaming responses  
- ✅ Model selection
- ✅ Context slider
- ✅ Clear chat button
- ✅ Chat history

Add These (See UI_GUIDE.md):
- ⬜ Export chat
- ⬜ Show sources
- ⬜ Upload documents
- ⬜ Suggested questions
- ⬜ Search statistics
- ⬜ Custom themes

---

## 🎨 Theme Examples

### Dark Purple
```toml
[theme]
primaryColor = "#9D4EDD"
backgroundColor = "#10002B"
secondaryBackgroundColor = "#240046"
textColor = "#E0AAFF"
```

### Light Blue
```toml
[theme]
primaryColor = "#1E88E5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
textColor = "#212121"
```

### Hacker Green
```toml
[theme]
primaryColor = "#00FF00"
backgroundColor = "#000000"
secondaryBackgroundColor = "#0A0A0A"
textColor = "#00FF00"
```

Save as `.streamlit/config.toml` in your project!

---

## 🔗 Quick Links

- **Main UI File:** `streamlit_app.py`
- **Full Guide:** `UI_GUIDE.md`
- **Launcher:** `python launch_ui.py`
- **Docs:** https://docs.streamlit.io/

---

## 💡 Pro Tips

1. **Live Reload:** Save file → UI auto-updates
2. **Debug Mode:** Add `st.write(variable)` anywhere
3. **Clear Cache:** Settings → Clear Cache (in running UI)
4. **Mobile:** UI is responsive by default
5. **Share:** Deploy to Streamlit Cloud (free!)

---

**Your UI is ready! Just run: `streamlit run streamlit_app.py`** 🚀

For detailed customization, see `UI_GUIDE.md`!
