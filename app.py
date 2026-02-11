import streamlit as st
import os
import sqlite3
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

# ================= PAGE CONFIG =================
st.set_page_config(page_title=APP_NAME, layout="wide")

# Hide Streamlit default
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ================= RTL STYLE =================
st.markdown("""
<style>
body {
    direction: rtl;
    text-align: right;
    font-family: 'Segoe UI', sans-serif;
    background: #F5F7FA;
}

/* Header */
.header {
    text-align: center;
    margin-top: 40px;
    margin-bottom: 30px;
}

.header h1 {
    color: #5C0632;
    font-size: 40px;
}

.header p {
    color: #555;
}

/* Cards */
.card {
    background: white;
    border-radius: 18px;
    padding: 30px;
    margin-bottom: 20px;
    position: relative;
    cursor: pointer;
}

/* Animated Mulberry Border */
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

.email {
    text-align: center;
    margin-top: 50px;
    color: #5C0632;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown(f"""
<div class="header">
    <h1>{APP_NAME}</h1>
    <p>تطبيق إدارة الملفات - تصميم بلال شيخ</p>
</div>
""", unsafe_allow_html=True)

# ================= MENU =================
menu = st.selectbox(
    "القائمة الرئيسية",
    ["لوحة التحكم", "اختبر نفسك", "أوراق الامتحان"]
)

# ================= DASHBOARD =================
if menu == "لوحة التحكم":

    st.subheader("📊 لوحة التحليلات")

    cursor.execute("SELECT COUNT(*) FROM analytics")
    visits = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scores")
    tests = cursor.fetchone()[0]

    st.metric("إجمالي العمليات", visits)
    st.metric("عدد الاختبارات", tests)

# ================= TEST SECTION =================
elif menu == "اختبر نفسك":

    st.subheader("🧠 اختبار القدرات")

    questions = [
        ("كم حاصل 2 + 2؟", ["3","4","5"], "4"),
        ("كم حاصل 5 × 3؟", ["10","15","20"], "15"),
        ("كم حاصل 10 - 6؟", ["3","4","5"], "4"),
        ("كم حاصل 9 + 1؟", ["10","11","12"], "10"),
        ("كم حاصل 12 ÷ 4؟", ["2","3","4"], "3"),
        ("كم حاصل 6 × 2؟", ["10","12","14"], "12"),
        ("كم حاصل 15 - 5؟", ["5","10","15"], "10"),
        ("كم حاصل 8 + 7؟", ["14","15","16"], "15"),
        ("كم حاصل 9 × 1؟", ["9","8","7"], "9"),
        ("كم حاصل 20 ÷ 5؟", ["2","4","6"], "4"),
    ]

    score = 0
    answers = []

    for i,(q,options,correct) in enumerate(questions):
        ans = st.radio(q, options, key=i)
        answers.append((ans,correct))

    if st.button("إرسال الإجابات"):
        for ans,correct in answers:
            if ans == correct:
                score += 1

        cursor.execute("INSERT INTO scores(score) VALUES(?)",(score,))
        conn.commit()

        cursor.execute("INSERT INTO analytics(event) VALUES('Test Taken')")
        conn.commit()

        st.success(f"نتيجتك: {score} / 10")

# ================= PDF SECTION =================
elif menu == "أوراق الامتحان":

    st.subheader("📄 أوراق الامتحانات")

    pdfs = [f for f in os.listdir(EXAM_FOLDER) if f.endswith(".pdf")]

    for pdf in pdfs:
        st.markdown(f"### {pdf}")

        path = os.path.join(EXAM_FOLDER,pdf)
        with open(path,"rb") as f:
            pdf_bytes = f.read()

        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_display = f"""
        <iframe src="data:application/pdf;base64,{base64_pdf}"
        width="100%" height="600"></iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)

        if st.button(f"تحميل {pdf}"):
            cursor.execute("INSERT INTO analytics(event) VALUES('PDF Download')")
            conn.commit()

# ================= EMAIL =================
st.markdown(f"""
<div class="email">
📧 البريد الإلكتروني: {EMAIL}
</div>
""", unsafe_allow_html=True)
