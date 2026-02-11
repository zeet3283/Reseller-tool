import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# ---------------------------------------------------------
# 1. APP CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="ResellerLens Pro",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. ULTRA-MODERN CSS (Mobile First)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* IMPORT MODERN FONT */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* GRADIENT HEADER */
    .gradient-text {
        background: linear-gradient(120deg, #11998e, #38ef7d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5em;
        text-align: center;
        margin-bottom: 0;
    }

    /* METRICS (Big Green Numbers) */
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        color: #00b894;
        font-weight: 700;
    }
    
    /* TABS STYLING */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f8f9fa;
        border-radius: 10px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e6fffa;
        border-bottom: 2px solid #00b894;
    }

    /* BUTTONS (Gradient) */
    div.stButton > button {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        color: white !important;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 600;
        width: 100%;
        box-shadow: 0 4px 10px rgba(56, 239, 125, 0.3);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
    }

    /* HIDE JUNK */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. LOGIN SCREEN
# ---------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_screen():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="gradient-text">ResellerLens</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>AI Power for Modern Sellers</p>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2, col3 = st.columns([1,8,1])
    with col2:
        password = st.text_input("Access Code", type="password", placeholder="Enter Invite Code...", label_visibility="collapsed")
        if st.button("Unlock Dashboard 🚀"):
            if password == "MONEY2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.toast("❌ Invalid Code")

# ---------------------------------------------------------
# 4. MAIN APP
# ---------------------------------------------------------
def main_app():
    # Header
    st.markdown('<div class="gradient-text">ResellerLens</div>', unsafe_allow_html=True)
    
    # AI Setup
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if not api_key:
            st.error("⚠️ API Key Missing")
            return
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
    except:
        st.error("Connection Error")
        return

    # --- NAVIGATION TABS (Visible on Mobile) ---
    tab1, tab2, tab3 = st.tabs(["🔥 Profit", "📸 Studio", "⚙️ Settings"])

    # --- TAB 1: PROFIT MACHINE ---
    with tab1:
        st.markdown("### ⚡ Instant Listing")
        
        # 1. Upload
        uploaded_file = st.file_uploader("Product Photo", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")
        
        if uploaded_file:
            st.image(uploaded_file, caption="Preview", use_column_width=True)
            
            # 2. Cost Input
            col_a, col_b = st.columns(2)
            with col_a:
                st.write("**Cost Price (₹)**")
            with col_b:
                cost_price = st.number_input("Cost", min_value=0, step=50, value=0, label_visibility="collapsed")
            
            # 3. Generate Button
            if st.button("Analyze & Write Listing ✨"):
                with st.spinner("🔍 Scanning market value..."):
                    try:
                        img = Image.open(uploaded_file)
                        prompt = f"""
                        Act as an Indian Reseller.
                        Cost Price: ₹{cost_price}
                        
                        Analyze this image. Output EXACTLY with separators:
                        
                        EST_PRICE: [Number only, e.g. 1500]
                        CAPTION: [Catchy Instagram caption with hashtags]
                        TITLE: [OLX Title]
                        DESC: [OLX Description]
                        TIP: [One flip tip]
                        """
                        response = model.generate_content([prompt, img])
                        text = response.text
                        
                        # Parse Price
                        est_price = "0"
                        if "EST_PRICE:" in text:
                            est_price = text.split("EST_PRICE:")[1].split("\n")[0].strip().replace("₹", "").replace(",", "")

                        # --- FINANCIALS ---
                        st.divider()
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Cost", f"₹{cost_price}")
                        m2.metric("Value", f"₹{est_price}")
                        try:
                            profit = float(est_price) - cost_price
                            m3.metric("Profit", f"₹{profit}")
                            if profit > 0: st.balloons()
                        except:
                            m3.metric("Profit", "N/A")
                        st.divider()

                        # --- OUTPUTS ---
                        st.info("📱 Social Caption")
                        try:
                            st.code(text.split("CAPTION:")[1].split("TITLE:")[0].strip(), language="text")
                        except: st.write(text)

                        st.success("💼 Marketplace Details")
                        try:
                            st.text_input("Title", text.split("TITLE:")[1].split("DESC:")[0].strip())
                            st.text_area("Description", text.split("DESC:")[1].split("TIP:")[0].strip())
                        except: pass

                    except Exception as e:
                        st.error("Please try a clearer photo.")

    # --- TAB 2: PHOTO STUDIO ---
    with tab2:
        st.markdown("### 🎬 Photo Director")
        st.info("Upload a bad photo to get 3 tips to fix it.")
        
        coach_file = st.file_uploader("Upload Image", key="coach")
        if coach_file:
            st.image(coach_file, width=200)
            if st.button("Critique My Shot 🔍"):
                with st.spinner("Analyzing lighting..."):
                    img = Image.open(coach_file)
                    res = model.generate_content(["Act as a pro photographer. Give 3 short, specific tips to improve this photo.", img])
                    st.warning(res.text)

    # --- TAB 3: SETTINGS ---
    with tab3:
        st.write("### Profile")
        st.write("Plan: **Pro Reseller**")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

# ---------------------------------------------------------
# 5. RUN
# ---------------------------------------------------------
if not st.session_state.logged_in:
    login_screen()
else:
    main_app()
        
