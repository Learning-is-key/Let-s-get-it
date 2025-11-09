import streamlit as st

def apply_theme():
    """Applies custom styling across the entire app."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background: radial-gradient(circle at top left, #f0f4ff, #dbe7ff);
    }

    h1, h2, h3 {
        color: #1e3a8a;
        font-weight: 700;
    }

    /* --- Buttons --- */
    div.stButton > button {
        background: linear-gradient(135deg, #3a6ea5, #5e9cff);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 8px 0;
        font-weight: 600;
        transition: all 0.25s ease;
        width: 100%;
    }

    div.stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 6px 18px rgba(58, 110, 165, 0.35);
    }

    /* --- Sidebar container --- */
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(14px);
        border-right: 1px solid rgba(255,255,255,0.25);
        padding-top: 10px;
    }

    /* --- Sidebar title --- */
    .sidebar-title {
        text-align: center;
        color: #ffffff;
        background: linear-gradient(90deg, #3a6ea5, #5e9cff);
        padding: 15px 10px;
        border-radius: 12px;
        margin-bottom: 15px;
    }

    .sidebar-title h2 {
        margin: 0;
        font-size: 22px;
    }

    .sidebar-title p {
        font-size: 12px;
        color: #e2e8f0;
        margin: 0;
    }

    /* --- Navigation cards --- */
    .nav-card {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 12px;
        padding: 10px 15px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.25s ease;
        color: white;
        font-weight: 500;
    }

    .nav-card:hover {
        background: rgba(255,255,255,0.35);
        transform: scale(1.02);
        box-shadow: 0 6px 15px rgba(0,0,0,0.15);
    }

    /* --- Info tips --- */
    .tip-box {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        padding: 10px;
        margin-top: 20px;
        color: #e2e8f0;
        font-size: 13px;
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Draws glassmorphic sidebar with navigation cards."""
    st.sidebar.markdown("""
    <div class="sidebar-title">
        <h2>⚖️ LegalLite</h2>
        <p>Simplify • Summarize • Secure</p>
    </div>
    """, unsafe_allow_html=True)

    nav_items = [
        ("📤 Upload & Simplify", "upload"),
        ("👤 Profile", "profile"),
        ("🚨 Risky Terms Detector", "risky_terms"),
        ("🕓 My History", "history"),
        ("❓ Help & Feedback", "help")
    ]

    for label, key in nav_items:
        if st.sidebar.button(label, key=f"nav_{key}"):
            st.session_state.current_page = key

    st.sidebar.markdown("""
    <div class="tip-box">
        💡 <b>Pro Tip:</b> Upload any PDF or DOCX to get instant summaries and legal risk detection.
    </div>
    """, unsafe_allow_html=True)
