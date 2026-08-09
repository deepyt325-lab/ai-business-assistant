import streamlit as st
from google import genai
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Ultra AI Assistant",
    page_icon="⚡",
    layout="centered"
)

# --- MODERN STYLING (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-title {
        text-align: center;
        color: #8b949e;
        font-size: 0.9rem;
        margin-bottom: 20px;
    }
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        background-color: #161b22;
        color: #c9d1d9;
        border: 1px solid #30363d;
    }
    </style>
""", unsafe_allow_html=True)

# --- GEMINI CLIENT SETUP ---
api_key = os.environ.get("GEMINI_API_KEY", "")

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Settings")
    if api_key:
        st.write("Status: 🟢 **AI Connected**")
    else:
        st.write("Status: 🔴 **API Key Missing**")
        api_key = st.text_input("Enter Gemini API Key:", type="password")

    st.markdown("---")
    if st.button("🗑️ Clear Chat History", key="clear_chat_key"):
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

# --- QUICK SUGGESTIONS ---
if len(st.session_state.messages) <= 1:
    st.write("**Quick Suggestions:**")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💡 Creative Ideas", key="btn_ideas_key"):
            st.session_state.prompt_input = "Mujhe 3 unique business ideas batao."
    with col2:
        if st.button("📝 Email Writer", key="btn_email_key"):
            st.session_state.prompt_input = "Ek professional leave application email likho."

# --- DISPLAY CHAT MESSAGES ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- HANDLE QUICK SUGGESTION CLICK ---
user_input = ""
if "prompt_input" in st.session_state and st.session_state.prompt_input:
    user_input = st.session_state.prompt_input
    st.session_state.prompt_input = ""

# --- CHAT INPUT & AI GENERATION ---
if prompt := (st.chat_input("Yahan message likhein...") or user_input):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        if not api_key:
            reply = "⚠️ Please sidebar me apni **GEMINI_API_KEY** daalein taaki AI jawaab de sake!"
            st.warning(reply)
        else:
            try:
                client = genai.Client(api_key=api_key)
                
                # Convert session history to Gemini chat format
                formatted_contents = []
                for msg in st.session_state.messages:
                    role = "user" if msg["role"] == "user" else "model"
                    formatted_contents.append({
                        "role": role,
                        "parts": [{"text": msg["content"]}]
                    })
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=formatted_contents,
                )
                reply = response.text
                st.write(reply)
            except Exception as e:
                reply = f"Error: {str(e)}"
                st.error(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
