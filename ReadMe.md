# 🤖 Model Chat Interface

A minimal Streamlit-based chatbot interface to connect to your own LLM API (OpenAI-compatible). Easily run it locally in your terminal using Python or Podman.

---

## 🚀 Features

- Simple chat interface with message history
- Sidebar configuration for API URL, Key, and Model
- Connect to any OpenAI-compatible API
- Lightweight and easy to run in terminal

---

## 🧑‍💻 Run with Python

### ✅ Prerequisites

- Python 3.10+
- `pip` (Python package manager)

### 🔧 Setup and Run

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/chatbot.git
cd chatbot
```

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Streamlit app
streamlit run app.py
Open your browser at:
👉 http://localhost:8501

🐳 Run with Podman (or Docker)
✅ Prerequisites
Podman or Docker installed
🔧 Build and Run
bash

Copy
# 1. Build the image
podman build -t streamlit-chatbot .

# 2. Run the container
podman run -p 8501:8501 streamlit-chatbot
Then open:
👉 http://localhost:8501

⚙️ API Setup
Use the sidebar in the app to enter:

API URL (e.g. https://api.myendpoint.com/v1/chat/completions)
API Key (e.g. sk-xxxx)
Model Name (e.g. gpt-3.5-turbo, inference-granite-33-8b)