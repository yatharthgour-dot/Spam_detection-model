import time
import joblib
import streamlit as st

# ----------------------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Spam Scanner",
    page_icon="📡",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# Theme: a message-scanning "terminal" — incoming transmissions get swept
# for threats, flagged terms light up, and a verdict gets stamped.
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600&display=swap');

    #MainMenu, header, footer { visibility: hidden; }

    .stApp {
        background: radial-gradient(circle at 50% -10%, #16213a 0%, #0b0f1a 55%, #07090f 100%);
        font-family: 'Inter', sans-serif;
        color: #E6E9F0;
    }

    .block-container { padding-top: 2.2rem; max-width: 760px; }

    /* ---- Header ---- */
    .scan-eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        letter-spacing: 0.22em;
        color: #5FE3C0;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    .scan-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.1rem;
        font-weight: 700;
        color: #F2F4F8;
        margin: 0;
        line-height: 1.2;
    }
    .scan-sub {
        color: #8993A8;
        font-size: 0.95rem;
        margin-top: 0.4rem;
        margin-bottom: 1.6rem;
    }

    /* ---- Input panel ---- */
    .stTextArea textarea {
        background: #0F1626 !important;
        border: 1px solid #232C42 !important;
        border-radius: 10px !important;
        color: #E6E9F0 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.92rem !important;
    }
    .stTextArea textarea:focus {
        border-color: #5FE3C0 !important;
        box-shadow: 0 0 0 1px #5FE3C0 !important;
    }
    label { color: #8993A8 !important; font-size: 0.8rem !important; letter-spacing: 0.05em; }

    div[data-testid="stButton"] button {
        background: #5FE3C0;
        color: #07090f;
        border: none;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        letter-spacing: 0.06em;
        padding: 0.55rem 1.2rem;
        transition: transform 0.12s ease, box-shadow 0.12s ease;
    }
    div[data-testid="stButton"] button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(95, 227, 192, 0.25);
        color: #07090f;
    }
    div[data-testid="stButton"] button[kind="secondary"] {
        background: transparent;
        color: #8993A8;
        border: 1px solid #232C42;
        font-weight: 500;
    }
    div[data-testid="stButton"] button[kind="secondary"]:hover {
        border-color: #5FE3C0;
        color: #5FE3C0;
    }

    /* ---- Scan line animation while "analyzing" ---- */
    .scanner-box {
        position: relative;
        overflow: hidden;
        border: 1px solid #232C42;
        border-radius: 10px;
        background: #0F1626;
        padding: 1.4rem;
        font-family: 'JetBrains Mono', monospace;
        color: #5FE3C0;
        font-size: 0.85rem;
        letter-spacing: 0.08em;
    }
    .scanner-box::after {
        content: "";
        position: absolute;
        left: 0; top: 0;
        width: 100%; height: 2px;
        background: linear-gradient(90deg, transparent, #5FE3C0, transparent);
        animation: sweep 1.1s linear infinite;
    }
    @keyframes sweep {
        0% { top: 0%; }
        100% { top: 100%; }
    }

    /* ---- Verdict card ---- */
    .verdict {
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        margin-top: 0.6rem;
        border: 1px solid;
    }
    .verdict-spam { background: rgba(255, 92, 92, 0.08); border-color: #FF5C5C; }
    .verdict-ham  { background: rgba(95, 227, 192, 0.08); border-color: #5FE3C0; }

    .verdict-label {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 1.3rem;
        letter-spacing: 0.05em;
    }
    .verdict-spam .verdict-label { color: #FF5C5C; }
    .verdict-ham .verdict-label { color: #5FE3C0; }

    .verdict-meta {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #8993A8;
        margin-top: 0.2rem;
    }

    .chip {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        background: rgba(255, 92, 92, 0.12);
        color: #FF8C8C;
        border: 1px solid rgba(255, 92, 92, 0.35);
        border-radius: 999px;
        padding: 0.18rem 0.6rem;
        margin: 0.25rem 0.3rem 0 0;
    }

    /* ---- History rows ---- */
    .hist-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.55rem 0.2rem;
        border-bottom: 1px solid #1A2236;
        font-size: 0.86rem;
    }
    .hist-text { color: #B6BCCB; max-width: 70%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .tag-spam { color: #FF5C5C; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; }
    .tag-ham { color: #5FE3C0; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; }

    section[data-testid="stSidebar"] {
        background: #0B0F1A;
        border-right: 1px solid #1A2236;
    }
    section[data-testid="stSidebar"] * { color: #B6BCCB; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Load model (cached so it only loads once per session)
# ----------------------------------------------------------------------------
@st.cache_resource
def load_artifacts():
    model = joblib.load("model/spam_model.pkl")
    vectorizer = joblib.load("model/vectorizer.pkl")
    return model, vectorizer


model_error = None
try:
    model, vectorizer = load_artifacts()
except Exception as e:
    model, vectorizer = None, None
    model_error = str(e)

# ----------------------------------------------------------------------------
# Session state
# ----------------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: text, label, confidence
if "draft" not in st.session_state:
    st.session_state.draft = ""


def set_draft(text):
    st.session_state.draft = text


def flagged_terms(text_vector, top_n=6):
    """Pull out the words in this message that pushed the verdict toward spam."""
    try:
        feature_names = vectorizer.get_feature_names_out()
        if hasattr(model, "coef_"):
            weights = model.coef_[0]
        elif hasattr(model, "feature_log_prob_"):
            weights = model.feature_log_prob_[1] - model.feature_log_prob_[0]
        else:
            return []
        idx = text_vector.nonzero()[1]
        scored = sorted(
            ((feature_names[i], weights[i]) for i in idx),
            key=lambda x: x[1],
            reverse=True,
        )
        return [w for w, s in scored if s > 0][:top_n]
    except Exception:
        return []


def run_prediction(text):
    text_vector = vectorizer.transform([text])
    prediction = model.predict(text_vector)[0]
    confidence = None
    if hasattr(model, "predict_proba"):
        try:
            confidence = max(model.predict_proba(text_vector)[0])
        except Exception:
            confidence = None
    terms = flagged_terms(text_vector) if prediction == 1 else []
    return ("Spam" if prediction == 1 else "Ham"), confidence, terms


# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("##### 📡 SYSTEM STATUS")
    if model_error:
        st.error(f"Model not loaded:\n{model_error}")
        st.caption("Check that model/spam_model.pkl and model/vectorizer.pkl exist.")
    else:
        st.success("Model online")

    st.markdown("---")
    st.markdown("##### HOW IT WORKS")
    st.caption(
        "Every message is converted into the same numeric features the model "
        "was trained on, then classified as **Spam** or **Ham** (a normal "
        "message). If the model exposes word weights, the terms that pushed "
        "a message toward Spam are highlighted below the verdict."
    )

    st.markdown("---")
    st.markdown("##### SESSION STATS")
    total = len(st.session_state.history)
    spam_count = sum(1 for h in st.session_state.history if h["label"] == "Spam")
    ham_count = total - spam_count
    c1, c2, c3 = st.columns(3)
    c1.metric("Scanned", total)
    c2.metric("Spam", spam_count)
    c3.metric("Ham", ham_count)

    if total:
        if st.button("Clear history", type="secondary", use_container_width=True):
            st.session_state.history = []
            st.rerun()

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.markdown('<div class="scan-eyebrow">INCOMING TRANSMISSION ANALYSIS</div>', unsafe_allow_html=True)
st.markdown('<h1 class="scan-title">SPAM SCANNER</h1>', unsafe_allow_html=True)
st.markdown(
    '<div class="scan-sub">Drop in a message below and run it through the filter.</div>',
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Quick examples
# ----------------------------------------------------------------------------
ex1, ex2, ex3 = st.columns(3)
with ex1:
    st.button(
        "🎁 Try a prize text",
        on_click=set_draft,
        args=("Congratulations! You've WON a $1000 Walmart gift card. Click here to claim now!!!",),
        use_container_width=True,
        type="secondary",
    )
with ex2:
    st.button(
        "💬 Try a normal text",
        on_click=set_draft,
        args=("Hey, are we still on for dinner at 7? Let me know if you want me to grab anything.",),
        use_container_width=True,
        type="secondary",
    )
with ex3:
    st.button(
        "🏦 Try a phishing text",
        on_click=set_draft,
        args=("Your account has been suspended. Verify your identity immediately at the link below to avoid closure.",),
        use_container_width=True,
        type="secondary",
    )

# ----------------------------------------------------------------------------
# Input
# ----------------------------------------------------------------------------
message = st.text_area(
    "MESSAGE TO SCAN",
    value=st.session_state.draft,
    height=140,
    placeholder="Paste or type the message you want to check...",
    key="message_box",
)

analyze_clicked = st.button("▶ ANALYZE MESSAGE", type="primary", use_container_width=True, disabled=model is None)

# ----------------------------------------------------------------------------
# Run analysis
# ----------------------------------------------------------------------------
if analyze_clicked:
    text = message.strip()
    if not text:
        st.warning("Enter a message first — nothing to scan yet.")
    else:
        placeholder = st.empty()
        placeholder.markdown(
            '<div class="scanner-box">SCANNING TRANSMISSION ...</div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.6)
        label, confidence, terms = run_prediction(text)
        placeholder.empty()

        verdict_class = "verdict-spam" if label == "Spam" else "verdict-ham"
        icon = "🚨" if label == "Spam" else "✅"
        conf_str = f"{confidence * 100:.1f}% confidence" if confidence is not None else "confidence unavailable"

        chips_html = "".join(f'<span class="chip">{t}</span>' for t in terms)

        st.markdown(
            f"""
            <div class="verdict {verdict_class}">
                <div class="verdict-label">{icon} {label.upper()}</div>
                <div class="verdict-meta">{conf_str}</div>
                {f'<div style="margin-top:0.7rem;">{chips_html}</div>' if chips_html else ''}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.session_state.history.insert(
            0, {"text": text, "label": label, "confidence": confidence}
        )
        st.session_state.history = st.session_state.history[:8]

# ----------------------------------------------------------------------------
# Recent scans
# ----------------------------------------------------------------------------
if st.session_state.history:
    st.markdown("##### RECENT SCANS")
    for h in st.session_state.history:
        tag_class = "tag-spam" if h["label"] == "Spam" else "tag-ham"
        preview = h["text"][:70] + ("…" if len(h["text"]) > 70 else "")
        st.markdown(
            f"""
            <div class="hist-row">
                <span class="hist-text">{preview}</span>
                <span class="{tag_class}">{h['label'].upper()}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
