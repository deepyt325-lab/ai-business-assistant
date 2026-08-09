import streamlit as st
from groq import Groq
import os

# Page Config
st.set_page_config(page_title="AI Assistant", page_icon="⚡")

# Key Render Environment se auto-fetch hogi
API_KEY = os.environ.get("GROQ_API_KEY", "")

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    st.write("Status: 🟢 **Online**")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Header
st.title("⚡ AI Assistant")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Haan ji bhai! Aapki kya madad karoon?"}
    ]

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat Input & AI Logic
if prompt := st.chat_input("Yahan message likhein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        if not API_KEY:
            st.error("⚠️ API Key nahi mili! Render Dashboard mein GROQ_API_KEY set karein.")
        else:
            try:
                client = Groq(api_key=API_KEY)
                
                formatted_contents = []
                for msg in st.session_state.messages:
                    formatted_contents.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=formatted_contents,
                )
                
                reply = response.choices[0].message.content
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")
