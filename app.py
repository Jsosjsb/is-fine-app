import streamlit as st
import sqlite3
import os
import base64

# ================= CONFIG =================
APP_NAME = "IS_FINE"
EMAIL = "adishaikh776@gmail.com"
EXAM_FOLDER = "exam_papers"
DB_NAME = "app.db"

os.makedirs(EXAM_FOLDER, exist_ok=True)

# ================= DATABASE =================
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()

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

# ================= SESSION =================
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ================= PAGE CONFIG =================
st.set_page_config(page_title=APP_NAME, layout="wide")

# Hide Streamlit default UI
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
body {
    background: #F4F6F9;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown(f"""
<h1 style='text-align:center; color:#5C0632;'>{APP_NAME}</h1>
<p style='text-align:center;'>Online Aptitude & Exam Portal - Created by Bilal Shaikh</p>
""", unsafe_allow_html=True)

# ================= HOME =================
if st.session_state.page == "Home":

    if st.button("📊 Analytics Dashboard"):
        st.session_state.page = "Dashboard"

    if st.button("🧠 Take Aptitude Test"):
        st.session_state.page = "Test"

    if st.button("🏆 Leaderboard"):
        st.session_state.page = "Leaderboard"

    if st.button("📄 Exam Papers"):
        st.session_state.page = "Papers"

# ================= DASHBOARD =================
elif st.session_state.page == "Dashboard":

    st.header("📊 Analytics Dashboard")

    cursor.execute("SELECT COUNT(*) FROM analytics")
    total_actions = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scores")
    total_tests = cursor.fetchone()[0]

    st.metric("Total Platform Actions", total_actions)
    st.metric("Total Tests Taken", total_tests)

    if st.button("⬅ Back to Home"):
        st.session_state.page = "Home"

# ================= TEST =================
elif st.session_state.page == "Test":

    st.header("🧠 Advanced Aptitude Test")

    username = st.text_input("Enter Your Name")

    questions = [
        ("Solve: 3x + 5 = 20. x = ?", ["3","4","5"], "5"),
        ("Square root of 196?", ["12","14","16"], "14"),
        ("Average of 5 numbers is 12. Total sum?", ["50","60","70"], "60"),
        ("Prime numbers between 1 and 20?", ["6","7","8"], "8"),
        ("2^5 = ?", ["16","32","64"], "32"),
        ("(15 × 3) ÷ 5 = ?", ["9","10","12"], "9"),
        ("25% of 240?", ["50","60","70"], "60"),
        ("Perimeter of square = 40. Side = ?", ["8","10","12"], "10"),
        ("7! = ?", ["5040","720","120"], "5040"),
        ("GCD of 24 and 36?", ["6","8","12"], "12"),
    ]

    score = 0
    answers = []

    for i,(q,options,correct) in enumerate(questions):
        ans = st.radio(q, options, key=i)
        answers.append((ans,correct))

    if st.button("Submit Test"):
        if username.strip() == "":
            st.error("Please enter your name.")
        else:
            for ans,correct in answers:
                if ans == correct:
                    score += 1

            cursor.execute("INSERT INTO scores(username,score) VALUES(?,?)",
                           (username,score))
            conn.commit()

            cursor.execute("INSERT INTO analytics(event) VALUES('Test Taken')")
            conn.commit()

            st.success(f"Your Final Score: {score} / 10")

    if st.button("⬅ Back to Home"):
        st.session_state.page = "Home"

# ================= LEADERBOARD =================
elif st.session_state.page == "Leaderboard":

    st.header("🏆 Top 10 Leaderboard")

    cursor.execute("""
    SELECT username, MAX(score) as best_score
    FROM scores
    GROUP BY username
    ORDER BY best_score DESC
    LIMIT 10
    """)

    data = cursor.fetchall()

    if data:
        for rank, (username, score) in enumerate(data, start=1):
            st.write(f"#{rank}  —  {username}  —  {score}/10")
    else:
        st.info("No test attempts yet.")

    if st.button("⬅ Back to Home"):
        st.session_state.page = "Home"

# ================= PDF VIEWER =================
elif st.session_state.page == "Papers":

    st.header("📄 Exam Papers")

    pdfs = [f for f in os.listdir(EXAM_FOLDER) if f.endswith(".pdf")]

    for pdf in pdfs:
        st.subheader(pdf)

        path = os.path.join(EXAM_FOLDER,pdf)
        with open(path,"rb") as f:
            pdf_bytes = f.read()

        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_display = f"""
        <iframe src="data:application/pdf;base64,{base64_pdf}"
        width="100%" height="600"></iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)

        if st.button(f"Download {pdf}"):
            cursor.execute("INSERT INTO analytics(event) VALUES('PDF Download')")
            conn.commit()

    if st.button("⬅ Back to Home"):
        st.session_state.page = "Home"

# ================= EMAIL =================
st.markdown(f"""
<hr>
<p style='text-align:center; color:#5C0632; font-weight:bold;'>
Contact: {EMAIL}
</p>
""", unsafe_allow_html=True)
