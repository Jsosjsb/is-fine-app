import streamlit as st
import os

# ================= CONFIG =================
APP_NAME = "IS_FINE"
EMAIL = "adishaikh776@gmail.com"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit default header/footer
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================= ULTRA LUXURY CSS =================
st.markdown("""
<style>

/* BACKGROUND */
body {
    background: linear-gradient(180deg, #000000, #0E0E0E);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* HEADER */
.header-box {
    text-align: center;
    margin-top: 50px;
    margin-bottom: 50px;
}

.header-box h1 {
    font-size: 52px;
    letter-spacing: 4px;
    font-weight: 900;
    background: linear-gradient(90deg, #D4AF37, #FFD700, #B8860B);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.header-sub {
    color: #C5A84B;
    font-size: 15px;
    margin-top: 10px;
}

/* GRID */
.grid-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
    max-width: 700px;
    margin: auto;
}

/* MOBILE STACK */
@media (max-width: 768px) {
    .grid-container {
        grid-template-columns: 1fr;
    }
}

/* GLASS CARD */
.card {
    position: relative;
    aspect-ratio: 1 / 1;
    border-radius: 25px;
    backdrop-filter: blur(12px);
    background: rgba(255,255,255,0.05);
    border: 3px solid transparent;
    background-clip: padding-box;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    transition: 0.4s ease;
    cursor: pointer;
}

/* GOLD GRADIENT BORDER */
.card::before {
    content: "";
    position: absolute;
    inset: 0;
    padding: 3px;
    border-radius: 25px;
    background: linear-gradient(135deg, #FFD700, #D4AF37, #B8860B);
    -webkit-mask:
        linear-gradient(#000 0 0) content-box,
        linear-gradient(#000 0 0);
    -webkit-mask-composite: xor;
            mask-composite: exclude;
}

/* HOVER EFFECT */
.card:hover {
    transform: translateY(-10px) scale(1.05);
    box-shadow: 0 20px 50px rgba(212,175,55,0.5);
}

/* ICON ANIMATION */
.icon {
    font-size: 50px;
    margin-bottom: 15px;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-12px); }
    100% { transform: translateY(0px); }
}

/* TEXT */
.card-title {
    font-size: 18px;
    font-weight: 600;
    color: #FFD700;
}

/* EMAIL */
.email-box {
    text-align: center;
    margin-top: 60px;
    font-size: 15px;
    color: #C5A84B;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown(f"""
<div class="header-box">
    <h1>{APP_NAME}</h1>
    <div class="header-sub">Created by Bilal Shaikh</div>
</div>
""", unsafe_allow_html=True)

# ================= 2x2 SQUARE GRID =================
st.markdown('<div class="grid-container">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    if st.button("🖼 Image to PDF", use_container_width=True):
        st.session_state.page = "convert"

with col2:
    if st.button("📄 Past Exam Papers", use_container_width=True):
        st.session_state.page = "exam"

with col3:
    if st.button("📊 Analytics Dashboard", use_container_width=True):
        st.session_state.page = "analytics"

with col4:
    if st.button("🔐 Secrect File", use_container_width=True):
        st.session_state.page = "admin"

st.markdown('</div>', unsafe_allow_html=True)

# ================= EMAIL =================
st.markdown(f"""
<div class="email-box">
📧 Contact: {EMAIL}
</div>
""", unsafe_allow_html=True)


