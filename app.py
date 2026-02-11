import streamlit as st

APP_NAME = "IS_FINE"
EMAIL = "adishaikh776@gmail.com"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide default Streamlit header/footer
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

/* Background */
body {
    background: #F4F6F9;
    font-family: 'Segoe UI', sans-serif;
}

/* Header */
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

/* Grid Layout */
.card-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 25px;
    max-width: 900px;
    margin: auto;
}

/* Mobile Stack */
@media (max-width: 768px) {
    .card-container {
        grid-template-columns: 1fr;
    }
}

/* Card Style */
.card {
    background: white;
    border: 2px solid #1C6E8C;
    border-radius: 18px;
    padding: 30px;
    text-align: center;
    transition: 0.3s ease;
    cursor: pointer;
}

.card:hover {
    background: #EAF3F7;
    transform: translateY(-6px);
}

/* Icon */
.icon {
    font-size: 42px;
    margin-bottom: 15px;
    color: #1C6E8C;
}

/* Text */
.card-title {
    font-size: 18px;
    font-weight: 600;
    color: #1C6E8C;
}

/* Email */
.email {
    text-align: center;
    margin-top: 60px;
    font-size: 15px;
    color: #1C6E8C;
    font-weight: 500;
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

# ================= CARD GRID =================
st.markdown('<div class="card-container">', unsafe_allow_html=True)

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

st.markdown('</div>', unsafe_allow_html=True)

# ================= EMAIL =================
st.markdown(f"""
<div class="email">
📧 Contact: {EMAIL}
</div>
""", unsafe_allow_html=True)
