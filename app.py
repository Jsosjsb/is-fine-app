import streamlit as st
from PIL import Image
from fpdf import FPDF
import os

st.markdown("""
<link rel="manifest" href="data:application/json,{
  &quot;name&quot;:&quot;is_fine app&quot;,
  &quot;short_name&quot;:&quot;is_fine&quot;,
  &quot;start_url&quot;:&quot;/&quot;,
  &quot;display&quot;:&quot;standalone&quot;,
  &quot;background_color&quot;:&quot;#FAFAFA&quot;,
  &quot;theme_color&quot;:&quot;#5A0F2E&quot;
}">
""", unsafe_allow_html=True)

# ================= CONFIG =================
APP_NAME = "is_fine app"
ADMIN_PASSWORD = "admin123"
EXAM_FOLDER = "exam_papers"
WHATSAPP_NUMBER = "919209499163"

os.makedirs(EXAM_FOLDER, exist_ok=True)

# ================= SESSION =================
if "page" not in st.session_state:
    st.session_state.page = "home"
if "admin" not in st.session_state:
    st.session_state.admin = False

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title=APP_NAME,
    page_icon="💎",
    layout="centered"
)

# ================= LIGHT LUXURY CSS =================
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #FAFAFA, #F1F1F1);
    color: #222;
}

/* HEADER */
.main-title {
    text-align: center;
    font-size: clamp(30px, 5vw, 46px);
    font-weight: 800;
    color: #5A0F2E;
}
.subtitle {
    text-align: center;
    color: #8A6A4F;
    margin-bottom: 30px;
}

/* BUTTONS */
button {
    border: 2px solid #D4AF37 !important;
    background-color: white !important;
    color: #5A0F2E !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}
button:hover {
    background-color: #FFF6D8 !important;
}

/* CARD */
.pdf-card {
    height: 170px;
    border-radius: 16px;
    padding: 18px;
    background: white;
    border: 2px solid #D4AF37;
    color: #5A0F2E;
    box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-weight: 600;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.pdf-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 28px rgba(212,175,55,0.4);
}

/* FLOAT HELP */
.help-float {
    position: fixed;
    bottom: 14px;
    left: 14px;
    background: white;
    border: 2px solid #D4AF37;
    color: #5A0F2E;
    padding: 8px 14px;
    border-radius: 30px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
}

/* FOOTER RIGHT */
.footer-right {
    position: fixed;
    bottom: 14px;
    right: 14px;
    font-size: 12px;
    color: #8A6A4F;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown(f'<div class="main-title">{APP_NAME}</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Premium • Light • Professional Utility</div>', unsafe_allow_html=True)

# ================= HOME =================
if st.session_state.page == "home":

    if st.button("📄 Convert Images to PDF", use_container_width=True):
        st.session_state.page = "convert"

    if st.button("📘 Exam Papers", use_container_width=True):
        st.session_state.page = "exam"

    if st.button("🔐 Admin Upload", use_container_width=True):
        st.session_state.page = "admin"

# ================= IMAGE TO PDF =================
elif st.session_state.page == "convert":

    st.header("📄 Image to PDF Converter")

    images = st.file_uploader(
        "Upload JPG / PNG images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if images:
        pdf = FPDF()
        for img in images:
            image = Image.open(img).convert("RGB")
            temp = f"temp_{img.name}"
            image.save(temp)
            pdf.add_page()
            pdf.image(temp, x=10, y=10, w=190)
            os.remove(temp)

        pdf.output("images_to_pdf.pdf")
        with open("images_to_pdf.pdf", "rb") as f:
            st.download_button("⬇️ Download PDF", f, "images_to_pdf.pdf", use_container_width=True)

    if st.button("⬅️ Back"):
        st.session_state.page = "home"

# ================= EXAM PAPERS =================
elif st.session_state.page == "exam":

    st.header("📘 Exam Papers")

    pdfs = [f for f in os.listdir(EXAM_FOLDER) if f.lower().endswith(".pdf")]

    if not pdfs:
        st.info("No exam papers uploaded yet.")
    else:
        cols = st.columns(3)
        for i, pdf in enumerate(pdfs):
            with cols[i % 3]:
                st.markdown(
                    f"""
                    <div class="pdf-card">
                        📄<br>{pdf}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                with open(os.path.join(EXAM_FOLDER, pdf), "rb") as f:
                    st.download_button("⬇️ Download", f, pdf, use_container_width=True)

    if st.button("⬅️ Back"):
        st.session_state.page = "home"

# ================= ADMIN =================
elif st.session_state.page == "admin":

    st.header("🔐 Admin Panel")

    if not st.session_state.admin:
        pwd = st.text_input("Enter admin password", type="password")
        if st.button("Login"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin = True
                st.success("Admin access granted")
            else:
                st.error("Wrong password")
    else:
        upload = st.file_uploader("Upload Exam PDF", type=["pdf"])
        if upload:
            with open(os.path.join(EXAM_FOLDER, upload.name), "wb") as f:
                f.write(upload.read())
            st.success("PDF uploaded successfully")

        if st.button("Logout"):
            st.session_state.admin = False
            st.session_state.page = "home"

    if st.button("⬅️ Back"):
        st.session_state.page = "home"

# ================= HELP =================
elif st.session_state.page == "help":

    st.header("ℹ️ Help & Information")

    st.markdown("""
    **What you can do**
    - Convert images into high-quality PDFs
    - Download exam papers easily
    - Works on mobile & desktop

    **Privacy**
    - Files are processed temporarily
    - No user data stored

    **Contact**
    - WhatsApp: +91 9209499163
    """)

    if st.button("⬅️ Back"):
        st.session_state.page = "home"

# ================= FLOAT HELP + FOOTER =================
st.markdown(
    """
    <div class="help-float" onclick="window.location.search='?page=help'">
        ℹ️ Help
    </div>
    <div class="footer-right">
        Created by Bilal Shaikh
    </div>
    """,
    unsafe_allow_html=True
)
