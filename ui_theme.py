import streamlit as st

# --- THEME ---
def apply_theme():
    st.markdown("""
    <style>
    /* --- Global Fonts & Background --- */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(to right, #f8fafc, #e2e8f0);
    }

    /* --- Headers --- */
    h1, h2, h3, h4, h5 {
        color: #1e3a8a;
    }

    /* --- Buttons --- */
    div.stButton > button {
        background: linear-gradient(90deg, #3a6ea5, #88b0f7);
        color: white;
        border-radius: 10px;
        height: 40px;
        width: 100%;
        font-weight: bold;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
    }

    /* --- File Uploader --- */
    .stFileUploader {
        border: 2px dashed #3a6ea5;
        border-radius: 10px;
        padding: 10px;
    }

    /* --- Tabs --- */
    .css-1fceugx.edgvbvh3 {
        background: #f1f5f9;
        border-radius: 10px;
    }

    /* --- Expander --- */
    .streamlit-expanderHeader {
        font-weight: bold;
        color: #1e40af;
    }

    /* --- Alerts --- */
    .stAlert {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
def render_sidebar():
    st.sidebar.markdown("""
    <div style='text-align:center; padding:10px; background: linear-gradient(90deg, #3a6ea5, #88b0f7); border-radius:10px; color:white;'>
        <h2>LegalLite ⚖️</h2>
        <p style='font-size:12px;'>AI Legal Assistant</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("### 🔹 Navigation")
    pages = ["Profile", "Upload", "Risky Terms", "History"]
    for p in pages:
        if st.sidebar.button(p):
            st.session_state.current_page = p.lower().replace(" ", "_")

    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.sidebar.markdown("### ⚡ Pro Tips")
    st.sidebar.info("Upload PDF documents for a quick AI summary.")
    st.sidebar.info("Check for risky terms before signing any contract.")
    st.sidebar.info("Download summaries as PDF or audio for convenience.")
