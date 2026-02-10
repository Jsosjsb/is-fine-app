import streamlit as st
from PIL import Image
from fpdf import FPDF
import os

# ================= CONFIG =================
APP_NAME = "IS_FINE APP"
EXAM_FOLDER = "exam_papers"
WHATSAPP_LINK = "https://wa.me/918999932770"

os.makedirs(EXAM_FOLDER, exist_ok=True)

# ================= SESSION =================
if "page" not in st.session_state:
    st.session_state.page = "home"

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title=APP_NAME,
    page_icon="💎",
    layout="centered"
)

# ================= LIGHT GOLD THEME =================
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #FAFAFA, #F1F1F1);
    color: #222;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #5A0F2E;
}

.created {
    text-align: center;
    font-size: 13px;
    color: #8A6A4F;
    margin-bottom: 30px;
}

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
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown(f'<div class="main-title">{APP_NAME}</div>', unsafe_allow_html=True)
st.markdown('<div class="created">Created by Bilal Shaikh</div>', unsafe_allow_html=True)

# ================= HOME =================
if st.session_state.page == "home":

    if st.button("📄 Convert Images to PDF", use_container_width=True):
        st.session_state.page = "convert"

    if st.button("📘 Exam Papers", use_container_width=True):
        st.session_state.page = "exam"

    if st.button("➕ ADD NEW", use_container_width=True):
        st.markdown(f"[Open WhatsApp]({WHATSAPP_LINK})", unsafe_allow_html=True)

# ================= IMAGE TO PDF WITH ROTATION =================
elif st.session_state.page == "convert":

    st.header("📄 Image to PDF Converter")

    images = st.file_uploader(
        "Upload images (JPG / PNG)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    rotation = st.selectbox(
        "Rotate pages",
        options=[0, 90, 180, 270],
        format_func=lambda x: f"{x}°"
    )

    if images:
        pdf = FPDF()

        for img in images:
            image = Image.open(img).convert("RGB")

            if rotation != 0:
                image = image.rotate(-rotation, expand=True)

            temp = f"temp_{img.name}"
            image.save(temp)

            pdf.add_page()
            pdf.image(temp, x=10, y=10, w=190)
            os.remove(temp)

        pdf.output("images_to_pdf.pdf")

        with open("images_to_pdf.pdf", "rb") as f:
            st.download_button(
                "⬇️ Download PDF",
                f,
                file_name="images_to_pdf.pdf",
                use_container_width=True
            )

    if st.button("⬅️ Back"):
        st.session_state.page = "home"

# ================= EXAM PAPERS =================
elif st.session_state.page == "exam":

    st.header("📘 Exam Papers")

    pdfs = [f for f in os.listdir(EXAM_FOLDER) if f.lower().endswith(".pdf")]

    if not pdfs:
        st.info("No exam papers available.")
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
                    st.download_button(
                        "⬇️ Download",
                        f,
                        pdf,
                        use_container_width=True
                    )

    if st.button("⬅️ Back"):
        st.session_state.page = "home"
