
import streamlit as st
import requests
import uuid

# ============== PAGE CONFIG ==============
st.set_page_config(
    page_title="Raain AI | Premium Assistant",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"

# ============== LUXURY THEMES ==============
THEMES = {
    "Obsidian Luxury": {
        "bg": "#08080D",
        "sidebar": "rgba(15,13,25,0.96)",
        "accent": "#B49AFF",
        "glow": "139,92,246",
        "text": "#F5F3FF",
        "border": "167,139,250",
        "muted": "#A7A1BB"
    },
    "Midnight Sapphire": {
        "bg": "#07111F",
        "sidebar": "rgba(8,20,38,0.96)",
        "accent": "#69B7FF",
        "glow": "37,99,235",
        "text": "#EFF6FF",
        "border": "96,165,250",
        "muted": "#9BAFC8"
    },
    "Emerald Elite": {
        "bg": "#07110D",
        "sidebar": "rgba(8,22,16,0.97)",
        "accent": "#4BE3B0",
        "glow": "5,150,105",
        "text": "#ECFDF5",
        "border": "52,211,153",
        "muted": "#9CB9AA"
    },
    "Champagne Gold": {
        "bg": "#17130F",
        "sidebar": "rgba(29,24,18,0.97)",
        "accent": "#E8CA91",
        "glow": "180,130,55",
        "text": "#FFF8EB",
        "border": "229,197,139",
        "muted": "#C4B9A5"
    }
}

# ============== SESSION STATE ==============
if "theme_name" not in st.session_state:
    st.session_state.theme_name = "Obsidian Luxury"

if "chats" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.chats = [{
        "id": chat_id,
        "title": "New Chat",
        "messages": []
    }]
    st.session_state.active_chat = chat_id


def active_chat():
    for chat in st.session_state.chats:
        if chat["id"] == st.session_state.active_chat:
            return chat
    return st.session_state.chats[0]


# ============== SIDEBAR / THEME ==============
with st.sidebar:
    st.markdown(
        '<div class="brand">✦ Raain <span>AI</span></div>',
        unsafe_allow_html=True
    )

    st.markdown("##### PERSONALIZE")

    chosen_theme = st.selectbox(
        "Luxury Theme",
        list(THEMES.keys()),
        index=list(THEMES.keys()).index(
            st.session_state.theme_name
        )
    )

    if chosen_theme != st.session_state.theme_name:
        st.session_state.theme_name = chosen_theme
        st.rerun()

theme = THEMES[st.session_state.theme_name]

# ============== LUXURY GLASS CSS ==============
st.markdown(f"""
<style>
@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

:root {{
    --accent: {theme["accent"]};
    --foreground: {theme["text"]};
}}

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    color: {theme["text"]};
    background:
        radial-gradient(
            ellipse at 12% 5%,
            rgba({theme["glow"]},0.23),
            transparent 36%
        ),
        radial-gradient(
            ellipse at 90% 25%,
            rgba({theme["glow"]},0.13),
            transparent 34%
        ),
        {theme["bg"]};
    background-attachment: fixed;
}}

#MainMenu, footer, header {{
    visibility: hidden;
}}

.block-container {{
    max-width: 1050px;
    padding-top: 2.2rem;
    padding-bottom: 5rem;
}}

[data-testid="stSidebar"] {{
    background: {theme["sidebar"]};
    border-right: 1px solid
        rgba({theme["border"]},0.22);
    backdrop-filter: blur(24px);
}}

[data-testid="stSidebar"] > div:first-child {{
    background: transparent;
}}

.brand {{
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -1.5px;
    padding: 8px 0 24px;
    color: #FFFFFF;
}}

.brand span {{
    background: linear-gradient(
        110deg,
        {theme["accent"]},
        #FFFFFF
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
    color: {theme["muted"]};
}}

.stButton > button {{
    color: {theme["text"]};
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba({theme["border"]},0.20);
    border-radius: 13px;
    min-height: 43px;
    transition: all 0.22s ease;
}}

.stButton > button:hover {{
    color: #FFFFFF;
    background: rgba({theme["glow"]},0.15);
    border-color: {theme["accent"]};
    box-shadow: 0 0 24px rgba({theme["glow"]},0.17);
    transform: translateY(-1px);
}}

[data-testid="stSelectbox"] > div > div {{
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba({theme["border"]},0.24);
    border-radius: 12px;
}}

.welcome {{
    text-align: center;
    padding-top: 10vh;
    padding-bottom: 30px;
}}

.orb {{
    width: 74px;
    height: 74px;
    margin: 0 auto 25px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 25px;
    font-size: 35px;
    color: white;
    background: linear-gradient(
        135deg,
        {theme["accent"]},
        {theme["bg"]}
    );
    border: 1px solid rgba({theme["border"]},0.4);
    box-shadow:
        0 0 45px rgba({theme["glow"]},0.32),
        inset 0 0 20px rgba(255,255,255,0.08);
}}

.welcome h1 {{
    color: {theme["text"]};
    font-size: clamp(29px,4vw,44px);
    font-weight: 700;
    letter-spacing: -1.8px;
}}

.welcome p {{
    color: {theme["muted"]};
    font-size: 15px;
    line-height: 1.8;
}}

.section-heading {{
    color: {theme["muted"]};
    text-align: center;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    margin: 12px 0 18px;
}}

[data-testid="stChatMessage"] {{
    background: rgba(255,255,255,0.027);
    border: 1px solid rgba({theme["border"]},0.14);
    border-radius: 20px;
    padding: 17px 19px;
    margin: 13px 0;
    backdrop-filter: blur(18px);
}}

[data-testid="stChatMessage"] p {{
    color: {theme["text"]};
    line-height: 1.85;
}}

[data-testid="stChatInput"] {{
    background: rgba({theme["glow"]},0.075);
    border: 1px solid rgba({theme["border"]},0.36);
    border-radius: 21px;
    box-shadow: 0 8px 35px rgba(0,0,0,0.22);
    backdrop-filter: blur(22px);
}}

[data-testid="stChatInput"]:focus-within {{
    border-color: {theme["accent"]};
    box-shadow: 0 0 25px rgba({theme["glow"]},0.18);
}}

[data-testid="stChatInput"] textarea {{
    color: {theme["text"]};
}}

[data-testid="stChatInput"] textarea::placeholder {{
    color: {theme["muted"]};
}}

[data-testid="stChatMessage"] code {{
    color: {theme["accent"]};
}}

[data-testid="stChatMessage"] pre {{
    border: 1px solid rgba({theme["border"]},0.2);
    border-radius: 14px;
}}

hr {{
    border-color: rgba({theme["border"]},0.17);
}}

.footer-note {{
    color: {theme["muted"]};
    text-align: center;
    font-size: 11px;
    padding-top: 22px;
}}

::-webkit-scrollbar {{
    width: 6px;
}}

::-webkit-scrollbar-thumb {{
    background: rgba({theme["border"]},0.35);
    border-radius: 20px;
}}
</style>
""", unsafe_allow_html=True)

# ============== CHAT SIDEBAR ==============
with st.sidebar:
    st.markdown("---")

    if st.button("＋   New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.chats.insert(0, {
            "id": new_id,
            "title": "New Chat",
            "messages": []
        })
        st.session_state.active_chat = new_id
        st.rerun()

    st.markdown("---")
    st.caption("YOUR CONVERSATIONS")

    for item in st.session_state.chats:
        label = "◦   " + item["title"][:25]
        if st.button(
            label,
            key="history_" + item["id"],
            use_container_width=True
        ):
            st.session_state.active_chat = item["id"]
            st.rerun()

    st.markdown("---")
    st.caption("✦ Powered by Groq")
    st.caption("Raain AI · Premium Edition")

# ============== MAIN SCREEN ==============
chat = active_chat()

if not chat["messages"]:
    st.markdown("""
    <div class="welcome">
        <div class="orb">✦</div>
        <h1>What can I help with?</h1>
        <p>Your ideas, questions and creativity.<br>
        One intelligent assistant, endless possibilities.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">EXPLORE YOUR POSSIBILITIES</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✧   Learn English", use_container_width=True):
            st.session_state.suggested_prompt = (
                "Teach me English step by step as a beginner."
            )
            st.rerun()

        if st.button("⌘   Learn Python", use_container_width=True):
            st.session_state.suggested_prompt = (
                "Teach me Python from absolute beginner level."
            )
            st.rerun()

    with col2:
        if st.button("✦   Explore AI", use_container_width=True):
            st.session_state.suggested_prompt = (
                "Explain artificial intelligence in simple terms."
            )
            st.rerun()

        if st.button("▤   Study Assistant", use_container_width=True):
            st.session_state.suggested_prompt = (
                "Help me create an effective study plan."
            )
            st.rerun()

else:
    for message in chat["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ============== AI INPUT ==============
suggested = st.session_state.pop("suggested_prompt", None)
prompt = st.chat_input("Message Raain AI...")

if suggested:
    prompt = suggested

if prompt:
    if not chat["messages"]:
        chat["title"] = prompt[:25]

    chat["messages"].append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            api_key = st.secrets["GROQ_API_KEY"]

            messages = [{
                "role": "system",
                "content": (
                    "You are Raain AI, a helpful assistant. "
                    "Reply in the language the user uses. "
                    "For Bangla, use Bengali script, not Banglish. "
                    "For English, answer in English. "
                    "Never randomly switch languages. "
                    "Be clear, friendly, and accurate."
                )
            }] + chat["messages"]

            with st.spinner("Raain AI is thinking..."):
                response = requests.post(
                    API_URL,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": MODEL,
                        "messages": messages,
                        "max_tokens": 1200,
                        "temperature": 0.7
                    },
                    timeout=120
                )

            if response.status_code == 429:
                st.error(
                    "Usage limit reached. Please wait and try again."
                )
                chat["messages"].pop()

            else:
                response.raise_for_status()
                answer = response.json()["choices"][0]["message"]["content"]

                st.markdown(answer)

                chat["messages"].append({
                    "role": "assistant",
                    "content": answer
                })

        except KeyError:
            st.error(
                "API key missing. Add GROQ_API_KEY in Streamlit Secrets."
            )
            chat["messages"].pop()

        except requests.exceptions.HTTPError as error:
            st.error(
                f"API error: {error}. Check your API key, model and usage limit."
            )
            chat["messages"].pop()

        except requests.exceptions.RequestException:
            st.error(
                "Cannot reach the AI server. Check your internet connection."
            )
            chat["messages"].pop()

        except (ValueError, KeyError):
            st.error("Could not read the AI response. Please try again.")
            chat["messages"].pop()

st.markdown(
    '<div class="footer-note">'
    'Raain AI can make mistakes. Verify important information.'
    '</div>',
    unsafe_allow_html=True
)
