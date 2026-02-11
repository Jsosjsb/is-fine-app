import streamlit as st
import sqlite3
import hashlib
import os
import base64
from PyPDF2 import PdfReader

# ================= CONFIG =================
APP_NAME = "IS_FINE"
DB_NAME = "app.db"
EXAM_FOLDER = "exam_papers"
os.makedirs(EXAM_FOLDER, exist_ok=True)

# ================= DATABASE SETUP =================
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS scores(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    score INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS analytics(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT
)
""")
conn.commit()

# ================= HELPERS =================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_analytics(event):
    cursor.execute("INSERT INTO analytics(event) VALUES(?)", (event,))
    conn.commit()

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None
if "lang" not in st.session_state:
    st.session_state.lang = "EN"

# ================= LANGUAGE =================
def t(en, ar):
    return en if st.session_state.lang == "EN" else ar

# ================= UI =================
st.title(APP_NAME)

col1, col2 = st.columns([6,1])
with col2:
    if st.button("EN / AR"):
        st.session_state.lang = "AR" if st.session_state.lang=="EN" else "EN"

# ================= AUTH =================
if st.session_state.user is None:

    option = st.selectbox("Select", ["Login","Register"])

    username = st.text_input(t("Username","اسم المستخدم"))
    password = st.text_input(t("Password","كلمة المرور"), type="password")

    if option == "Register":
        if st.button("Register"):
            try:
                cursor.execute("INSERT INTO users(username,password) VALUES(?,?)",
                               (username, hash_password(password)))
                conn.commit()
                st.success("Registered Successfully")
            except:
                st.error("User already exists")

    if option == "Login":
        if st.button("Login"):
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                           (username, hash_password(password)))
            if cursor.fetchone():
                st.session_state.user = username
                st.success("Logged In")
                st.rerun()
            else:
                st.error("Invalid credentials")

else:

    st.success(f"Welcome {st.session_state.user}")

    menu = st.selectbox("Menu",
                        [t("Dashboard","لوحة التحكم"),
                         t("Test Yourself","اختبر نفسك"),
                         t("Exam Papers","أوراق الامتحان"),
                         t("Logout","تسجيل الخروج")])

    # ================= DASHBOARD =================
    if menu == t("Dashboard","لوحة التحكم"):
        st.header(t("Analytics Dashboard","لوحة التحليلات"))

        cursor.execute("SELECT COUNT(*) FROM analytics")
        visits = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM scores")
        tests = cursor.fetchone()[0]

        st.metric("Total Actions", visits)
        st.metric("Total Tests Taken", tests)

    # ================= TEST =================
    if menu == t("Test Yourself","اختبر نفسك"):

        questions = [
            ("2 + 2 ?", ["3","4","5"], "4"),
            ("5 x 3 ?", ["10","15","20"], "15"),
            ("10 - 6 ?", ["3","4","5"], "4"),
            ("9 + 1 ?", ["10","11","12"], "10"),
            ("12 / 4 ?", ["2","3","4"], "3"),
            ("6 x 2 ?", ["10","12","14"], "12"),
            ("15 - 5 ?", ["5","10","15"], "10"),
            ("8 + 7 ?", ["14","15","16"], "15"),
            ("9 x 1 ?", ["9","8","7"], "9"),
            ("20 / 5 ?", ["2","4","6"], "4"),
        ]

        score = 0
        answers = []

        for i,(q,options,correct) in enumerate(questions):
            ans = st.radio(q, options, key=i)
            answers.append((ans,correct))

        if st.button("Submit"):
            for ans,correct in answers:
                if ans == correct:
                    score += 1

            cursor.execute("INSERT INTO scores(username,score) VALUES(?,?)",
                           (st.session_state.user,score))
            conn.commit()

            add_analytics("Test Taken")

            st.success(f"Score: {score}/10")

    # ================= EXAM PAPERS =================
    if menu == t("Exam Papers","أوراق الامتحان"):

        pdfs = [f for f in os.listdir(EXAM_FOLDER) if f.endswith(".pdf")]

        for pdf in pdfs:
            st.subheader(pdf)

            path = os.path.join(EXAM_FOLDER,pdf)
            with open(path,"rb") as f:
                pdf_bytes = f.read()

            # REAL PDF VIEWER
            base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
            pdf_display = f"""
            <iframe src="data:application/pdf;base64,{base64_pdf}"
            width="100%" height="500"></iframe>
            """
            st.markdown(pdf_display, unsafe_allow_html=True)

            if st.button("Download "+pdf):
                add_analytics("PDF Download")

    # ================= LOGOUT =================
    if menu == t("Logout","تسجيل الخروج"):
        st.session_state.user = None
        st.rerun()
