import streamlit as st

from api_client import (
    API_BASE_URL,
    BackendError,
    BackendTimeoutError,
    BackendUnavailableError,
    ConfigurationError,
    ask_question,
    check_backend_health,
)

# --------------------------------------------------------------------------
# Page configuration
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Support Desk — AI Help Assistant",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# Design tokens
# --------------------------------------------------------------------------
NAVY = "#1E293B"       # Sidebar background (Soft Slate)
NAVY_SOFT = "#334155"  # Lighter Slate for gradients
INK = "#E2E8F0"        # Main text (Soft off-white)
PAPER = "#0F172A"      # Main app background (Deep Slate)
CARD = "#1E293B"       # Chat bubbles and input fields
AMBER = "#38BDF8"      # Primary Accent (Soft Sky Blue)
AMBER_DARK = "#0284C7" # Darker Accent for active states
LINE = "#475569"       # Subtle borders
MUTED = "#94A3B8"      # Secondary text/captions
GOOD = "#10B981"       # Success indicator (Mint Green)
BAD = "#F43F5E"        # Error indicator (Soft Rose)

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        color: {INK};
    }}

    .stApp {{
        background: {PAPER};
    }}

    #MainMenu, footer, header {{visibility: hidden;}}

    /* Kill Streamlit's built-in "rerunning" dim/fade */
    [data-stale="true"] {{
        opacity: 1 !important;
        transition: none !important;
    }}
    .element-container, .stMarkdown, .stButton, .stTextInput, .stCaption {{
        opacity: 1 !important;
    }}

    .block-container {{
        padding-top: 1.4rem;
        max-width: 860px;
    }}

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {{
        background: {NAVY};
    }}
    section[data-testid="stSidebar"] * {{
        color: #E7EAF0;
    }}
    .side-brand {{
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.15rem;
        color: #F3EEE1;
        margin-bottom: 0.1rem;
    }}
    .side-brand-sub {{
        font-size: 0.78rem;
        color: #9FACC2;
        margin-bottom: 1.3rem;
    }}
    .status-row {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.85rem;
        padding: 0.55rem 0.7rem;
        border-radius: 8px;
        background: rgba(255,255,255,0.06);
        margin-bottom: 1.1rem;
    }}
    .status-dot {{
        width: 8px; height: 8px;
        border-radius: 50%;
        flex-shrink: 0;
    }}
    .side-section-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.78rem;
        font-weight: 600;
        color: #9FACC2;
        margin: 1.1rem 0 0.5rem 0;
    }}
    .side-scope-item {{
        font-size: 0.85rem;
        color: #D6DBE5;
        padding: 0.3rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.07);
    }}
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button {{
        width: 100%;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.18);
        color: #F3EEE1;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 500;
        padding: 0.5rem 0.7rem;
    }}
    section[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {{
        border-color: {AMBER};
        color: #F3EEE1;
    }}

    /* ---------- Hero banner ---------- */
    .desk-hero {{
        background: linear-gradient(135deg, {NAVY} 0%, {NAVY_SOFT} 100%);
        border-radius: 12px;
        padding: 1.7rem 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }}
    .desk-hero::after {{
        content: "";
        position: absolute;
        top: -40px; right: -40px;
        width: 150px; height: 150px;
        border-radius: 50%;
        background: {AMBER};
        opacity: 0.13;
    }}
    .desk-kicker {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.78rem;
        font-weight: 600;
        color: {AMBER};
        margin: 0 0 0.4rem 0;
    }}
    .desk-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.65rem;
        font-weight: 700;
        color: #F3EEE1;
        margin: 0;
        line-height: 1.3;
        max-width: 34ch;
    }}

    /* ---------- Suggested questions ---------- */
    .prompt-heading {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        color: {MUTED};
        margin: 0.1rem 0 0.65rem 0;
    }}
    div[data-testid="stVerticalBlock"] div[data-testid="stButton"] > button {{
        width: 100%;
        text-align: left;
        background: {CARD};
        border: 1px solid {LINE};
        border-radius: 10px;
        padding: 0.7rem 0.95rem;
        font-size: 0.85rem;
        color: {INK};
        font-weight: 500;
        transition: border-color 0.15s ease, background 0.15s ease;
        white-space: normal;
        line-height: 1.4;
    }}
    div[data-testid="stVerticalBlock"] div[data-testid="stButton"] > button:hover {{
        border-color: {AMBER};
        background: {NAVY_SOFT};
        color: {INK};
    }}

    /* ---------- Chat bubbles ---------- */
    div[data-testid="stChatMessage"] {{
        background: {CARD};
        border: 1px solid {LINE};
        border-radius: 12px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.7rem;
    }}

    /* ---------- Chat input (bottom bar) ---------- */
    [data-testid="stChatInput"] {{
        background: {PAPER};
    }}
    [data-testid="stChatInput"] textarea {{
        background: {CARD} !important;
        color: {INK} !important;
        border: 1px solid {LINE} !important;
        border-radius: 10px !important;
    }}
    [data-testid="stChatInput"] textarea::placeholder {{
        color: {MUTED} !important;
        opacity: 1 !important;
    }}
    [data-testid="stChatInput"] textarea:disabled {{
        background: {LINE} !important;
        color: {MUTED} !important;
    }}
    [data-testid="stChatInput"] button svg {{
        fill: {AMBER_DARK} !important;
    }}

    /* ---------- Main-area buttons, incl. disabled suggestion buttons ---------- */
    .main div[data-testid="stButton"] > button:disabled {{
        background: {LINE} !important;
        border: 1px solid {LINE} !important;
        color: {MUTED} !important;
        opacity: 1 !important;
    }}

    /* ---------- Text colour safety net ---------- */
    .stApp, .stApp p, .stApp span, .stApp li, .stApp label {{
        color: {INK};
    }}
    .stApp .stMarkdown, .stApp .stCaption, .stApp small {{
        color: {INK};
    }}
    div[data-testid="stCaptionContainer"], .stCaption, small {{
        color: {MUTED} !important;
    }}
    section[data-testid="stSidebar"] div[data-testid="stCaptionContainer"],
    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] small {{
        color: #9FACC2 !important;
    }}
    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] li,
    div[data-testid="stChatMessage"] span {{
        color: {INK} !important;
    }}

    /* ---------- Misc ---------- */
    hr {{ border-color: {LINE}; }}
    .footnote {{
        font-size: 0.76rem;
        color: {MUTED};
        text-align: center;
        margin-top: 1.2rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Backend health check
# --------------------------------------------------------------------------
CONFIGURED = API_BASE_URL is not None
DISPLAY_URL = API_BASE_URL if CONFIGURED else "API_BASE_URL (not configured)"


@st.cache_data(ttl=15, show_spinner=False)
def backend_is_online() -> bool:
    return check_backend_health()


backend_up = backend_is_online()

if not CONFIGURED:
    st.error(
        "API_BASE_URL is not set. Copy `frontend/.env.example` to `frontend/.env`, "
        "set `API_BASE_URL=http://localhost:8000`, and restart the app."
    )

# --------------------------------------------------------------------------
# Sidebar — status, scope, controls
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<p class="side-brand">📦 Support Desk</p>', unsafe_allow_html=True)
    st.markdown('<p class="side-brand-sub">AI help assistant</p>', unsafe_allow_html=True)

    dot_color = GOOD if backend_up else BAD
    status_text = "Assistant is online" if backend_up else "Assistant is offline"
    st.markdown(
        f"""
        <div class="status-row">
            <span class="status-dot" style="background:{dot_color};"></span>
            <span>{status_text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if not backend_up:
        st.caption(f"Can't reach the backend at `{DISPLAY_URL}`. Start the backend (uvicorn) and refresh.")

    if st.button("↺ Start a new conversation"):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()

    st.markdown('<p class="side-section-title">What I can help with</p>', unsafe_allow_html=True)
    for item in [
        "Orders & shipping",
        "Returns & refunds",
        "Account & security",
        "Product specs & pricing",
        "Seller support",
    ]:
        st.markdown(f'<div class="side-scope-item">{item}</div>', unsafe_allow_html=True)

# --------------------------------------------------------------------------
# Hero
# --------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="desk-hero">
        <p class="desk-kicker">STORE SUPPORT · AI ASSISTANT</p>
        <p class="desk-title">Ask about your orders, returns, shipping, or any product in the catalog.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

SUGGESTED_QUESTIONS = [
    "How do I cancel an order that's already shipped?",
    "What's the return window and what items can't be returned?",
    "How do I enable two-factor authentication?",
    "What are the specs and price of the SoundSculpt headphones?",
    "My package is missing — what should I do?",
    "Can I pay for an order using multiple payment methods?",
]

# --------------------------------------------------------------------------
# Suggested questions — Always visible (so they stay on screen)
# --------------------------------------------------------------------------
st.markdown('<p class="prompt-heading">Suggested Questions</p>', unsafe_allow_html=True)
cols = st.columns(2)
for i, q in enumerate(SUGGESTED_QUESTIONS):
    with cols[i % 2]:
        if st.button(q, key=f"suggest_{i}", disabled=not backend_up):
            st.session_state.pending_question = q
st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# Render chat history
# --------------------------------------------------------------------------
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "📦"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


def handle_question(question: str):
    """Send a question to the backend and record the exchange."""
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="📦"):
        placeholder = st.empty()
        placeholder.markdown("_Checking the docs…_")
        try:
            data = ask_question(question)
            bot_answer = data.get("answer", "No answer returned.")
            sources = data.get("sources") or []

            placeholder.markdown(bot_answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": bot_answer, "sources": sources}
            )
        except ConfigurationError:
            err_text = (
                "⚠️ The backend URL is not configured. Copy `frontend/.env.example` to "
                "`frontend/.env`, set `API_BASE_URL`, and restart the app."
            )
            placeholder.markdown(err_text)
            st.session_state.messages.append({"role": "assistant", "content": err_text})
        except BackendUnavailableError:
            err_text = (
                f"⚠️ I can't reach the backend right now. Make sure it is running at "
                f"`{DISPLAY_URL}`, then try again."
            )
            placeholder.markdown(err_text)
            st.session_state.messages.append({"role": "assistant", "content": err_text})
        except BackendTimeoutError:
            err_text = "⚠️ That took too long to answer. Please try again."
            placeholder.markdown(err_text)
            st.session_state.messages.append({"role": "assistant", "content": err_text})
        except BackendError as err:
            err_text = (
                f"I ran into a problem answering that (server returned {err.status_code}). "
                f"Please try rephrasing the question or try again in a moment."
            )
            placeholder.markdown(err_text)
            st.session_state.messages.append({"role": "assistant", "content": err_text})
        except Exception as e:
            err_text = f"An unexpected error occurred: {e}"
            placeholder.markdown(err_text)
            st.session_state.messages.append({"role": "assistant", "content": err_text})


# --------------------------------------------------------------------------
# Process a suggested-question click
# --------------------------------------------------------------------------
if st.session_state.pending_question:
    q = st.session_state.pending_question
    st.session_state.pending_question = None
    handle_question(q)
    st.rerun()

# --------------------------------------------------------------------------
# Free-text input
# --------------------------------------------------------------------------
if user_prompt := st.chat_input(
    "Type your question here..." if backend_up else "Backend offline — start the backend first",
    disabled=not backend_up,
):
    handle_question(user_prompt)



#streamlit run app.py