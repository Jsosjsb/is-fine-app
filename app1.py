import streamlit as st
import pandas as pd
from fractions import Fraction
import json

# ─── Measure parsing & scaling ───────────────────────────────────────
def parse_measure(s):
    if not s or pd.isna(s): return None, ""
    s = str(s).strip()
    parts = s.split(maxsplit=1)
    num_str = parts[0]
    unit = parts[1] if len(parts)>1 else ""
    try:
        if '/' in num_str: num = float(Fraction(num_str))
        else: num = float(num_str)
        return num, unit.strip()
    except:
        return None, s

def scale_measure(s, factor):
    n, u = parse_measure(s)
    if n is not None:
        scaled = n * factor
        scaled = int(scaled) if scaled.is_integer() else round(scaled, 2)
        return f"{scaled} {u}".strip()
    return u.strip() or s

# ─── Page & Theme ───────────────────────────────────────���────────────
st.set_page_config(
    page_title="Culinary Craft • Professional Recipe Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "Professional Recipe Assistant v1.0"}
)

# ─── Advanced CSS Styling ────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Lato:wght@300;400;700&family=Poppins:wght@500;600;700&display=swap');

    * { margin: 0; padding: 0; box-sizing: border-box; }

    .stApp {
        background: linear-gradient(135deg, #0a0803 0%, #1a130c 100%);
        color: #e8dcc8;
        font-family: 'Lato', sans-serif;
    }

    /* Typography */
    h1, h2, h3, h4, h5 { 
        font-family: 'Playfair Display', serif; 
        color: #e8b923; 
        letter-spacing: 1px;
    }

    h1 { font-size: 3.5rem; font-weight: 800; }
    h2 { font-size: 2.2rem; font-weight: 700; margin-top: 1.5rem; }
    h3 { font-size: 1.6rem; font-weight: 700; }
    h4 { font-size: 1.3rem; font-weight: 700; }

    /* ─── Navigation ─── */
    .nav-container {
        background: linear-gradient(90deg, #1a130c 0%, #2d1e15 100%);
        padding: 1.5rem 2rem;
        border-bottom: 3px solid #e8b923;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .nav-logo {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 800;
        color: #e8b923;
        text-decoration: none;
        letter-spacing: 2px;
    }

    .nav-links {
        display: flex;
        gap: 2.5rem;
        list-style: none;
    }

    .nav-link {
        color: #d4af88;
        text-decoration: none;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: all 0.3s ease;
        position: relative;
    }

    .nav-link:hover {
        color: #e8b923;
        background: rgba(232, 185, 35, 0.1);
        transform: translateY(-2px);
    }

    /* ─── Hero Section ─── */
    .hero-section {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(180deg, rgba(232,185,35,0.05) 0%, rgba(0,0,0,0) 100%);
        border-radius: 20px;
        margin-bottom: 2.5rem;
        border: 1px solid rgba(232,185,35,0.2);
    }

    .hero-section h1 {
        font-size: 4rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 20px rgba(232,185,35,0.3);
        animation: fadeInDown 0.8s ease;
    }

    .hero-tagline {
        color: #d4af88;
        font-size: 1.4rem;
        font-weight: 300;
        letter-spacing: 1px;
        animation: fadeInUp 0.8s ease 0.2s backwards;
    }

    @keyframes fadeInDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

    /* ─── Filters Section ─── */
    .filter-section {
        background: linear-gradient(135deg, rgba(45,30,21,0.8) 0%, rgba(26,19,13,0.8) 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid rgba(232,185,35,0.2);
        margin-bottom: 2.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
    }

    .filter-title {
        color: #e8b923;
        font-weight: 600;
        margin-bottom: 1.5rem;
        font-size: 1.2rem;
    }

    /* ─── Recipe Card ─── */
    .recipe-card {
        background: linear-gradient(135deg, rgba(26,19,13,0.95) 0%, rgba(45,30,21,0.95) 100%);
        border: 2px solid #e8b923;
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 15px 50px rgba(0,0,0,0.6);
        backdrop-filter: blur(10px);
        margin: 2rem 0;
        animation: slideInUp 0.6s ease;
    }

    @keyframes slideInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }

    .recipe-header {
        text-align: center;
        margin-bottom: 2.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 2px solid rgba(232,185,35,0.3);
    }

    .recipe-header h2 {
        font-size: 3rem;
        margin: 0.5rem 0;
    }

    .recipe-meta {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }

    .meta-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #d4af88;
        font-weight: 500;
    }

    .meta-icon {
        font-size: 1.4rem;
    }

    /* ─── Image Section ─── */
    .dish-image-container {
        position: relative;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 12px 35px rgba(232,185,35,0.15);
        border: 2px solid #e8b923;
        margin-bottom: 2rem;
    }

    .dish-image-container img {
        width: 100%;
        height: auto;
        display: block;
        transition: transform 0.4s ease;
    }

    .dish-image-container:hover img {
        transform: scale(1.05);
    }

    /* ─── Ingredients List ─── */
    .ingredients-section h3 {
        color: #e8b923;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid rgba(232,185,35,0.3);
    }

    .ing-list {
        list-style: none;
        padding: 0;
    }

    .ing-list li {
        font-size: 1.1rem;
        margin: 1rem 0;
        padding-left: 2.5rem;
        position: relative;
        color: #e8dcc8;
        line-height: 1.6;
        transition: all 0.3s ease;
    }

    .ing-list li:hover {
        padding-left: 3rem;
        color: #e8b923;
    }

    .ing-list li:before {
        content: "✓";
        color: #e8b923;
        position: absolute;
        left: 0;
        font-size: 1.5rem;
        font-weight: bold;
    }

    /* ─── Instructions ─── */
    .instructions-section h3 {
        color: #e8b923;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid rgba(232,185,35,0.3);
    }

    .steps ol {
        counter-reset: stepcounter;
        list-style: none;
        padding: 0;
    }

    .steps li {
        position: relative;
        padding: 1.5rem;
        padding-left: 5rem;
        margin: 1.2rem 0;
        background: linear-gradient(135deg, rgba(232,185,35,0.05) 0%, rgba(0,0,0,0) 100%);
        border-radius: 12px;
        border-left: 4px solid #e8b923;
        color: #e8dcc8;
        line-height: 1.8;
        transition: all 0.3s ease;
    }

    .steps li:hover {
        background: linear-gradient(135deg, rgba(232,185,35,0.1) 0%, rgba(0,0,0,0.05) 100%);
        transform: translateX(10px);
        box-shadow: 0 5px 15px rgba(232,185,35,0.1);
    }

    .steps li:before {
        counter-increment: stepcounter;
        content: counter(stepcounter);
        position: absolute;
        left: 1.2rem;
        top: 50%;
        transform: translateY(-50%);
        width: 3rem;
        height: 3rem;
        background: linear-gradient(135deg, #e8b923 0%, #d4a435 100%);
        color: #0a0803;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1.4rem;
        box-shadow: 0 4px 12px rgba(232,185,35,0.3);
    }

    /* ─── Tips & Warnings ─── */
    .tips-warnings {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin: 2.5rem 0;
    }

    .info-box {
        padding: 1.8rem;
        border-radius: 12px;
        border-left: 5px solid;
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
    }

    .info-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }

    .tip-box {
        background: linear-gradient(135deg, rgba(232,185,35,0.08) 0%, rgba(0,0,0,0.05) 100%);
        border-color: #e8b923;
    }

    .tip-box h4 { color: #e8b923; }
    .tip-box ul { color: #d4af88; }

    .warning-box {
        background: linear-gradient(135deg, rgba(184,74,74,0.08) 0%, rgba(0,0,0,0.05) 100%);
        border-color: #d45555;
    }

    .warning-box h4 { color: #e88888; }
    .warning-box ul { color: #d4a8a8; }

    .info-box ul {
        list-style: none;
        padding-left: 1.5rem;
    }

    .info-box li {
        margin: 0.7rem 0;
        padding-left: 1.5rem;
        position: relative;
        line-height: 1.6;
    }

    .tip-box li:before { content: "→"; color: #e8b923; position: absolute; left: 0; }
    .warning-box li:before { content: "⚠"; color: #e88888; position: absolute; left: 0; }

    /* ─── Action Buttons ─── */
    .button-container {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin: 2.5rem 0;
        flex-wrap: wrap;
    }

    .action-btn {
        background: linear-gradient(135deg, #e8b923 0%, #d4a435 100%);
        color: #0a0803;
        border: none;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.4s ease;
        box-shadow: 0 6px 20px rgba(232,185,35,0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .action-btn:hover {
        background: linear-gradient(135deg, #fff 0%, #e8b923 100%);
        box-shadow: 0 10px 30px rgba(232,185,35,0.5);
        transform: translateY(-3px);
    }

    .action-btn:active {
        transform: translateY(-1px);
    }

    .secondary-btn {
        background: rgba(232,185,35,0.2);
        color: #e8b923;
        border: 2px solid #e8b923;
    }

    .secondary-btn:hover {
        background: #e8b923;
        color: #0a0803;
    }

    /* ─── Footer ─── */
    .footer {
        text-align: center;
        padding: 3rem 2rem;
        margin-top: 3rem;
        border-top: 2px solid rgba(232,185,35,0.3);
        color: #b89e7e;
    }

    .footer-title {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        color: #e8b923;
        margin-bottom: 1rem;
        letter-spacing: 2px;
    }

    .footer-text {
        font-size: 1.1rem;
        line-height: 1.8;
        margin: 0.5rem 0;
    }

    /* ─── Responsive ─── */
    @media (max-width: 768px) {
        h1 { font-size: 2.5rem; }
        h2 { font-size: 1.8rem; }
        .tips-warnings { grid-template-columns: 1fr; gap: 1.5rem; }
        .nav-links { gap: 1rem; font-size: 0.9rem; }
        .button-container { flex-direction: column; }
        .action-btn { width: 100%; }
        .recipe-meta { flex-direction: column; gap: 1rem; }
        .steps li { padding-left: 4.5rem; }
    }

    /* ─── Scrollbar ─── */
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: #1a130c; }
    ::-webkit-scrollbar-thumb { background: #e8b923; border-radius: 5px; }
    ::-webkit-scrollbar-thumb:hover { background: #d4a435; }

    /* ─── Animations ─── */
    .fade-in { animation: fadeIn 0.8s ease; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

</style>
""", unsafe_allow_html=True)

# ─── Data Loading ────────────────────────────────────────────────────
@st.cache_data
def load_data():
    """Load and clean recipe dataset"""
    try:
        df = pd.read_csv("mealdb_dataset_with_flag.csv")
        df.columns = df.columns.str.lower().str.strip()
        
        # Clean ingredient and measure columns
        for i in range(1, 21):
            ing_col = f'stringredient{i}'
            meas_col = f'strmeasure{i}'
            
            if ing_col in df.columns:
                df[ing_col] = df[ing_col].astype(str).replace(['nan', 'NaN', ''], '').str.strip()
            if meas_col in df.columns:
                df[meas_col] = df[meas_col].astype(str).replace(['nan', 'NaN', ''], '').str.strip()
        
        return df
    except FileNotFoundError:
        st.error("Dataset file 'mealdb_dataset_with_flag.csv' not found!")
        return None

df = load_data()

if df is None:
    st.stop()

# ─── Sidebar Configuration ────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙�� Preferences")
    serving_default = st.slider("Default Servings", 1, 20, 4, help="Set your preferred number of servings")
    
    st.divider()
    st.markdown("### 📊 About")
    st.info("""
    **Culinary Craft** - Your professional recipe assistant
    
    - 🍳 Scalable recipes
    - 👨‍🍳 Step-by-step guidance
    - 💡 Professional tips
    - ⚠️ Common mistakes to avoid
    """)

# ─── Navigation ─── 
st.markdown("""
<div class="nav-container">
    <span class="nav-logo">🍽️ Culinary Craft</span>
    <ul class="nav-links">
        <li><a href="#" class="nav-link">Home</a></li>
        <li><a href="#" class="nav-link">Recipes</a></li>
        <li><a href="#" class="nav-link">Tips</a></li>
        <li><a href="#" class="nav-link">Contact</a></li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ─── Hero Section ───
st.markdown("""
<div class="hero-section">
    <h1>Culinary Craft</h1>
    <p class="hero-tagline">Discover & Master Authentic Recipes</p>
</div>
""", unsafe_allow_html=True)

# ─── Filter Section ───
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.markdown('<p class="filter-title">🔍 Find Your Perfect Dish</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 2, 1.5])

with col1:
    veg_options = sorted(df['veg_flag'].unique())
    veg_nonveg = st.selectbox(
        "Recipe Type",
        veg_options,
        help="Choose between vegetarian and non-vegetarian recipes"
    )

filtered_df = df[df['veg_flag'] == veg_nonveg]
dishes = sorted(filtered_df['strmeal'].dropna().unique())

with col2:
    dish = st.selectbox(
        "Select Dish",
        dishes if dishes else ["No dishes available"],
        help="Choose a recipe to view details"
    )

with col3:
    persons = st.number_input(
        "Servings",
        min_value=1,
        max_value=20,
        value=serving_default,
        step=1,
        help="Adjust recipe for number of servings"
    )

st.markdown('</div>', unsafe_allow_html=True)

# ─��─ Get Recipe Button ───
if st.button("🎯 Get Recipe", type="primary", use_container_width=True):
    if not dish or dish == "No dishes available":
        st.error("❌ Please select a valid dish from the list.")
    else:
        # Get recipe data
        recipe_row = filtered_df[filtered_df['strmeal'] == dish].iloc[0]
        
        # ─── Recipe Header ───
        st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="recipe-header">
            <h2>{recipe_row['strmeal']}</h2>
            <div class="recipe-meta">
                <div class="meta-item">
                    <span class="meta-icon">👥</span>
                    <span>{persons} Serving{"s" if persons != 1 else ""}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-icon">⏱️</span>
                    <span>≈ 45 Minutes</span>
                </div>
                <div class="meta-item">
                    <span class="meta-icon">📊</span>
                    <span>Medium Difficulty</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ─── Image & Ingredients ───
        img_col, ing_col = st.columns([1.2, 1], gap="large")
        
        with img_col:
            if recipe_row.get('strmealthumb'):
                st.markdown('<div class="dish-image-container">', unsafe_allow_html=True)
                st.image(
                    recipe_row['strmealthumb'],
                    use_column_width=True,
                    caption=f"Delicious {recipe_row['strmeal']}"
                )
                st.markdown('</div>', unsafe_allow_html=True)
        
        with ing_col:
            st.markdown('<div class="ingredients-section">', unsafe_allow_html=True)
            st.markdown('<h3>🥘 Ingredients</h3>', unsafe_allow_html=True)
            
            base_servings = 4
            scale_factor = persons / base_servings
            
            ingredients_html = '<ul class="ing-list">'
            ingredient_count = 0
            
            for i in range(1, 21):
                ingredient = recipe_row.get(f'stringredient{i}', '').strip()
                measure = recipe_row.get(f'strmeasure{i}', '').strip()
                
                if ingredient:
                    scaled_measure = scale_measure(measure, scale_factor)
                    ingredient_text = f"{scaled_measure} {ingredient}" if scaled_measure else ingredient
                    ingredients_html += f'<li>{ingredient_text}</li>'
                    ingredient_count += 1
            
            ingredients_html += '</ul>'
            st.markdown(ingredients_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ─── Instructions ───
        st.markdown('<div class="instructions-section">', unsafe_allow_html=True)
        st.markdown('<h3>👨‍🍳 Step-by-Step Instructions</h3>', unsafe_allow_html=True)
        
        instructions = recipe_row.get('strinstructions', 'No instructions available.').strip()
        # Split instructions intelligently
        sentences = [s.strip() for s in instructions.replace('\n', ' ').split('.') if s.strip()]
        
        steps_html = '<ol class="steps">'
        for sentence in sentences[:12]:  # Limit to 12 steps
            steps_html += f'<li>{sentence}.</li>'
        steps_html += '</ol>'
        
        st.markdown(steps_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ─── Tips & Warnings ───
        st.markdown('<div class="tips-warnings">', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box tip-box">
            <h4>💡 Professional Tips</h4>
            <ul>
                <li>Use fresh, quality ingredients for best results</li>
                <li>Prepare and measure all ingredients before cooking (mise en place)</li>
                <li>Maintain proper temperature control throughout</li>
                <li>Don't skip the resting time - it matters!</li>
                <li>Taste and adjust seasonings as you cook</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box warning-box">
            <h4>⚠️ Common Mistakes to Avoid</h4>
            <ul>
                <li>Adding ingredients before reaching proper temperature</li>
                <li>Overcrowding the pan or pot</li>
                <li>Not following the recipe order</li>
                <li>Cooking on too high heat</li>
                <li>Skipping important steps for speed</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ─── Action Buttons ───
        st.markdown("""
        <div class="button-container">
            <button class="action-btn">🔊 Listen Recipe</button>
            <button class="action-btn secondary-btn">🖨️ Print Recipe</button>
            <button class="action-btn secondary-btn">⭐ Save Recipe</button>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close recipe-card
        
        # ─── Footer ───
        st.markdown("""
        <div class="footer">
            <div class="footer-title">✨ Happy Cooking! ✨</div>
            <p class="footer-text">Enjoy creating your masterpiece in the kitchen</p>
            <p class="footer-text" style="font-size: 0.9rem; color: #8b7e6b; margin-top: 1.5rem;">
                © 2024 Culinary Craft • Professional Recipe Assistant
            </p>
        </div>
        """, unsafe_allow_html=True)