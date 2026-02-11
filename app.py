import streamlit as st

# ================= CONFIG =================
APP_NAME = "IS_FINE"
WHATSAPP_LINK = "https://wa.me/918999932770"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="💎",
    layout="wide"
)

# ================= QATAR STYLE HEADER =================
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #F8F5F2, #EFE9E3);
    color: #3A0F1D;
}

/* HEADER */
.header-box {
    background: linear-gradient(90deg, #5A0F2E, #7A1B3F);
    padding: 30px;
    border-radius: 20px;
    color: white;
    margin-bottom: 40px;
}

.header-title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: 2px;
}

.header-sub {
    font-size: 18px;
    color: #E8C9A0;
}

/* CARDS */
.card {
    background: white;
    border: 2px solid #D4AF37;
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    transition: 0.3s ease;
    cursor: pointer;
}

.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 35px rgba(212,175,55,0.4);
}

/* ICON */
.icon {
    font-size: 50px;
    margin-bottom: 15px;
}

/* FOOTER */
.footer {
    text-align: center;
    margin-top: 50px;
    font-size: 14px;
    color: #7A1B3F;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="header-box">
    <div class="header-title">IS_FINE APP</div>
    <div class="header-sub">Manage your files easily & securely</div>
</div>
""", unsafe_allow_html=True)

# ================= CARDS =================
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🖼️ Image to PDF", use_container_width=True):
        st.session_state.page = "convert"

with col2:
    if st.button("📄 Past Exam Papers", use_container_width=True):
        st.session_state.page = "exam"

with col3:
    if st.button("🔐 Secret Files", use_container_width=True):
        st.session_state.page = "secret"

with col4:
    if st.button("➕ Add New", use_container_width=True):
        st.markdown(f"[Open WhatsApp]({WHATSAPP_LINK})")

# ================= SECRET PAGE (PLACEHOLDER) =================
if "page" in st.session_state and st.session_state.page == "secret":
    st.header("🔐 Secret Files")
    st.write("This section is private and password protected (can be added).")

# ================= FOOTER =================
st.markdown("""
<div class="footer">
    Created by Bilal Shaikh
</div>
""", unsafe_allow_html=True)
