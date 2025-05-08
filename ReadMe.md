
### 🔧 Setup and Run

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/chatbot.git
cd chatbot
```
#  Build the image
```bash

podman build -t streamlit-chatbot .
```

# 2. Run the container

```bash
podman run -p 8501:8501 streamlit-chatbot
```

Then open:
👉 http://localhost:8501

⚙️ API Setup
Use the sidebar in the app to enter:

API URL (e.g. https://api.myendpoint.com/v1/chat/completions)
API Key (e.g. sk-xxxx)
Model Name (e.g. gpt-3.5-turbo, inference-granite-33-8b)