import streamlit as st
import os

# ================= CONFIG =================
APP_NAME = "IS_FINE"
EMAIL = "adishaikh776@gmail.com"

st.set_page_config(page_title=APP_NAME, layout="wide")

# Hide Streamlit default
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ================= DUBAI PORTAL CSS =================
st.markdown("""
<style>

body {
    background: #F5F7FA;
    font-family: 'Segoe UI', sans-serif;
}

/* HEADER BAR */
.topbar {
    background: #5C0632;
    padding: 15px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: white;
}

.logo {
    font-size: 22px;
    font-weight: bold;
}

.lang-toggle {
    background: white;
    color: #5C0632;
    padding: 6px 15px;
    border-radius: 20px;
    font-weight: 600;
}

/* PAGE TITLE */
.header {
    text-align: center;
    margin: 40px 0;
}

.header h1 {
    font-size: 40px;
    color: #5C0632;
}

.header p {
    color: #555;
}

/* GRID */
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 25px;
    max-width: 1000px;
    margin: auto;
}

@media(max-width: 768px){
    .grid {
        grid-template-columns: 1fr;
    }
}

/* CARD */
.card {
    background: white;
    border-radius: 18px;
    padding: 30px;
    text-align: center;
    position: relative;
    cursor: pointer;
    overflow: hidden;
}

/* LIVE BORDER ANIMATION */
.card::before {
    content: "";
    position: absolute;
    inset: 0;
    padding: 3px;
    border-radius: 18px;
    background: linear-gradient(90deg, #5C0632, #9E2956, #5C0632);
    background-size: 300% 300%;
    animation: borderMove 3s linear infinite;
    -webkit-mask:
        linear-gradient(#000 0 0) content-box,
        linear-gradient(#000 0 0);
    -webkit-mask-composite: xor;
            mask-composite: exclude;
}

@keyframes borderMove {
    0% {background-position: 0% 50%;}
    100% {background-position: 100% 50%;}
}

.card:hover {
    background: #FAF1F6;
    transform: translateY(-6px);
    transition: 0.3s;
}

.icon {
    font-size: 38px;
    margin-bottom: 10px;
    color: #5C0632;
}

.title {
    font-weight: 600;
    font-size: 16px;
    color: #5C0632;
}

/* EMAIL */
.email {
    text-align: center;
    margin: 60px 0 20px;
    color: #5C0632;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="topbar">
    <div class="logo">🇦🇪 Dubai Portal - IS_FINE</div>
    <div class="lang-toggle">EN | AR</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="header">
    <h1>{APP_NAME}</h1>
    <p>Created by Bilal Shaikh App</p>
</div>
""", unsafe_allow_html=True)

# ================= GRID =================
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    if st.button("🖼 Image to PDF", use_container_width=True):
        st.write("Image to PDF Page")

with col2:
    if st.button("📄 Past Exam Papers", use_container_width=True):
        st.write("Exam Papers Page")

with col3:
    with st.expander("📊 Analytics Dashboard"):
        st.metric("Visitors", "1,245")
        st.metric("Downloads", "320")

with col4:
    if st.button("🔐 Secret File", use_container_width=True):
        st.write("Secret File Section")

with col5:
    if st.button("🧠 Test Yourself", use_container_width=True):
        st.session_state.page = "test"

with col6:
    st.empty()

# ================= TEST YOURSELF SECTION =================
if "page" in st.session_state and st.session_state.page == "test":

    st.subheader("🧠 Aptitude Test")

    questions = [
        ("2 + 2 = ?", ["3","4","5"], "4"),
        ("5 x 3 = ?", ["15","10","20"], "15"),
        ("Square root of 16?", ["2","4","8"], "4"),
        ("10 - 7 = ?", ["1","2","3"], "3"),
        ("6 / 2 = ?", ["2","3","4"], "3"),
        ("9 + 1 = ?", ["10","11","12"], "10"),
        ("8 x 2 = ?", ["14","16","18"], "16"),
        ("12 / 4 = ?", ["2","3","4"], "3"),
        ("7 + 5 = ?", ["11","12","13"], "12"),
        ("15 - 5 = ?", ["5","10","15"], "10"),
    ]

    score = 0
    answers = []

    for i, (q, options, correct) in enumerate(questions):
        ans = st.radio(q, options, key=i)
        answers.append((ans, correct))

    if st.button("Submit Test"):
        for ans, correct in answers:
            if ans == correct:
                score += 1
        st.success(f"Your Score: {score}/10")

# ================= EMAIL =================
st.markdown(f"""
<div class="email">
📧 Contact: {EMAIL}
</div>
""", unsafe_allow_html=True)
