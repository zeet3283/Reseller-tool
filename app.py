import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image
import os

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
# 2. UI STYLING (The Button Fix)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Force standard text visibility */
    .stApp { background-color: white; color: black; }
    
    /* FIX THE BUTTONS: Black background, White text */
    div.stButton > button {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: none;
        padding: 10px 20px;
        border-radius: 10px;
        width: 100%;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #333333 !important;
        color: #ffffff !important;
    }
    
    /* Hide menus */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. SECURE LOGIN (No API Key Box)
# ---------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_screen():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>✨ ResellerLens</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: grey;'>AI Listing Tool</p>", unsafe_allow_html=True)
    
    st.write("")
    password = st.text_input("Enter Access Code", type="password", placeholder="••••••••")
    st.write("")
    
    if st.button("Login 🔐"):
        if password == "MONEY2026":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Invalid Code")

# ---------------------------------------------------------
# 4. MAIN APP
# ---------------------------------------------------------
def main_app():
    # Load the Secret Key automatically
    try:
        # Tries to get key from Secrets; falls back to empty if missing to prevent crash
        api_key = st.secrets.get("GOOGLE_API_KEY") 
        if not api_key:
            st.error("⚠️ SYSTEM ERROR: Google API Key is missing in Secrets.")
            st.info("Go to Streamlit Dashboard > App > Settings > Secrets to add it.")
            return
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return

    # TABS
    tab1, tab2 = st.tabs(["🚀 Instant List", "🎬 Photo Coach"])

    # INSTANT LISTING
    with tab1:
        st.write("### Upload Product Photo")
        uploaded_file = st.file_uploader(" ", type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file:
            st.image(uploaded_file, caption="Preview", width=200)
            if st.button("Generate Listing ✨"):
                with st.spinner("Writing magic..."):
                    try:
                        img = Image.open(uploaded_file)
                        prompt = """
                        You are an expert Indian Reseller.
                        OUTPUT 1: 📱 Instagram Caption (Catchy, Emoji, Price ₹, Hashtags)
                        OUTPUT 2: 💼 OLX Listing (Title, Condition, Desc, Price ₹)
                        OUTPUT 3: 💡 Quick Flip Tip
                        """
                        response = model.generate_content([prompt, img])
                        st.success("Listing Ready!")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"AI Error: {e}")

    # PHOTO COACH
    with tab2:
        st.write("### Check Photo Quality")
        coach_file = st.file_uploader(" ", key="coach", type=['jpg', 'jpeg', 'png'])
        if coach_file and st.button("Analyze Photo 🔍"):
            img = Image.open(coach_file)
            st.image(img, width=200)
            res = model.generate_content(["Act as a pro photographer. Give 3 tips to improve this shot.", img])
            st.info(res.text)

# ---------------------------------------------------------
# 5. RUN
# ---------------------------------------------------------
if not st.session_state.logged_in:
    login_screen()
else:
    main_app()
    
