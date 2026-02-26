import streamlit as st
import requests

# API URL
API_URL = "http://localhost:8000"

# Page config
st.set_page_config(
    page_title="Local LLM Chat",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Local LLM Chat")
st.caption("Powered by TinyLlama GGUF model")
mode = st.radio("Select Mode", ["Chat", "Generate"], horizontal=True)
st.divider()

st.sidebar.title("⚙️ Settings")


system_prompt = st.sidebar.text_area(
    "System Prompt",
    value="You are a helpful assistant.",
    height=100
)

temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
top_k = st.sidebar.slider("Top-K", 1, 100, 40)
top_p = st.sidebar.slider("Top-P", 0.0, 1.0, 0.95)
max_tokens = st.sidebar.slider("Max Tokens", 50, 512, 200)

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

if mode == "Generate":
    st.subheader("Generate Mode")

    prompt = st.text_area("Enter your prompt:", height=150)

    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating..."):
                try:
                    response = requests.post(
                        f"{API_URL}/generate",
                        json={
                            "prompt": prompt,
                            "max_tokens": max_tokens,
                            "temperature": temperature,
                            "top_k": top_k,
                            "top_p": top_p
                        }
                    )
                    result = response.json()
                    st.subheader("Response:")
                    st.write(result["response"])
                    st.caption(f"Request ID: {result['request_id']}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a prompt!")


elif mode == "Chat":
    st.subheader("Chat Mode")
    st.caption("Multi-turn conversation with history.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.write(user_input)

        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "messages": st.session_state.messages,
                        "system_prompt": system_prompt,
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "top_k": top_k,
                        "top_p": top_p
                    }
                )
                result = response.json()
                assistant_response = result["response"]

            except Exception as e:
                assistant_response = f"Error: {str(e)}"

        # Only add to history if real response
        if "I'm sorry! I can only answer coding" not in assistant_response:
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_response
            })

        with st.chat_message("assistant"):
            st.write(assistant_response)