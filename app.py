import streamlit as st
import os
from PIL import Image
from fpdf import FPDF

# ================= CONFIG =================
APP_NAME = "IS_FINE APP"
ADMIN_PASSWORD = "admin123"
EXAM_FOLDER = "exam_papers"
WHATSAPP_LINK = "https://wa.me/918999932770"

os.makedirs(EXAM_FOLDER, exist_ok=True)

# ================= SESSION =================
if "page" not in st.session_state:
    st.session_state.page = "home"
if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

# ================= PAGE CONFIG =================
st.set_page_config(page_title=APP_NAME, page_icon="💎", layout="wide")

# ================= STYLE =================
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #F8F5F2, #EFE9E3);
    color: #3A0F1D;
}

.header {
    background: linear-gradient(90deg, #5A0F2E, #7A1B3F);
    padding: 25px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
}

button {
    border-radius: 16px !important;
    border: 2px solid #D4AF37 !important;
    background: white !important;
    color: #5A0F2E !important;
    font-weight: 600 !important;
    padding: 15px !important;
}

.pdf-card {
    background: white;
    border: 2px solid #D4AF37;
    border-radius: 16px;
    padding: 15px;
    text-align: center;
    margin-bottom: 10px;
}

.footer {
    text-align: center;
    margin-top: 40px;
    font-size: 14px;
    color: #7A1B3F;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown(f"""
<div class="header">
    <h1>{APP_NAME}</h1>
    <p>Professional File Manager</p>
</div>
""", unsafe_allow_html=True)

# ================= HOME =================
if st.session_state.page == "home":

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🖼️ Image to PDF", use_container_width=True):
            st.session_state.page = "convert"

        if st.button("📄 Past Exam Papers", use_container_width=True):
            st.session_state.page = "exam"

    with col2:
        if st.button("🔐 Admin Panel", use_container_width=True):
            st.session_state.page = "admin"

        if st.button("➕ ADD NEW", use_container_width=True):
            st.markdown(f"[Open WhatsApp]({WHATSAPP_LINK})")

# ================= IMAGE TO PDF =================
elif st.session_state.page == "convert":

    st.header("🖼️ Image to PDF Converter")

    images = st.file_uploader(
        "Upload images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    rotation = st.selectbox("Rotate Pages", [0, 90, 180, 270])

    if images:
        pdf = FPDF()

        for img in images:
            image = Image.open(img).convert("RGB")

            if rotation != 0:
                image = image.rotate(-rotation, expand=True)

            temp_path = f"temp_{img.name}"
            image.save(temp_path)

            pdf.add_page()
            pdf.image(temp_path, x=10, y=10, w=190)
            os.remove(temp_path)

        pdf.output("images_to_pdf.pdf")

        with open("images_to_pdf.pdf", "rb") as f:
            st.download_button("⬇️ Download PDF", f, "images_to_pdf.pdf", use_container_width=True)

    if st.button("⬅️ Back"):
        st.session_state.page = "home"

# ================= EXAM PAPERS =================
elif st.session_state.page == "exam":

    st.header("📄 Past Exam Papers")

    # AUTO DETECT PDFs
    pdfs = [f for f in os.listdir(EXAM_FOLDER) if f.lower().endswith(".pdf")]

    if not pdfs:
        st.info("No exam papers available.")
    else:
        for pdf in pdfs:
            st.markdown(f'<div class="pdf-card">{pdf}</div>', unsafe_allow_html=True)

            col1, col2 = st.columns([3, 1])

            with col1:
                with open(os.path.join(EXAM_FOLDER, pdf), "rb") as f:
                    st.download_button(
                        "⬇️ Download",
                        f,
                        pdf,
                        key=f"download_{pdf}",
                        use_container_width=True
                    )

            with col2:
                if st.session_state.admin_logged:
                    if st.button("🗑 Delete", key=f"delete_{pdf}"):
                        os.remove(os.path.join(EXAM_FOLDER, pdf))
                        st.success(f"{pdf} deleted")
                        st.rerun()

    if st.button("⬅️ Back"):
        st.session_state.page = "home"

# ================= ADMIN PANEL =================
elif st.session_state.page == "admin":

    st.header("🔐 Admin Panel")

    if not st.session_state.admin_logged:
        password = st.text_input("Enter Admin Password", type="password")

        if st.button("Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_logged = True
                st.success("Admin Logged In")
                st.rerun()
            else:
                st.error("Wrong Password")

    else:
        st.success("Admin Mode Active")

        uploaded_pdf = st.file_uploader("Upload New Exam PDF", type=["pdf"])

        if uploaded_pdf:
            save_path = os.path.join(EXAM_FOLDER, uploaded_pdf.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_pdf.read())
            st.success("PDF Uploaded Successfully")
            st.rerun()

        if st.button("Logout"):
            st.session_state.admin_logged = False
            st.session_state.page = "home"
            st.rerun()

        if st.button("⬅️ Back"):
            st.session_state.page = "home"

# ================= FOOTER =================
st.markdown("""
<div class="footer">
    Created by Bilal Shaikh
</div>
""", unsafe_allow_html=True)
