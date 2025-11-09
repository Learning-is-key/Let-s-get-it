import streamlit as st
import fitz  # PyMuPDF
import requests
import hashlib
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from db import init_db, register_user, login_user, save_upload, get_user_history
from gtts import gTTS
from ui_theme import apply_theme, render_sidebar

# --- THEME & SIDEBAR ---
apply_theme()
render_sidebar()

# Load Hugging Face token
try:
    hf_token = st.secrets["HF_TOKEN"]
except Exception:
    hf_token = ""

# --- INIT DB ---
init_db()

# --- CONFIG ---
st.set_page_config(page_title="LegalLite", layout="wide", page_icon="⚖️")

# --- HEADER ---
st.markdown("""
<div style='text-align:center; background: linear-gradient(90deg, #3a6ea5, #88b0f7); 
            padding:25px; border-radius:15px; color:white;'>
    <h1>LegalLite ⚖️</h1>
    <p style='font-size:14px;'>Your AI-powered legal assistant</p>
</div>
<br>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
for key in ["logged_in", "user_email", "mode", "api_key", "mode_chosen", "current_page"]:
    if key not in st.session_state:
        st.session_state[key] = False if key == "logged_in" else ""

# --- UTILITY ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_pdf(summary_text, filename):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    margin = 40
    y = height - margin
    c.drawString(margin, y, f"LegalLite Summary - {filename}")
    y -= 20
    c.drawString(margin, y, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 30
    for line in summary_text.split('\n'):
        for subline in [line[i:i+90] for i in range(0, len(line), 90)]:
            if y < margin:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = height - margin
            c.drawString(margin, y, subline)
            y -= 20
    c.save()
    buffer.seek(0)
    return buffer

def generate_voice(summary_text):
    try:
        tts = gTTS(summary_text, lang='en')
        audio_path = "summary_audio.mp3"
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        st.error(f"❌ Voice generation failed: {e}")
        return None

@st.cache_data
def query_huggingface_api(prompt):
    API_URL = "https://api-inference.huggingface.co/models/csebuetnlp/mT5_multilingual_XLSum"
    headers = {"Authorization": f"Bearer {hf_token}"}
    try:
        response = requests.post(API_URL, headers=headers, json={
            "inputs": prompt,
            "parameters": {"max_length": 200, "do_sample": False},
            "options": {"wait_for_model": True}
        })
        if response.status_code != 200:
            return f"❌ API Error {response.status_code}: {response.text}"
        output = response.json()
        if isinstance(output, list) and len(output) > 0:
            return output[0].get("summary_text", str(output[0]))
        if isinstance(output, dict) and "summary_text" in output:
            return output["summary_text"]
        return f"⚠️ Unexpected output: {output}"
    except Exception as e:
        return f"❌ Exception: {str(e)}"

# --- LOGIN & SIGNUP ---
def login_section():
    st.subheader("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(email, hash_password(password))
        if user:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.success(f"Welcome back, {email}!")
        else:
            st.error("Invalid email or password.")

def signup_section():
    st.subheader("📝 Create Account")
    email = st.text_input("New Email")
    password = st.text_input("New Password", type="password")
    if st.button("Sign Up"):
        if register_user(email, hash_password(password)):
            st.success("Account created! You can now login.")
        else:
            st.error("User already exists.") 

# --- MAIN APP ---
def app_main():
    # Navigation
    page = st.session_state.get("current_page", "upload")
    
    if page == "profile":
        st.subheader("👤 Your Profile")
        st.write(f"**Logged in as:** `{st.session_state.user_email}`")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.success("Logged out. Refresh to login again.")
    
    elif page == "upload":
        st.subheader("📑 Upload & Simplify Legal Document")
        uploaded_file = st.file_uploader("Select a legal PDF", type=["pdf"])
        if uploaded_file:
            try:
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                full_text = "".join([page.get_text() for page in doc])
                st.success("✅ Text extracted from PDF.")
                st.text_area("📄 Extracted Text", full_text, height=300)
            except Exception as e:
                st.error(f"❌ Error reading PDF: {str(e)}")
                return
            if st.button("🧐 Simplify Document"):
                simplified = "📜 Demo Summary: Simplified content goes here."
                st.subheader("✅ Simplified Summary")
                st.success(simplified)
                save_upload(st.session_state.user_email, uploaded_file.name, simplified)
                # PDF
                pdf_file = generate_pdf(simplified, uploaded_file.name)
                st.download_button("📥 Download PDF", pdf_file, f"simplified_{uploaded_file.name.replace('.pdf','')}.pdf", mime="application/pdf")
                # Voice
                audio_file_path = generate_voice(simplified)
                if audio_file_path:
                    with open(audio_file_path, "rb") as audio_file:
                        st.audio(audio_file.read(), format="audio/mp3")
                        st.download_button("🎧 Download Audio", audio_file.read(), "summary_audio.mp3", mime="audio/mp3")

    elif page == "risky_terms":
        st.subheader("🚨 Risky Terms Detector")
        uploaded_file = st.file_uploader("Upload a legal PDF", type=["pdf"])
        if uploaded_file:
            try:
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                full_text = "".join([page.get_text() for page in doc])
                risky_terms = ["penalty", "termination", "breach", "fine"]
                found = [term for term in risky_terms if term in full_text.lower()]
                if found:
                    st.error(f"❗ Risky Terms Found: {', '.join(found)}")
                else:
                    st.success("✅ No risky terms found")
            except Exception as e:
                st.error(f"❌ Error reading PDF: {e}")

    elif page == "history":
        st.subheader("⏳ Upload History")
        history = get_user_history(st.session_state.user_email)
        if not history:
            st.info("No uploads yet.")
        else:
            for file_name, summary, timestamp in history:
                with st.expander(f"📄 {file_name} | 🕒 {timestamp}"):
                    st.text(summary)

# --- ROUTING ---
if not st.session_state.logged_in:
    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])
    with login_tab:
        login_section()
    with signup_tab:
        signup_section()
else:
    if not st.session_state.mode_chosen:
        st.subheader("🎛️ Choose LegalLite Mode")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🧪 Demo Mode"):
                st.session_state.mode = "Demo"
                st.session_state.mode_chosen = True
        with col2:
            if st.button("🔐 OpenAI API Key"):
                st.session_state.mode = "OpenAI"
                st.session_state.mode_chosen = True
        with col3:
            if st.button("🌐 Hugging Face"):
                st.session_state.mode = "HuggingFace"
                st.session_state.mode_chosen = True
    else:
        app_main()

# --- FOOTER ---
st.markdown("""
<hr style='border:1px solid #ddd;'>
<p style='text-align:center; color: gray; font-size:12px;'>
⚡DISCLAIMER: LegalLite does not replace professional legal advice.
</p>
<p style='text-align:center; color: gray; font-size:12px;'>
© 2025 LegalLite | Built with ❤️ in Streamlit
</p>
""", unsafe_allow_html=True)
