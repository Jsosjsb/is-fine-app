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

# ================= LUXURY DUBAI STYLE CSS =================
st.markdown("""
<style>
/* Deep Navy & Gold Theme */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0A192F 0%, #112240 100%);
}

.header {
    text-align: center;
    padding: 30px 10px;
}

.header h1 {
    font-size: 36px;
    font-weight: 800;
    color: #CCD6F6;
    letter-spacing: 2px;
    margin-bottom: 0px;
}

.header p {
    font-size: 14px;
    color: #64FFDA;
    text-transform: uppercase;
    letter-spacing: 3px;
}

div.stButton > button {
    background: rgba(255, 255, 255, 0.05);
    color: #64FFDA;
    border: 1px solid #64FFDA;
    padding: 20px;
    border-radius: 12px;
    transition: all 0.3s ease;
    font-size: 18px;
    font-weight: 600;
    height: 100px;
}

div.stButton > button:hover {
    background: #64FFDA;
    color: #0A192F;
    box-shadow: 0 0 20px rgba(100, 255, 218, 0.4);
    transform: translateY(-5px);
}

.email {
    text-align: center;
    padding: 20px;
    color: #8892B0;
    font-size: 12px;
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
    col4, col5, col6 = st.columns(3)

    with col1:
        if st.button("🖼 Image to PDF", use_container_width=True):
            st.session_state.page = "convert"
    with col2:
        if st.button("📄 Exam Papers", use_container_width=True):
            st.session_state.page = "exam"
    with col3:
        # Changed to internal page routing
        if st.button("🌙 Ramzan Spc", use_container_width=True):
            st.session_state.page = "ramzan_special"
    with col4:
        if st.button("🧠 Aptitude Test", use_container_width=True):
            st.session_state.page = "quiz"
    with col5:
        if st.button("🕌 Islamic Tranquility", use_container_width=True):
            st.session_state.page = "islamic"
    with col6:
        if st.button("📝 B.Com MCQs", use_container_width=True):
            st.session_state.page = "mcq_bank"

# ================= RAMZAN SPECIAL (Integrated) =================
elif st.session_state.page == "ramzan_special":
    # 1. Internal Navigation
    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown('<div class="header"><h1>🌙 Ramzan Special Recipes</h1></div>', unsafe_allow_html=True)

    # 2. Add the Recipe Logic directly here
    @st.cache_data
    def load_ramzan_data():
        try:
            # Ensure this file is uploaded to your GitHub repository
            df = pd.read_csv("mealdb_dataset_with_flag.csv")
            df.columns = df.columns.str.lower().str.strip()
            return df
        except FileNotFoundError:
            return None

    recipe_df = load_ramzan_data()

    if recipe_df is not None:
        col1, col2 = st.columns(2)
        with col1:
            veg_type = st.selectbox("Dietary Preference", sorted(recipe_df['veg_flag'].unique()))
        
        filtered = recipe_df[recipe_df['veg_flag'] == veg_type]
        
        with col2:
            dish_choice = st.selectbox("Select Recipe", sorted(filtered['strmeal'].unique()))

        if st.button("📖 View Recipe Details", use_container_width=True):
            recipe_row = filtered[filtered['strmeal'] == dish_choice].iloc[0]
            
            st.markdown(f"## {recipe_row['strmeal']}")
            st.image(recipe_row['strmealthumb'], width=400)
            
            st.subheader("🥘 Ingredients")
            # Logic to display ingredients (stringredient1 to 20)
            for i in range(1, 21):
                ing = recipe_row.get(f'stringredient{i}', '')
                meas = recipe_row.get(f'strmeasure{i}', '')
                if str(ing).strip() and str(ing) != 'nan':
                    st.write(f"- {meas} {ing}")

            st.subheader("👨‍🍳 Instructions")
            st.write(recipe_row['strinstructions'])
    else:
        st.error("Error: 'mealdb_dataset_with_flag.csv' not found. Please upload it to GitHub.")

# ================= IMAGE TO PDF =================
elif st.session_state.page == "convert":
    st.header("🖼 Image to PDF Converter")
    images = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
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
            st.download_button("⬇️ Download PDF", f, file_name="images_to_pdf.pdf", use_container_width=True)
    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"

# ================= EXAM PAPERS =================
elif st.session_state.page == "exam":
    st.markdown('<div class="header"><h1>📄 Past Exam Papers</h1></div>', unsafe_allow_html=True)
    subjects = ["Accounts", "Marketing 3", "Marketing 2", "Auditing", "Economics", "Business Framework"]
    cols = st.columns(3)
    for i, subject in enumerate(subjects):
        with cols[i % 3]:
            if st.button(f"📁 {subject}", use_container_width=True):
                st.session_state.selected_subject = subject
    if "selected_subject" in st.session_state:
        st.subheader(f"✨ {st.session_state.selected_subject} Resources")
        # (File listing logic here...)
    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"

# ================= TEST YOURSELF (QUIZ) =================
elif st.session_state.page == "quiz":
    st.markdown('<div class="header"><h1>🧠 Aptitude Challenge</h1></div>', unsafe_allow_html=True)
    # (Quiz questions logic here...)
    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"

# ================= ISLAMIC TRANQUILITY =================
elif st.session_state.page == "islamic":
    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    with open("islammmm.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    import streamlit.components.v1 as components
    components.html(html_content, height=800, scrolling=True)

# ================= MCQ BANK =================
elif st.session_state.page == "mcq_bank":
    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    with open("mcq.html", "r", encoding="utf-8") as f:
        mcq_html = f.read()
    import streamlit.components.v1 as components
    components.html(mcq_html, height=800, scrolling=True)

# ================= FOOTER =================
st.markdown(f'<div class="email">📧 Contact: {EMAIL}</div>', unsafe_allow_html=True)


