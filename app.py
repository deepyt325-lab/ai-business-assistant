import streamlit as st
from groq import Groq
import os
import json
import uuid
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Nexus AI", page_icon="⚡", layout="wide")

# Fetch API Key from Render Environment
API_KEY = os.environ.get("GROQ_API_KEY", "")

# File path for storing permanent chats
STORAGE_FILE = "chat_history.json"

# Helper functions to load and save chat history to local JSON file
def load_chats():
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_chats(chats):
    with open(STORAGE_FILE, "w") as f:
        json.dump(chats, f, indent=4)

# Initialize Main Storage
if "chats" not in st.session_state:
    st.session_state.chats = load_chats()

if "current_chat_id" not in st.session_state:
    if st.session_state.chats:
        st.session_state.current_chat_id = list(st.session_state.chats.keys())[-1]
    else:
        st.session_state.current_chat_id = None

# System Prompt for Flexible Multi-Language Response
SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are Nexus AI, a highly capable assistant. Respond naturally in whichever language or script the user writes in (Hinglish, Hindi, English, etc.). Be helpful, smart, and direct."
}

# Function to Create a New Chat Session
def create_new_chat():
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {
        "title": f"New Chat ({datetime.now().strftime('%H:%M')})",
        "messages": [
            {"role": "assistant", "content": "Hello! How can I help you today?"}
        ]
    }
    st.session_state.current_chat_id = chat_id
    save_chats(st.session_state.chats)

# Create initial chat if none exists
if not st.session_state.chats:
    create_new_chat()

# Sidebar Setup
with st.sidebar:
    st.title("⚡ Nexus AI")
    
    # New Chat Button
    if st.button("➕ New Chat", use_container_width=True):
        create_new_chat()
        st.rerun()

    st.markdown("---")
    st.subheader("🗂️ Chat History")

    # List and Select Previous Chats
    chat_ids = list(st.session_state.chats.keys())
    for cid in reversed(chat_ids):
        chat = st.session_state.chats[cid]
        
        # Highlight active chat
        is_active = (cid == st.session_state.current_chat_id)
        button_label = f"💬 {chat['title']}" if not is_active else f"👉 {chat['title']}"
        
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            if st.button(button_label, key=f"select_{cid}", use_container_width=True):
                st.session_state.current_chat_id = cid
                st.rerun()
        with col2:
            if st.button("🗑️", key=f"del_{cid}"):
                del st.session_state.chats[cid]
                save_chats(st.session_state.chats)
                if st.session_state.current_chat_id == cid:
                    remaining_ids = list(st.session_state.chats.keys())
                    if remaining_ids:
                        st.session_state.current_chat_id = remaining_ids[-1]
                    else:
                        create_new_chat()
                st.rerun()

    st.markdown("---")
    st.caption("Powered by Groq Llama-3.3")

# Get Current Chat Data
current_id = st.session_state.current_chat_id
current_chat = st.session_state.chats[current_id]

# Chat Title & Editing Header
col_title, col_edit = st.columns([0.7, 0.3])
with col_title:
    st.title(current_chat["title"])

with col_edit:
    new_name = st.text_input("Rename Chat:", value=current_chat["title"], key=f"rename_{current_id}")
    if new_name != current_chat["title"]:
        st.session_state.chats[current_id]["title"] = new_name
        save_chats(st.session_state.chats)
        st.rerun()

# Display Current Conversation Messages
for msg in current_chat["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat Input & AI Response Generation
if prompt := st.chat_input("Type a message..."):
    # Append User Message to Active Chat History
    st.session_state.chats[current_id]["messages"].append({"role": "user", "content": prompt})
    
    # Auto-rename "New Chat" on first query
    if current_chat["title"].startswith("New Chat") and len(current_chat["messages"]) == 2:
        auto_title = prompt[:25] + "..." if len(prompt) > 25 else prompt
        st.session_state.chats[current_id]["title"] = auto_title

    save_chats(st.session_state.chats)

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        if not API_KEY:
            st.error("⚠️ API Key not found! Set GROQ_API_KEY in Render Environment Variables.")
        else:
            try:
                client = Groq(api_key=API_KEY)
                
                # Format full context memory including system prompt for Groq API
                formatted_contents = [SYSTEM_PROMPT]
                for msg in st.session_state.chats[current_id]["messages"]:
                    formatted_contents.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
                
                # API Call with full chat context
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=formatted_contents,
                )
                
                reply = response.choices[0].message.content
                st.write(reply)
                
                # Save Assistant Response to Active Chat History
                st.session_state.chats[current_id]["messages"].append({"role": "assistant", "content": reply})
                save_chats(st.session_state.chats)
            except Exception as e:
                st.error(f"Error: {e}")
