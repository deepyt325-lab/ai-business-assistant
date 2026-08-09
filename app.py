import os
import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

# Sidebar Configuration
with st.sidebar:
    st.title("⚙️ Settings")
    system_prompt = st.text_area(
        "System Prompt (AI ka Nature):",
        value="You are a helpful and witty AI assistant who responds naturally."
    )
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 My AI Assistant")

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY Secret me nahi mili! Advanced Settings me Key add karo.")
    st.stop()

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Poocho jo poochna hai..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Build payload with system prompt + chat history
            api_messages = [{"role": "system", "content": system_prompt}] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            # Streaming API call for live typing effect
            stream = client.chat.completions.create(
                messages=api_messages,
                model="llama-3.3-70b-versatile",
                stream=True,
            )

            def generate_responses():
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content

            full_response = st.write_stream(generate_responses())
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Error: {e}")
