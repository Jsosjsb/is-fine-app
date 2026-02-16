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

# Hide Streamlit header/footer
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================= DUBAI STYLE CSS =================
st.markdown("""
<style>
body {
    background: #F4F6F9;
    font-family: 'Segoe UI', sans-serif;
}

.header {
    text-align: center;
    margin-top: 40px;
    margin-bottom: 40px;
}

.header h1 {
    font-size: 42px;
    font-weight: 700;
    color: #1C6E8C;
}

.header p {
    font-size: 16px;
    color: #555;
    margin-top: 8px;
}

.card-container {
    max-width: 900px;
    margin: auto;
}

.email {
    text-align: center;
    margin-top: 60px;
    font-size: 15px;
    color: #1C6E8C;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ================= HOME =================
if st.session_state.page == "home":

    st.markdown(f"""
    <div class="header">
        <h1>{APP_NAME}</h1>
        <p>Created by Bilal Shaikh</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🖼 Image to PDF", use_container_width=True):
            st.session_state.page = "convert"

    with col2:
        if st.button("📄 Past Exam Papers", use_container_width=True):
            st.session_state.page = "exam"

    with col3:
        if st.button("📊 Analytics Dashboard", use_container_width=True):
            st.session_state.page = "analytics"

# ================= IMAGE TO PDF =================
elif st.session_state.page == "convert":

    st.header("🖼 Image to PDF Converter")

    images = st.file_uploader(
        "Upload JPG / PNG images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if images:
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
            st.download_button(
                "⬇️ Download PDF",
                f,
                file_name="images_to_pdf.pdf",
                use_container_width=True
            )

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"

# ================= EXAM PAPERS =================
elif st.session_state.page == "exam":

    st.header("📄 Past Exam Papers")
    
    # These names must match your folder names exactly
    subjects = ["Accounts", "Marketing 3", "Marketing 2", "Auditing", "Economics", "Business Framework"]
    
    # Step 1: Create the Subject Boxes
    cols = st.columns(3)
    for i, subject in enumerate(subjects):
        with cols[i % 3]:
            # If user clicks a subject box
            if st.button(f"📁 {subject}", use_container_width=True):
                st.session_state.selected_subject = subject

    st.divider()

    # Step 2: Show the PDFs for the selected subject
    if "selected_subject" in st.session_state:
        subject = st.session_state.selected_subject
        st.subheader(f"Results for: {subject}")
        
        subject_path = os.path.join(EXAM_FOLDER, subject)
        
        # Check if folder exists
        if os.path.exists(subject_path):
            files = [f for f in os.listdir(subject_path) if f.lower().endswith(".pdf")]
            
            if files:
                # Loop through every PDF found in that folder
                for pdf_name in files:
                    with st.expander(f"📄 View: {pdf_name}"):
                        file_path = os.path.join(subject_path, pdf_name)
                        with open(file_path, "rb") as f:
                            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                        
                        # Embed the PDF viewer
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)
            else:
                st.info(f"No PDF files found in the {subject} folder.")
        else:
            st.error(f"Folder '{subject}' not found. Create it inside 'exam_papers' on GitHub.")

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        if "selected_subject" in st.session_state:
            del st.session_state.selected_subject

# ================= ANALYTICS =================
elif st.session_state.page == "analytics":

    st.header("📊 Analytics Dashboard")

    total_pdfs = len([f for f in os.listdir(EXAM_FOLDER) if f.endswith(".pdf")])

    st.metric("Total Uploaded PDFs", total_pdfs)
    st.metric("App Version", "1.0")

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"

# ================= EMAIL =================
st.markdown(f"""
<div class="email">
📧 Contact: {EMAIL}
</div>
""", unsafe_allow_html=True)


