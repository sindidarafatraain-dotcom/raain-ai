
import streamlit as st
import requests
import uuid
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Raain AI | Premium Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-oss-20b"

# ---------------- THEMES ----------------
THEMES = {
    "Obsidian Gold": {
        "bg": "#08090D",
        "panel": "#11131A",
        "accent": "#D6B36A",
        "text": "#F4F0E8",
        "muted": "#9A9BA5",
        "border": "#2B2B32"
    },
    "Midnight Sapphire": {
        "bg": "#080D18",
        "panel": "#101A2B",
        "accent": "#78A9FF",
        "text": "#F0F5FF",
        "muted": "#A0AEC4",
        "border": "#24344E"
    },
    "Emerald Elite": {
        "bg": "#07100D",
        "panel": "#101C17",
        "accent": "#72D6A0",
        "text": "#F0FFF6",
        "muted": "#9AB7A7",
        "border": "#244535"
    },
    "Champagne Noir": {
        "bg": "#100D0B",
        "panel": "#1B1511",
        "accent": "#E4C9A1",
        "text": "#FFF7EC",
        "muted": "#B6A99A",
        "border": "#3A2C21"
    }
}

# ---------------- SESSION STATE ----------------
if "chats" not in st.session_state:
    first_id = str(uuid.uuid4())
    st.session_state.chats = {
        first_id: {
            "title": "নতুন চ্যাট",
            "messages": []
        }
    }
    st.session_state.active_chat = first_id

if "active_chat" not in st.session_state:
    st.session_state.active_chat = next(iter(st.session_state.chats))

if st.session_state.active_chat not in st.session_state.chats:
    st.session_state.active_chat = next(iter(st.session_state.chats))

# ---------------- HELPERS ----------------
def new_chat():
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {
        "title": "নতুন চ্যাট",
        "messages": []
    }
    st.session_state.active_chat = chat_id

def open_chat(chat_id):
    st.session_state.active_chat = chat_id

def delete_current_chat():
    chats = st.session_state.chats
    current = st.session_state.active_chat

    if current in chats:
        del chats[current]

    if not chats:
        new_chat()
    else:
        st.session_state.active_chat = next(iter(chats))

def make_system_prompt(style, language, personality):
    style_instructions = {
        "Balanced": "Give clear, useful answers with a moderate amount of detail.",
        "Detailed": "Explain thoroughly with steps, examples, and practical advice.",
        "Short": "Answer briefly and directly without unnecessary details.",
        "Tutor": "Teach step by step for a beginner. Explain difficult terms simply and give examples."
    }

    language_instructions = {
        "Auto": "Reply in the same language as the user's latest message.",
        "বাংলা": "Always reply in simple, natural Bangla unless the user asks for another language.",
        "English": "Reply in clear, natural English."
    }

    personalities = {
        "Friendly": "Be friendly, respectful, warm, and easy to understand.",
        "Professional": "Be polished, professional, structured, and precise.",
        "Creative": "Be creative, thoughtful, and offer useful alternatives when appropriate."
    }

    return (
        "You are Raain AI, a helpful personal AI assistant. "
        "Be truthful. Never invent facts, sources, or capabilities. "
        "If you are uncertain, say so. "
        + style_instructions[style] + " "
        + language_instructions[language] + " "
        + personalities[personality]
    )

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding:12px 0 20px 0;">
            <div style="font-size:42px;">✦</div>
            <h2 style="margin:0; letter-spacing:2px;">RAAIN AI</h2>
            <p style="color:#A0A0AA; font-size:12px; letter-spacing:3px;">
                YOUR PERSONAL INTELLIGENCE
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("＋  নতুন চ্যাট", use_container_width=True):
        new_chat()
        st.rerun()

    st.markdown("### 💬 Chat History")

    # Show recent chats first
    for chat_id, chat in reversed(list(st.session_state.chats.items())):
        label = chat["title"][:27]
        if chat_id == st.session_state.active_chat:
            label = "● " + label

        if st.button(
            label,
            key=f"chat_{chat_id}",
            use_container_width=True
        ):
            open_chat(chat_id)
            st.rerun()

    st.divider()
    st.markdown("### ⚙️ Personalize")

    theme_name = st.selectbox(
        "Luxury Theme",
        list(THEMES.keys()),
        index=0
    )

    response_style = st.selectbox(
        "Answer Style",
        ["Balanced", "Detailed", "Short", "Tutor"],
        index=0
    )

    response_language = st.selectbox(
        "Response Language",
        ["Auto", "বাংলা", "English"],
        index=0
    )

    personality = st.selectbox(
        "AI Personality",
        ["Friendly", "Professional", "Creative"],
        index=0
    )

    st.divider()

    st.caption("Powered by Groq API")
    st.caption("Raain AI • Premium Edition")

# ---------------- APPLY THEME ----------------
theme = THEMES[theme_name]

st.markdown(
    f"""
    <style>
    :root {{
        color-scheme: dark;
    }}

    .stApp {{
        background:
            radial-gradient(ellipse at 15% 0%, {theme["panel"]} 0%, transparent 42%),
            {theme["bg"]};
        color: {theme["text"]};
    }}

    [data-testid="stSidebar"] {{
        background: {theme["panel"]};
        border-right: 1px solid {theme["border"]};
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    h1, h2, h3 {{
        color: {theme["text"]} !important;
    }}

    p, label, .stMarkdown {{
        color: {theme["text"]};
    }}

    .stCaption, small {{
        color: {theme["muted"]} !important;
    }}

    div[data-testid="stChatMessage"] {{
        background: {theme["panel"]};
        border: 1px solid {theme["border"]};
        border-radius: 18px;
        padding: 16px;
        margin-bottom: 12px;
    }}

    div[data-testid="stChatInput"] {{
        border: 1px solid {theme["accent"]} !important;
        border-radius: 18px !important;
    }}

    div[data-testid="stChatInput"] textarea {{
        color: {theme["text"]} !important;
    }}

    .stButton > button {{
        border: 1px solid {theme["border"]};
        border-radius: 12px;
        transition: all 0.2s ease;
    }}

    .stButton > button:hover {{
        border-color: {theme["accent"]};
        color: {theme["accent"]};
    }}

    div[data-testid="stAlert"] {{
        border-radius: 12px;
    }}

    .raain-hero {{
        padding: 26px 24px;
        border: 1px solid {theme["border"]};
        border-radius: 22px;
        background: linear-gradient(
            135deg,
            {theme["panel"]},
            {theme["bg"]}
        );
        margin-bottom: 22px;
    }}

    .raain-kicker {{
        color: {theme["accent"]};
        font-size: 11px;
        letter-spacing: 4px;
        font-weight: 700;
    }}

    .raain-subtitle {{
        color: {theme["muted"]};
        font-size: 14px;
    }}

    #MainMenu, footer {{
        visibility: hidden;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- MAIN HEADER ----------------
st.markdown(
    f"""
    <div class="raain-hero">
        <div class="raain-kicker">PERSONAL AI • PREMIUM EDITION</div>
        <h1 style="font-size:36px; margin:10px 0;">
            ✦ Raain AI
        </h1>
        <div class="raain-subtitle">
            Think clearly. Create freely. Achieve more.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

current_chat = st.session_state.chats[st.session_state.active_chat]
messages = current_chat["messages"]

left, right = st.columns([5, 1])

with left:
    st.caption(
        f"Theme: {theme_name}  ·  Style: {response_style}  ·  Model: {DEFAULT_MODEL}"
    )

with right:
    if messages:
        chat_text = "\n\n".join(
            f'{m["role"].upper()}:\n{m["content"]}'
            for m in messages
        )
        st.download_button(
            "⬇ Export",
            data=chat_text,
            file_name="raain_ai_chat.txt",
            mime="text/plain",
            use_container_width=True
        )

# ---------------- DISPLAY CHAT ----------------
if not messages:
    st.markdown(
        f"""
        <div style="
            border:1px solid {theme["border"]};
            background:{theme["panel"]};
            padding:22px;
            border-radius:18px;
            margin-bottom:20px;
        ">
            <h3 style="margin-top:0;">Welcome to Raain AI ✨</h3>
            <p style="color:{theme["muted"]};">
                তোমার প্রশ্ন, পড়াশোনা, coding, writing অথবা নতুন আইডিয়া নিয়ে
                কথা শুরু করো।
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 আমাকে পড়াশোনায় সাহায্য করো", use_container_width=True):
            st.session_state.suggested_prompt = (
                "আমাকে একজন beginner-friendly tutor-এর মতো ধাপে ধাপে পড়াশোনায় সাহায্য করো।"
            )
    with col2:
        if st.button("💻 একটি Python project শেখাও", use_container_width=True):
            st.session_state.suggested_prompt = (
                "আমাকে beginner হিসেবে একটি ছোট Python project ধাপে ধাপে শেখাও।"
            )

for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- USER INPUT ----------------
suggested = st.session_state.pop("suggested_prompt", None)
prompt = st.chat_input("Raain AI-কে কিছু জিজ্ঞেস করো...")

if suggested and not prompt:
    prompt = suggested

if prompt:
    messages.append({"role": "user", "content": prompt})

    if current_chat["title"] == "নতুন চ্যাট":
        current_chat["title"] = prompt.strip().replace("\n", " ")[:30]
        if len(prompt.strip()) > 30:
            current_chat["title"] += "…"

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            api_key = st.secrets["GROQ_API_KEY"]

            system_prompt = make_system_prompt(
                response_style,
                response_language,
                personality
            )

            api_messages = [
                {"role": "system", "content": system_prompt}
            ] + messages

            with st.spinner("Raain AI ভাবছে..."):
                response = requests.post(
                    API_URL,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": DEFAULT_MODEL,
                        "messages": api_messages,
                        "max_tokens": 1600,
                        "temperature": 0.7
                    },
                    timeout=90
                )

            if response.status_code == 429:
                st.warning(
                    "Groq API-এর rate limit পূর্ণ হয়েছে। "
                    "কিছুক্ষণ পরে আবার চেষ্টা করো।"
                )
                messages.pop()

            else:
                response.raise_for_status()
                answer = response.json()["choices"][0]["message"]["content"]

                st.markdown(answer)
                messages.append({
                    "role": "assistant",
                    "content": answer
                })

        except KeyError:
            st.error(
                "GROQ_API_KEY পাওয়া যায়নি। "
                "Streamlit Cloud → App Settings → Secrets পরীক্ষা করো।"
            )
            messages.pop()

        except requests.exceptions.Timeout:
            st.error("AI উত্তর দিতে বেশি সময় নিচ্ছে। আবার চেষ্টা করো।")
            messages.pop()

        except requests.exceptions.HTTPError as error:
            st.error(
                f"Groq API error: {error}. "
                "API key, model এবং API usage পরীক্ষা করো।"
            )
            messages.pop()

        except requests.exceptions.RequestException:
            st.error("সার্ভারে যোগাযোগ করা যায়নি। ইন্টারনেট পরীক্ষা করো।")
            messages.pop()

        except (ValueError, KeyError, IndexError, TypeError):
            st.error("AI-এর উত্তর পড়তে সমস্যা হয়েছে। আবার চেষ্টা করো।")
            messages.pop()

# ---------------- CHAT MANAGEMENT ----------------
st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("＋ New Chat", use_container_width=True):
        new_chat()
        st.rerun()

with col2:
    if st.button("🗑 Delete Current Chat", use_container_width=True):
        delete_current_chat()
        st.rerun()
