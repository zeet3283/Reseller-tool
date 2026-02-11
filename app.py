import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image

# ---------------------------------------------------------
# 1. APP CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="ResellerLens",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. HIGH-CONTRAST CSS (Fixes Invisible Text)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* 1. Force Background White, Text Black */
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    
    /* 2. Fix Input Fields (Grey background, Black text) */
    .stTextInput>div>div>input {
        color: #000000 !important;
        background-color: #f0f2f6 !important;
        border: 1px solid #ddd;
    }
    
    /* 3. Fix Headers & Labels */
    h1, h2, h3, h4, p, label {
        color: #000000 !important;
    }
    
    /* 4. THE BUTTON FIX (Black Button, White Text) */
    .stButton>button {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: none;
        border-radius: 8px;
        height: 50px;
        width: 100%;
        font-weight: bold;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #333333 !important;
        color: #ffffff !important;
    }
    
    /* 5. Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. SETUP & LOGIN
# ---------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_screen():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: black;'>✨ ResellerLens</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: grey;'>Professional AI Listing Tool</p>", unsafe_allow_html=True)
    
    st.write("")
    
    # Simple Password Field
    password = st.text_input("Enter Access Code", type="password", placeholder="••••••••")
    
    st.write("")
    
    if st.button("Login 🔐"):
        if password == "MONEY2026":  # Change this password if you want!
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Incorrect Access Code")

# ---------------------------------------------------------
# 4. MAIN APP LOGIC
# ---------------------------------------------------------
def main_app():
    # Load Key from Secrets (Invisible to user)
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
    except:
        st.error("⚠️ Server Error: API Key missing. Please check Streamlit Secrets.")
        return

    # Tabs Interface
    tab1, tab2, tab3 = st.tabs(["🚀 Social", "📦 Inventory", "🎬 Coach"])

    # --- TAB 1: SOCIAL ---
    with tab1:
        st.markdown("### ⚡ Instant Listing")
        uploaded_file = st.file_uploader("Upload Item", type=['jpg', 'jpeg', 'png'], key="t1")
        if uploaded_file and st.button("Generate ✨", key="b1"):
            with st.spinner("Writing caption..."):
                try:
                    img = Image.open(uploaded_file)
                    st.image(img, width=200)
                    prompt = "You are an Indian Reseller. Write a short, catchy Instagram caption with Price (₹) and hashtags."
                    response = model.generate_content([prompt, img])
                    st.success("Copy this text:")
                    st.code(response.text, language=None)
                except Exception as e:
                    st.error(f"Error: {e}")

    # --- TAB 2: INVENTORY ---
    with tab2:
        st.markdown("### 🏭 Batch Mode")
        files = st.file_uploader("Upload 5-10 Photos", accept_multiple_files=True, key="t2")
        if files and st.button("Process All 📦", key="b2"):
            status = st.empty()
            data = []
            bar = st.progress(0)
            
            for i, f in enumerate(files):
                status.write(f"Scanning item {i+1}...")
                try:
                    img = Image.open(f)
                    res = model.generate_content(["Output ONLY: Title | Price(₹) | Desc | Tip", img])
                    parts = res.text.split('|')
                    if len(parts) >= 4:
                        data.append({"Title": parts[0], "Price": parts[1], "Desc": parts[2]})
                except:
                    pass
                bar.progress((i+1)/len(files))
            
            if data:
                status.success("Done!")
                df = pd.DataFrame(data)
                st.dataframe(df)
                st.download_button("Download CSV", df.to_csv(), "stock.csv")

    # --- TAB 3: COACH ---
    with tab3:
        st.markdown("### 🎬 Photo Director")
        f = st.file_uploader("Check Photo Quality", key="t3")
        if f and st.button("Analyze 🔍", key="b3"):
            img = Image.open(f)
            st.image(img, width=200)
            res = model.generate_content(["Act as a pro photographer. Give 3 tips to fix this photo.", img])
            st.info(res.text)

# ---------------------------------------------------------
# 5. RUN
# ---------------------------------------------------------
if not st.session_state.logged_in:
    login_screen()
else:
    main_app()
    
