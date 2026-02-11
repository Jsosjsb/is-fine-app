import streamlit as st
import os
import time
import base64
from fpdf import FPDF
from PIL import Image
from PyPDF2 import PdfReader

# ================= CONFIG =================
APP_NAME = "IS_FINE"
ADMIN_PASSWORD = "admin123"
EXAM_FOLDER = "exam_papers"
WHATSAPP_LINK = "https://wa.me/918999932770"

os.makedirs(EXAM_FOLDER, exist_ok=True)

# ================= SESSION =================
if "page" not in st.session_state:
    st.session_state.page = "home"
if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False
if "analytics" not in st.session_state:
    st.session_state.analytics = {"downloads": 0}

# ================= PAGE CONFIG =================
st.set_page_config(page_title=APP_NAME, page_icon="💎", layout="wide")

# ================= SPLASH ICON ANIMATION =================
if "splash" not in st.session_state:
    st.session_state.splash = True

if st.session_state.splash:
    st.markdown("""
    <div style="text-align:center; margin-top:200px;">
        <div style="font-size:70px; animation:spin 2s linear infinite;">💎</div>
        <h1>IS_FINE</h1>
    </div>
    <style>
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.splash = False
    st.rerun()

# ================= GLOBAL STYLE =================
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #0D0F1A, #12162B);
    color: white;
    overflow-x: hidden;
}

.header {
    text-align:center;
    margin-bottom: 20px;
    animation: slideDown 0.6s ease;
}

@keyframes slideDown {
    from {opacity:0; transform: translateY(-40px);}
    to {opacity:1; transform: translateY(0);}
}

.page-transition {
    animation: slidePage 0.5s ease;
}

@keyframes slidePage {
    from {opacity:0; transform: translateX(40px);}
    to {opacity:1; transform: translateX(0);}
}

.bottom-nav {
    position: fixed;
    bottom: 0;
    width: 100%;
    background: #111428;
    display: flex;
    justify-content: space-around;
    padding: 12px;
    border-top: 2px solid #D4AF37;
}

.nav-btn {
    color: #D4AF37;
    font-weight: bold;
    text-decoration: none;
    transition: 0.3s ease;
}

.nav-btn:hover {
    color: white;
    transform: scale(1.1);
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown(f"""
<div class="header">
<h1>{APP_NAME}</h1>
<p>Created by Bilal Shaikh App</p>
</div>
""", unsafe_allow_html=True)

# ================= LOADING SPINNER =================
def loading():
    with st.spinner("Loading..."):
        time.sleep(0.6)

# ================= HOME =================
if st.session_state.page == "home":
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)

    if st.button("🖼 Image to PDF"):
        loading()
        st.session_state.page = "convert"

    if st.button("📄 Past Exam Papers"):
        loading()
        st.session_state.page = "exam"

    if st.button("📊 Analytics Dashboard"):
        loading()
        st.session_state.page = "analytics"

    if st.button("🔐 Admin Panel"):
        loading()
        st.session_state.page = "admin"

    if st.button("➕ Add New"):
        st.markdown(f"[Open WhatsApp]({WHATSAPP_LINK})")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= IMAGE TO PDF =================
elif st.session_state.page == "convert":
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)

    images = st.file_uploader("Upload Images", type=["jpg","png"], accept_multiple_files=True)

    if images:
        pdf = FPDF()
        for img in images:
            image = Image.open(img).convert("RGB")
            temp = f"temp_{img.name}"
            image.save(temp)
            pdf.add_page()
            pdf.image(temp, x=10, y=10, w=190)
            os.remove(temp)

        pdf.output("output.pdf")

        with open("output.pdf","rb") as f:
            st.download_button("Download PDF", f, "output.pdf")

    if st.button("⬅ Back"):
        st.session_state.page = "home"

    st.markdown('</div>', unsafe_allow_html=True)

# ================= EXAM PAPERS =================
elif st.session_state.page == "exam":
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)

    pdfs = [f for f in os.listdir(EXAM_FOLDER) if f.lower().endswith(".pdf")]

    search = st.text_input("🔍 Search PDF")

    for pdf in pdfs:
        if search.lower() in pdf.lower():
            path = os.path.join(EXAM_FOLDER, pdf)

            with open(path,"rb") as f:
                pdf_bytes = f.read()

            st.subheader(pdf)
            st.download_button("Download", pdf_bytes, pdf)

            st.session_state.analytics["downloads"] += 1

            # SEARCH INSIDE PDF
            reader = PdfReader(path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""

            keyword = st.text_input(f"Search inside {pdf}", key=pdf)
            if keyword and keyword.lower() in text.lower():
                st.success("Keyword Found!")

            if st.session_state.admin_logged:
                if st.button("Delete", key="del_"+pdf):
                    os.remove(path)
                    st.rerun()

    if st.button("⬅ Back"):
        st.session_state.page = "home"

    st.markdown('</div>', unsafe_allow_html=True)

# ================= ANALYTICS =================
elif st.session_state.page == "analytics":
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)

    st.header("📊 Analytics Dashboard")
    st.metric("Total Downloads", st.session_state.analytics["downloads"])
    st.metric("Total PDFs", len(os.listdir(EXAM_FOLDER)))

    if st.button("⬅ Back"):
        st.session_state.page = "home"

    st.markdown('</div>', unsafe_allow_html=True)

# ================= ADMIN =================
elif st.session_state.page == "admin":

    if not st.session_state.admin_logged:
        pwd = st.text_input("Enter Password", type="password")
        if st.button("Login"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin_logged = True
                st.rerun()
            else:
                st.error("Wrong Password")
    else:
        uploaded = st.file_uploader("Upload PDF", type=["pdf"])
        if uploaded:
            with open(os.path.join(EXAM_FOLDER, uploaded.name),"wb") as f:
                f.write(uploaded.read())
            st.success("Uploaded")
            st.rerun()

        if st.button("Logout"):
            st.session_state.admin_logged = False
            st.session_state.page = "home"
            st.rerun()

    if st.button("⬅ Back"):
        st.session_state.page = "home"

# ================= REAL BOTTOM NAV =================
st.markdown("""
<div class="bottom-nav">
    <a class="nav-btn" href="?page=home">Home</a>
    <a class="nav-btn" href="?page=exam">Papers</a>
    <a class="nav-btn" href="?page=analytics">Analytics</a>
    <a class="nav-btn" href="?page=admin">Admin</a>
</div>
""", unsafe_allow_html=True)
