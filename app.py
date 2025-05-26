import streamlit as st
import requests

# Page setup
st.set_page_config(page_title="AI Model Interface", page_icon="🤖", layout="wide")
st.title("🤖 Universal AI Model Chat & Inference Interface")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "models" not in st.session_state:
    st.session_state.models = []
if "model_confirmed" not in st.session_state:
    st.session_state.model_confirmed = False
if "selected_model" not in st.session_state:
    st.session_state.selected_model = None
if "selected_model_type" not in st.session_state:
    st.session_state.selected_model_type = None

# Known model types (based on documentation)
model_type_map = {
    "inference-bge-m3": "embedding",
    "inference-bge-reranker": "reranker",
    "inference-deepseekr1-70b": "chat",
    "inference-granite-33-8b": "chat",
    "inference-granite-emb-30m": "embedding",
    "inference-granite-vision-2b": "multimodal",
    "inference-llama33-70b": "chat",
    "inference-llama4-maverick": "multimodal",
    "inference-qwq-32b": "chat",
    "inference-whisper-3lt": "speech"
}

# Sidebar for configuration
with st.sidebar:
    st.header("API Configuration")
    api_base = st.text_input("Base API URL", value="https://maas.ai-2.kvant.cloud")
    api_key = st.text_input("API Key", placeholder="sk-...", type="password")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)

    if api_base and api_key:
        models_url = api_base.rstrip("/") + "/v1/models"
        headers = {"Authorization": f"Bearer {api_key}"}
        try:
            response = requests.get(models_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            st.session_state.models = data.get("data", [])
        except Exception as e:
            st.error(f"Error fetching models: {e}")
    else:
        st.info("Enter API URL and Key to load models.")

    if st.session_state.models:
        model_ids = [m["id"] for m in st.session_state.models]
        selected_id = st.selectbox("Select a model", model_ids)
        if st.button("✅ Confirm Model Selection"):
            st.session_state.selected_model = selected_id
            st.session_state.selected_model_type = model_type_map.get(selected_id, "chat")
            st.session_state.model_confirmed = True
            st.success(f"Selected: **{selected_id}** ({st.session_state.selected_model_type})")

    st.caption("Supports chat, embeddings, multimodal, and more.")

# Function to call relevant API based on model type
def call_model_api(prompt):
    model = st.session_state.selected_model
    model_type = st.session_state.selected_model_type
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    if model_type == "embedding":
        endpoint = f"{api_base.rstrip('/')}/v1/embeddings"
        payload = {
            "model": model,
            "input": prompt
        }

    elif model_type == "chat":
        endpoint = f"{api_base.rstrip('/')}/v1/chat/completions"
        messages = st.session_state.messages + [{"role": "user", "content": prompt}]
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }

    elif model_type == "multimodal":
        endpoint = f"{api_base.rstrip('/')}/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        # You can add an image block here if needed
                        # {"type": "image_url", "image_url": {"url": "https://your-image-url"}}
                    ]
                }
            ],
            "temperature": temperature
        }

    else:
        return f"⚠️ Unsupported model type: {model_type}"

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        return f"❌ HTTP error {response.status_code}: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"❌ Request error: {str(e)}"

# Main chat or input interface
if st.session_state.model_confirmed:
    model_type = st.session_state.selected_model_type

    if model_type == "chat" or model_type == "multimodal":
        # Display history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Enter your message..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = call_model_api(prompt)
                    if isinstance(response, dict):
                        try:
                            content = response["choices"][0]["message"]["content"]
                            st.markdown(content)
                        except Exception:
                            content = "⚠️ Unexpected format."
                            st.error(content)
                    else:
                        content = response
                        st.error(content)

            st.session_state.messages.append({"role": "assistant", "content": content})

    elif model_type == "embedding":
        prompt = st.text_input("Text to embed:")
        if st.button("🔍 Embed"):
            with st.spinner("Embedding..."):
                response = call_model_api(prompt)
                if isinstance(response, dict):
                    st.json(response)
                else:
                    st.error(response)

    else:
        st.info(f"Model type `{model_type}` is not yet fully integrated.")
else:
    st.info("Please select and confirm a model to begin.")