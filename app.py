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

# ================= SESSION =================
if "page" not in st.session_state:
    st.session_state.page = "الرئيسية"

# ================= PAGE CONFIG =================
st.set_page_config(page_title=APP_NAME, layout="wide")

# Hide Streamlit UI
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

/* HEADER */
.header {
    text-align: center;
    margin-top: 40px;
    margin-bottom: 30px;
}

.header h1 {
    color: #5C0632;
    font-size: 42px;
}

.header p {
    color: #555;
}

/* CARD */
.card {
    background: white;
    border-radius: 18px;
    padding: 30px;
    margin: 20px 0;
    position: relative;
    cursor: pointer;
}

/* Animated Border */
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
    <p>بوابة الخدمات الإلكترونية - تصميم بلال شيخ</p>
</div>
""", unsafe_allow_html=True)

# ================= HOME =================
if st.session_state.page == "الرئيسية":

    if st.button("📊 لوحة التحكم"):
        st.session_state.page = "التحليلات"

    if st.button("🧠 اختبر نفسك"):
        st.session_state.page = "الاختبار"

    if st.button("📄 أوراق الامتحان"):
        st.session_state.page = "الامتحانات"

# ================= DASHBOARD =================
elif st.session_state.page == "التحليلات":

    st.subheader("📊 لوحة التحليلات")

    cursor.execute("SELECT COUNT(*) FROM analytics")
    visits = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scores")
    tests = cursor.fetchone()[0]

    st.metric("إجمالي العمليات", visits)
    st.metric("عدد الاختبارات المنجزة", tests)

    if st.button("⬅ العودة للرئيسية"):
        st.session_state.page = "الرئيسية"

# ================= HARD TEST =================
elif st.session_state.page == "الاختبار":

    st.subheader("🧠 اختبار القدرات - مستوى متقدم")

    questions = [
        ("إذا كان 3x + 5 = 20، فما قيمة x؟", ["3","4","5"], "5"),
        ("ما هو الجذر التربيعي لـ 196؟", ["12","14","16"], "14"),
        ("إذا كان متوسط 5 أعداد هو 12، فما مجموعها؟", ["50","60","70"], "60"),
        ("كم عدد الأعداد الأولية بين 1 و 20؟", ["6","7","8"], "8"),
        ("إذا كان 2^5 = ؟", ["16","32","64"], "32"),
        ("احسب: (15 × 3) ÷ 5", ["9","10","12"], "9"),
        ("ما هو 25% من 240؟", ["50","60","70"], "60"),
        ("إذا كان محيط مربع 40، فما طول الضلع؟", ["8","10","12"], "10"),
        ("كم يساوي 7! ؟", ["5040","720","120"], "5040"),
        ("إذا كان القاسم المشترك الأكبر لـ 24 و 36 هو؟", ["6","8","12"], "12"),
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

        st.success(f"نتيجتك النهائية: {score} / 10")

    if st.button("⬅ العودة للرئيسية"):
        st.session_state.page = "الرئيسية"

# ================= PDF SECTION =================
elif st.session_state.page == "الامتحانات":

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

    if st.button("⬅ العودة للرئيسية"):
        st.session_state.page = "الرئيسية"

# ================= EMAIL =================
st.markdown(f"""
<div class="email">
📧 البريد الإلكتروني: {EMAIL}
</div>
""", unsafe_allow_html=True)
