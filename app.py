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
            import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# --- CLEAN & MODERN LOOK (CSS) ---
st.markdown("""
    <style>
    /* Background Color */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    /* Header Styling */
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #4F46E5, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #9CA3AF;
        font-size: 0.95rem;
        margin-bottom: 25px;
    }
    
    /* Chat Box Style */
    .stChatMessage {
        border-radius: 12px;
        padding: 8px 12px;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("<h1 class='main-title'>🤖 My AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Aapka apna personal intelligent assistant</p>", unsafe_allow_html=True)

# --- CHAT HISTORY INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Haan ji bhai! Kaise help karun aapki aaj?"}
    ]

# --- DISPLAY CHAT MESSAGES ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- CHAT INPUT ---
if prompt := st.chat_input("Yahan apna message likhein..."):
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # AI Reply (Basic Reply)
    reply = f"Aapne bola: '{prompt}'. Design kaisa lag raha hai app ka?"
    with st.chat_message("assistant"):
        st.write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Assistant",
    page_icon="⚡",
    layout="centered"
)

# --- MODERN STYLING (CSS) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
    
    /* Title Header */
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }
    .sub-title {
        text-align: center;
        color: #8b949e;
        font-size: 0.9rem;
        margin-bottom: 20px;
    }

    /* Welcome Card Buttons */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        background-color: #161b22;
        color: #c9d1d9;
        border: 1px solid #30363d;
        padding: 10px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        border-color: #58a6ff;
        color: #58a6ff;
        background-color: #1f242d;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROL ---
with st.sidebar:
    st.title("⚙️ Settings")
    st.write("Status: 🟢 **Online**")
    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- HEADER SECTION ---
st.markdown("<h1 class='main-title'>⚡ Ultra AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Fast, Smart & Always Ready</p>", unsafe_allow_html=True)

# --- CHAT HISTORY INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Haan ji bhai! Main aapki kya madad kar sakta hoon?"}
    ]

# --- QUICK SUGGESTIONS (If history is short) ---
if len(st.session_state.messages) <= 1:
    st.write("**Quick Suggestions:**")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💡 Creative Business Ideas"):
            st.session_state.prompt_input = "Mujhe 3 unique business ideas batao."
    with col2:
        if st.button("📝 Professional Email Writer"):
            st.session_state.prompt_input = "Ek professional leave application email likho."

# --- DISPLAY CHAT MESSAGES ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- HANDLE QUICK SUGGESTION CLICK ---
user_input = ""
if "prompt_input" in st.session_state and st.session_state.prompt_input:
    user_input = st.session_state.prompt_input
    st.session_state.prompt_input = ""  # Reset after use

# --- CHAT INPUT ---
if prompt := (st.chat_input("Yahan message likhein...") or user_input):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # AI Reply (Temporary placeholder reply)
    reply = f"Aapne poocha: **'{prompt}'**. Abhi design upgrade ho raha hai, jald hi isme real-time AI response link karenge!"
    
    with st.chat_message("assistant"):
        st.write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
