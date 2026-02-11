import streamlit as st

# ================= CONFIG =================
APP_NAME = "IS_FINE APP"

st.set_page_config(page_title=APP_NAME, layout="wide")

# Hide Streamlit default UI
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ================= EXACT DESIGN CSS =================
st.markdown("""
<style>

body {
    background: #F3F3F3;
    font-family: 'Segoe UI', sans-serif;
}

/* HEADER BANNER */
.banner {
    background: linear-gradient(90deg, #F2ECE4, #E7DED3);
    border: 3px solid #C6A46C;
    border-radius: 25px;
    padding: 40px;
    margin-top: 30px;
    position: relative;
}

/* TITLE */
.banner-title {
    font-size: 44px;
    font-weight: 700;
    color: #5C0632;
}

.banner-sub {
    font-size: 22px;
    color: #7A4C4C;
    margin-top: 8px;
}

/* SEARCH BOX */
.search-box {
    position: absolute;
    right: 40px;
    top: 40px;
    background: white;
    border-radius: 40px;
    padding: 10px 25px;
    border: 2px solid #C6A46C;
    font-size: 16px;
    color: #777;
}

/* GOLD WAVE LINE */
.wave {
    height: 4px;
    background: linear-gradient(90deg, #C6A46C, #E4C58C);
    margin-top: 25px;
    border-radius: 2px;
}

/* CARD CONTAINER */
.card-row {
    display: flex;
    gap: 30px;
    margin-top: 50px;
}

/* CARD STYLE */
.card {
    flex: 1;
    border-radius: 25px;
    padding: 50px 30px;
    text-align: center;
    border: 2px solid #C6A46C;
    background: #ECECEC;
    transition: 0.3s;
    cursor: pointer;
}

/* ACTIVE CARD */
.card-active {
    background: linear-gradient(135deg, #7C2636, #5C0632);
    color: white;
    border: none;
}

.card-title {
    margin-top: 15px;
    font-size: 22px;
    font-weight: 600;
}

.card:hover {
    transform: translateY(-8px);
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="banner">
    <div class="banner-title">IS_FINE APP</div>
    <div class="banner-sub">Manage your files easily</div>
    <div class="search-box">Search...</div>
    <div class="wave"></div>
</div>
""", unsafe_allow_html=True)

# ================= CARDS =================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card card-active">
        <div style="font-size:40px;">🖼 ➜ 📄</div>
        <div class="card-title">Image to PDF</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div style="font-size:40px;">📑</div>
        <div class="card-title">Past Exam Papers</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <div style="font-size:40px;">🔒</div>
        <div class="card-title">Secret Files</div>
    </div>
    """, unsafe_allow_html=True)
