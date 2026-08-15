import streamlit as st
from groq import Groq
import os
import json
import uuid
from datetime import datetime

# Page Configuration with Custom Layout
st.set_page_config(
    page_title="Nexus AI - Pro Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fetch API Key from Render Environment
API_KEY = os.environ.get("GROQ_API_KEY", "")

# Permanent Local File Storage
STORAGE_FILE = "chat_history.json"

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

# Initialize Session States
if "chats" not in st.session_state:
    st.session_state.chats = load_chats()

if "current_chat_id" not in st.session_state:
    if st.session_state.chats:
        st.session_state.current_chat_id = list(st.session_state.chats.keys())[-1]
    else:
        st.session_state.current_chat_id = None

# Function to Create New Chat Session
def create_new_chat():
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {
        "title": f"New Chat ({datetime.now().strftime('%H:%M')})",
        "messages": [
            {"role": "assistant", "content": "Welcome to Nexus AI Pro! How can I assist you today?"}
        ]
    }
    st.session_state.current_chat_id = chat_id
    save_chats(st.session_state.chats)

if not st.session_state.chats:
    create_new_chat()

# System Prompt Configuration
SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are Nexus AI Pro, an advanced AI system. Respond intelligently and naturally in the language used by the user (English, Hinglish, Hindi, etc.). Keep formatting clean and helpful."
}

# ----------------- SIDEBAR SETUP & CONTROL PANEL -----------------
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #4F46E5;'>⚡ Nexus AI Pro</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # New Chat Button
    if st.button("➕ New Chat Session", use_container_width=True, type="primary"):
        create_new_chat()
        st.rerun()

    st.markdown("### 🗂️ Conversation History")

    # List and Select Previous Chats
    chat_ids = list(st.session_state.chats.keys())
    for cid in reversed(chat_ids):
        chat = st.session_state.chats[cid]
        is_active = (cid == st.session_state.current_chat_id)
        button_label = f"💬 {chat['title']}" if not is_active else f"👉 {chat['title']}"
        
        col1, col2 = st.columns([0.85, 0.15])
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
    
    # Advanced Setup Controls
    with st.expander("⚙️ AI Response Setup", expanded=False):
        temperature = st.slider("Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
        max_tokens = st.slider("Max Response Length", min_value=256, max_value=4096, value=2048, step=256)

    st.markdown("---")
    # System Metrics / Status Widget
    st.markdown("#### 🌐 System Status")
    st.caption("• Core Engine: **Groq Llama-3.3-70B**")
    st.caption("• Status: 🟢 **Operational**")
    st.caption("• Latency: **Ultra-Low (<1s)**")

# ----------------- MAIN INTERFACE -----------------
current_id = st.session_state.current_chat_id
current_chat = st.session_state.chats[current_id]

# Top Control Bar & Header
col_title, col_edit, col_export = st.columns([0.5, 0.3, 0.2])

with col_title:
    st.subheader(f"📌 {current_chat['title']}")

with col_edit:
    new_name = st.text_input("Rename Session:", value=current_chat["title"], key=f"rename_{current_id}", label_visibility="collapsed")
    if new_name != current_chat["title"]:
        st.session_state.chats[current_id]["title"] = new_name
        save_chats(st.session_state.chats)
        st.rerun()

with col_export:
    # Export Chat to Text File
    chat_text = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in current_chat["messages"]])
    st.download_button(
        label="📥 Export Chat",
        data=chat_text,
        file_name=f"{current_chat['title'].replace(' ', '_')}.txt",
        mime="text/plain",
        use_container_width=True
    )

st.markdown("---")

# Display Messages
for msg in current_chat["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat Input & Processing
if prompt := st.chat_input("Ask Nexus AI anything..."):
    # Append User Message
    st.session_state.chats[current_id]["messages"].append({"role": "user", "content": prompt})
    
    # Auto Title Generator for New Chats
    if current_chat["title"].startswith("New Chat") and len(current_chat["messages"]) == 2:
        auto_title = prompt[:22] + "..." if len(prompt) > 22 else prompt
        st.session_state.chats[current_id]["title"] = auto_title

    save_chats(st.session_state.chats)

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        if not API_KEY:
            st.error("⚠️ API Key not found! Configure GROQ_API_KEY in Render Environment Variables.")
        else:
            try:
                client = Groq(api_key=API_KEY)
                
                formatted_contents = [SYSTEM_PROMPT]
                for msg in st.session_state.chats[current_id]["messages"]:
                    formatted_contents.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
                
                # API Call with Dynamic Setup Parameters
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=formatted_contents,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                reply = response.choices[0].message.content
                st.write(reply)
                
                # Save Assistant Response
                st.session_state.chats[current_id]["messages"].append({"role": "assistant", "content": reply})
                save_chats(st.session_state.chats)
            except Exception as e:
                st.error(f"Error: {e}")
