import streamlit as st
from PIL import Image
from fpdf import FPDF
import os
import base64

APP_NAME = "UNI-FIREEE"
EMAIL = "adishaikh776@gmail.com"
EXAM_FOLDER = "exam_papers"

os.makedirs(EXAM_FOLDER, exist_ok=True)

# ================= SESSION =================
if "page" not in st.session_state:
    st.session_state.page = "home"

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title=APP_NAME,
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= GLOBAL STYLES =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

#MainMenu, footer, header { visibility: hidden; }

html, body, [data-testid="stAppViewContainer"] {
    background: #05070D;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(82,130,255,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(100,255,218,0.10) 0%, transparent 55%),
        #05070D;
    min-height: 100vh;
}

[data-testid="block-container"] {
    padding: 2rem 3rem 4rem;
    max-width: 1100px;
    margin: 0 auto;
}

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 56px 20px 40px;
    position: relative;
}

.hero-badge {
    display: inline-block;
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #64FFDA;
    background: rgba(100,255,218,0.08);
    border: 1px solid rgba(100,255,218,0.25);
    padding: 6px 18px;
    border-radius: 100px;
    margin-bottom: 22px;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(40px, 6vw, 72px);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #E8F0FF 30%, #64FFDA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 14px;
}

.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    color: #5A6A8A;
    letter-spacing: 1px;
    margin: 0;
}

/* ── Divider ── */
.divider {
    width: 48px;
    height: 2px;
    background: linear-gradient(90deg, #64FFDA, transparent);
    margin: 28px auto;
    border-radius: 2px;
}

/* ── Section Label ── */
.section-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #3A4A6A;
    margin-bottom: 16px;
    padding-left: 2px;
}

/* ── Nav Buttons ── */
div.stButton > button {
    width: 100%;
    background: rgba(255,255,255,0.03);
    color: #C8D6F0;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 22px 16px;
    border-radius: 16px;
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 600;
    height: 90px;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(8px);
    letter-spacing: 0.3px;
}

div.stButton > button::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(100,255,218,0.06), rgba(82,130,255,0.06));
    opacity: 0;
    transition: opacity 0.25s ease;
    border-radius: 16px;
}

div.stButton > button:hover {
    border-color: rgba(100,255,218,0.4);
    color: #64FFDA;
    transform: translateY(-3px);
    box-shadow:
        0 8px 32px rgba(0,0,0,0.4),
        0 0 0 1px rgba(100,255,218,0.15),
        inset 0 1px 0 rgba(255,255,255,0.05);
}

div.stButton > button:hover::before { opacity: 1; }

div.stButton > button:active { transform: translateY(-1px); }

/* ── Back Button ── */
div.stButton > button[kind="secondary"],
div.stButton:first-child > button {
    height: auto;
    padding: 10px 20px;
    font-size: 13px;
    border-radius: 8px;
    background: transparent;
    border-color: rgba(255,255,255,0.1);
    color: #5A6A8A;
    width: auto;
}

/* ── Page Header (inner pages) ── */
.page-header {
    padding: 20px 0 32px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 32px;
}

.page-header h1 {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 800;
    color: #E8F0FF;
    margin: 0 0 6px;
    letter-spacing: -0.5px;
}

.page-header p {
    color: #3A4A6A;
    font-size: 13px;
    margin: 0;
}

/* ── Upload Area ── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02);
    border: 1.5px dashed rgba(100,255,218,0.2);
    border-radius: 14px;
    padding: 8px;
    transition: border-color 0.2s;
}

[data-testid="stFileUploader"]:hover {
    border-color: rgba(100,255,218,0.5);
}

/* ── Download / Action Buttons ── */
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #1A3A5C, #0F2D4A) !important;
    border: 1px solid rgba(100,255,218,0.3) !important;
    color: #64FFDA !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s ease !important;
}

[data-testid="stDownloadButton"] > button:hover {
    background: linear-gradient(135deg, #64FFDA, #4DDAB8) !important;
    color: #05070D !important;
    border-color: transparent !important;
    box-shadow: 0 4px 20px rgba(100,255,218,0.3) !important;
}

/* ── Headings ── */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: #C8D6F0 !important;
}

/* ── Subject Grid Cards ── */
div.stButton > button:has(svg) {
    text-align: left;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 40px 20px 20px;
    color: #1E2D4A;
    font-size: 12px;
    letter-spacing: 1px;
    border-top: 1px solid rgba(255,255,255,0.04);
    margin-top: 60px;
}

.footer a {
    color: #3A5A7A;
    text-decoration: none;
}

.footer a:hover { color: #64FFDA; }

/* ── Streamlit text overrides ── */
p, li, label, .stText { color: #7A8AAA !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(100,255,218,0.2); border-radius: 2px; }

/* ── Error / info boxes ── */
[data-testid="stAlert"] {
    background: rgba(255,80,80,0.06) !important;
    border-color: rgba(255,80,80,0.2) !important;
    border-radius: 10px !important;
    color: #FF8888 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────
def back_button(label="⬅ Back", key="back"):
    if st.button(label, key=key):
        st.session_state.page = "home"
        st.rerun()

def page_header(icon, title, subtitle=""):
    st.markdown(f"""
    <div class="page-header">
        <h1>{icon} {title}</h1>
        {'<p>' + subtitle + '</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


# ── HOME ──────────────────────────────────────────────────
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">Student Portal</div>
        <div class="hero-title">UNI-FIREEE</div>
        <div class="hero-sub">Created by Bilal Shaikh</div>
    </div>
    <div class="divider"></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Quick Access</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")
    col4, col5, col6 = st.columns(3, gap="medium")

    with col1:
        if st.button("🖼️\nImage to PDF", use_container_width=True):
            st.session_state.page = "convert"
    with col2:
        if st.button("📄\nExam Papers", use_container_width=True):
            st.session_state.page = "exam"
    with col3:
        if st.button("🌙\nRamzan Special", use_container_width=True):
            st.session_state.page = "ramzan_special"
    with col4:
        if st.button("🧠\nAptitude Test", use_container_width=True):
            st.session_state.page = "quiz"
    with col5:
        if st.button("🕌\nIslamic Tranquility", use_container_width=True):
            st.session_state.page = "islamic"
    with col6:
        if st.button("📝\nB.Com MCQs", use_container_width=True):
            st.session_state.page = "mcq_bank"


# ── RAMZAN SPECIAL ───────────────────────────────────────
elif st.session_state.page == "ramzan_special":
    back_button(key="ramzan_back")
    page_header("🌙", "Ramzan Special", "Curated recipes for the holy month")

    try:
        with open("app1.py", "r", encoding="utf-8") as f:
            lines = f.readlines()
        cleaned_code = "".join([
            line for line in lines
            if "st.set_page_config" not in line and "import streamlit" not in line
        ])
        exec(cleaned_code)
    except FileNotFoundError:
        st.error("⚠️ 'app1.py' not found. Please upload it to the project directory.")
    except Exception as e:
        st.error(f"❌ Could not load Ramzan Special: {e}")


# ── IMAGE TO PDF ─────────────────────────────────────────
elif st.session_state.page == "convert":
    back_button(key="convert_back")
    page_header("🖼️", "Image to PDF", "Upload images and convert them into a single PDF")

    images = st.file_uploader(
        "Drop your images here",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if images:
        st.markdown(f"<p style='color:#64FFDA;font-size:13px;'>✓ {len(images)} image(s) ready</p>", unsafe_allow_html=True)
        pdf = FPDF()
        for img in images:
            image = Image.open(img).convert("RGB")
            temp_path = f"temp_{img.name}"
            image.save(temp_path)
            pdf.add_page()
            pdf.image(temp_path, x=10, y=10, w=190)
            os.remove(temp_path)
        pdf.output("images_to_pdf.pdf")
        with open("images_to_pdf.pdf", "rb") as f:
            st.download_button("⬇️ Download PDF", f, file_name="images_to_pdf.pdf", use_container_width=True)


# ── EXAM PAPERS ──────────────────────────────────────────
elif st.session_state.page == "exam":
    back_button(key="exam_back")
    page_header("📄", "Past Exam Papers", "Browse resources by subject")

    subjects = ["Accounts", "Marketing 3", "Marketing 2", "Auditing", "Economics", "Business Framework"]
    cols = st.columns(3, gap="medium")
    for i, subject in enumerate(subjects):
        with cols[i % 3]:
            if st.button(f"📁 {subject}", use_container_width=True):
                st.session_state.selected_subject = subject

    if "selected_subject" in st.session_state:
        st.markdown(f"<h3 style='margin-top:28px;'>✨ {st.session_state.selected_subject}</h3>", unsafe_allow_html=True)
        # File listing logic here...


# ── APTITUDE TEST ─────────────────────────────────────────
elif st.session_state.page == "quiz":
    back_button(key="quiz_back")
    page_header("🧠", "Aptitude Challenge", "Test your knowledge and skills")
    # Quiz logic here...


# ── ISLAMIC TRANQUILITY ───────────────────────────────────
elif st.session_state.page == "islamic":
    back_button(key="islamic_back")
    page_header("🕌", "Islamic Tranquility", "A moment of peace and reflection")

    try:
        with open("islammmm.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        import streamlit.components.v1 as components
        components.html(html_content, height=800, scrolling=True)
    except FileNotFoundError:
        st.error("⚠️ 'islammmm.html' not found.")


# ── MCQ BANK ─────────────────────────────────────────────
elif st.session_state.page == "mcq_bank":
    back_button(key="mcq_back")
    page_header("📝", "B.Com MCQs", "Practice multiple choice questions")

    try:
        with open("mcq.html", "r", encoding="utf-8") as f:
            mcq_html = f.read()
        import streamlit.components.v1 as components
        components.html(mcq_html, height=800, scrolling=True)
    except FileNotFoundError:
        st.error("⚠️ 'mcq.html' not found.")


# ── FOOTER ───────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
    📧 <a href="mailto:{EMAIL}">{EMAIL}</a>
</div>
""", unsafe_allow_html=True)
