import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="Model Chat Interface",
    page_icon="💬",
    layout="wide"
)

st.title(" Model Chat Interface ")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for API configuration
with st.sidebar:
    st.header("API Configuration")
    api_url = st.text_input("API URL", placeholder="https://your-api-endpoint.com")
    api_key = st.text_input("API Key", placeholder="sk-xxxx", type="password")
    model_name = st.text_input("Model Name", value="inference-granite-33-8b")
    st.divider()
    st.caption("This application allows you to interact with your model through a simple chat interface.")

# Function to call the chat model API
def call_model_api(user_input):
    if not api_url or not api_key or not model_name:
        return "❗ Please provide API URL, API Key, and Model Name in the sidebar."

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    # Construct messages from chat history for context
    messages = st.session_state.messages + [{"role": "user", "content": user_input}]

    data = {
        "model": model_name,
        "messages": messages
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return f"❌ HTTP error {response.status_code}: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"❌ Request error: {str(e)}"

# Display chat history messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Enter your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get model response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = call_model_api(prompt)

            if isinstance(response, dict):
                try:
                    # Extract assistant response
                    response_content = response["choices"][0]["message"]["content"]
                    st.markdown(response_content)
                except (KeyError, IndexError):
                    response_content = "❗ Unexpected response format from API."
                    st.error(response_content)
            else:
                # If response is a string (error message)
                response_content = response
                st.error(response_content)

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_content})