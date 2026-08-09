import streamlit as st
from groq import Groq

# Page Config
st.set_page_config(page_title="AI Assistant", page_icon="⚡")

# Direct Groq API Key
API_KEY = "gsk_KAP9eRmZ5ke3dxYOnJHlWGdyb3FYiH7PL9ZHgy78t1BxgYdxSKc"

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    st.write("Status: 🟢 **Online**")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Header
st.title("⚡ AI Assistant")

# Initialize Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Haan ji bhai! Aapki kya madad karoon?"}
    ]

# Display Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat Input & Response Logic
if prompt := st.chat_input("Yahan message likhein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            client = Groq(api_key=API_KEY)
            
            # Format chat history for Groq
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
