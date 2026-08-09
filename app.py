import streamlit as st
from google import genai
import os

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="AI Assistant",
    page_icon="⚡",
    layout="centered"
)

# --- 2. CLEAN & MODERN LOOK (CSS) ---
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
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #8b949e;
        font-size: 0.9rem;
        margin-bottom: 25px;
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

# --- 3. SAFE API KEY CHECK ---
api_key = os.environ.get("GEMINI_API_KEY", "")

# --- 4. SIDEBAR SETTINGS ---
with st.sidebar:
    st.title("⚙️ Settings")
    if not api_key:
        api_key = st.text_input("Enter Gemini API Key:", type="password")
    else:
        st.success("🟢 API Connected")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat History", key="clear_chat_key"):
        st.session_state.messages = []
        st.rerun()

# --- 5. HEADER SECTION ---
st.markdown("<h1 class='main-title'>⚡ Ultra AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Fast, Smart & Always Ready</p>", unsafe_allow_html=True)

# --- 6. CHAT HISTORY INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Haan ji bhai! Main aapki kya madad kar sakta hoon?"}
    ]

# --- 7. DISPLAY CHAT MESSAGES ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- 8. CHAT INPUT & AI RESPONSE ---
if prompt := st.chat_input("Yahan message likhein..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # AI response
    with st.chat_message("assistant"):
        if not api_key:
            reply = "⚠️ Sidebar me apni **GEMINI_API_KEY** daalein taaki AI baat kar sake."
            st.warning(reply)
        else:
            try:
                client = genai.Client(api_key=api_key)
                
                # Build chat history for Gemini
                contents = []
                for msg in st.session_state.messages:
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append({
                        "role": role,
                        "parts": [{"text": msg["content"]}]
                    })

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=contents,
                )
                reply = response.text
                st.write(reply)
            except Exception as e:
                reply = f"Error: {str(e)}"
                st.error(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
