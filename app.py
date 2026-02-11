import streamlit as st

APP_NAME = "IS_FINE APP"

st.set_page_config(page_title=APP_NAME, layout="wide")

# Hide Streamlit header/footer
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ================= EXACT UI STYLE =================
st.markdown("""
<style>

body {
    background: #F4F4F4;
    font-family: 'Segoe UI', sans-serif;
}

/* HEADER BANNER */
.banner {
    background: linear-gradient(90deg, #F3EDE6, #E8DFD4);
    border: 3px solid #C6A46C;
    border-radius: 25px;
    padding: 40px;
    margin-top: 30px;
    position: relative;
}

.banner-title {
    font-size: 42px;
    font-weight: 700;
    color: #5C0632;
}

.banner-sub {
    font-size: 22px;
    color: #7A4C4C;
    margin-top: 10px;
}

/* SEARCH ICON */
.search-icon {
    position: absolute;
    right: 30px;
    top: 30px;
    font-size: 28px;
    color: #C6A46C;
}

/* CARD CONTAINER */
.card-row {
    display: flex;
    gap: 25px;
    margin-top: 40px;
}

/* CARD STYLE */
.card {
    flex: 1;
    border-radius: 25px;
    padding: 40px;
    text-align: center;
    border: 2px solid #C6A46C;
    background: #EDEDED;
    transition: 0.3s;
    cursor: pointer;
}

.card:hover {
    transform: translateY(-6px);
}

/* FIRST CARD ACTIVE */
.card-active {
    background: linear-gradient(135deg, #7C2636, #5C0632);
    color: white;
    border: none;
}

.card-title {
    margin-top: 15px;
    font-size: 20px;
    font-weight: 600;
}

/* ADD NEW BUTTON */
.add-new {
    margin-top: 30px;
    display: inline-block;
    padding: 15px 30px;
    border-radius: 15px;
    border: 2px solid #C6A46C;
    background: #EFE6DA;
    font-size: 18px;
    cursor: pointer;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="banner">
    <div class="search-icon">🔍</div>
    <div class="banner-title">IS_FINE APP</div>
    <div class="banner-sub">Manage your files easily</div>
</div>
""", unsafe_allow_html=True)

# ================= CARDS =================
st.markdown('<div class="card-row">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🖼 Image to PDF", use_container_width=True):
        st.write("Image to PDF Page")

with col2:
    if st.button("📄 Past Exam Papers", use_container_width=True):
        st.write("Past Exam Page")

with col3:
    if st.button("🔒 Secret Files", use_container_width=True):
        st.write("Secret Files Page")

with col4:
    if st.button("➕ Add New", use_container_width=True):
        st.write("Add New Page")

st.markdown('</div>', unsafe_allow_html=True)

# ================= BOTTOM ADD BUTTON =================
st.markdown("""
<div class="add-new">➕ Add New</div>
""", unsafe_allow_html=True)
