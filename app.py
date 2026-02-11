import streamlit as st
import google.generativeai as genai
from PIL import Image
import random

# ---------------------------------------------------------
# 1. APP CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="ResellerLens Pro",
    page_icon="💸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. MODERN CSS (Gradients, Shadows, Cards)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* GLOBAL FONTS & BACKGROUND */
    .stApp {
        background-color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* GRADIENT TEXT HEADER */
    .gradient-text {
        background: -webkit-linear-gradient(45deg, #FF512F, #DD2476);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3em;
        text-align: center;
        margin-bottom: 0px;
    }
    
    /* SUBTITLE */
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    
    /* MODERN CARDS (Glassmorphism) */
    .card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid #eee;
        margin-bottom: 20px;
    }
    
    /* BUTTON STYLING (Gradient) */
    div.stButton > button {
        background: linear-gradient(45deg, #FF512F, #DD2476);
        color: white !important;
        border: none;
        padding: 12px 24px;
        border-radius: 50px; /* Pill shape */
        width: 100%;
        font-weight: bold;
        font-size: 16px;
        transition: transform 0.2s;
        box-shadow: 0 5px 15px rgba(221, 36, 118, 0.3);
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        color: white !important;
    }
    
    /* INPUT FIELDS */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #ddd;
        padding: 10px;
    }

    /* HIDE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. HELPER FUNCTIONS
# ---------------------------------------------------------
def get_motivation():
    quotes = [
        "💰 One man's trash is another man's treasure.",
        "🚀 List it today, cash it tomorrow.",
        "✨ Good photos = Fast money.",
        "🔥 The hustle never stops.",
        "💎 You are sitting on a goldmine. Sell it.",
        "📸 Snap. List. Profit. Repeat."
    ]
    return random.choice(quotes)

# ---------------------------------------------------------
# 4. LOGIN SCREEN (The "Exclusive" Gate)
# ---------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_screen():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f'<div class="gradient-text">ResellerLens</div>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your AI Sales Assistant</p>', unsafe_allow_html=True)
    
    # Login Card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("### 🔐 Member Access")
    password = st.text_input("Enter Access Code", type="password", placeholder="••••••••", label_visibility="collapsed")
    
    if st.button("Unlock Dashboard 🚀"):
        if password == "MONEY2026":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Access Denied. Incorrect Code.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. MAIN DASHBOARD
# ---------------------------------------------------------
def main_app():
    # Load API Key
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if not api_key:
            st.error("⚠️ Server Error: API Key missing in Secrets.")
            return
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        st.error(f"Setup Error: {e}")
        return

    # --- HEADER SECTION ---
    st.markdown(f'<div class="gradient-text">ResellerLens</div>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">{get_motivation()}</p>', unsafe_allow_html=True)

    # --- INSTRUCTIONS (Collapsible) ---
    with st.expander("ℹ️  New here? Click for Instructions"):
        st.markdown("""
        **How to turn photos into cash:**
        1.  **Tap 'Instant Sell'** below.
        2.  **Upload a photo** of any item (shoe, watch, shirt).
        3.  **Wait 5 seconds** for the AI to write your listing.
        4.  **Copy & Paste** to Instagram, WhatsApp, or OLX!
        
        *Tip: Use the 'Photo Lab' tab if your pictures look dark or blurry.*
        """)

    # --- MAIN TABS ---
    tab1, tab2 = st.tabs(["🔥 Instant Sell", "📸 Photo Lab"])

    # --- TAB 1: SELLING TOOL ---
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("### 📤 Upload Product")
        
        uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")
        
        if uploaded_file:
            # Show image preview nicely
            st.image(uploaded_file, caption="Ready to analyze", use_column_width=True, channels="RGB")
            
            if st.button("Generate Magic Listing ✨"):
                with st.spinner("🧠 AI is analyzing brand, condition & price..."):
                    try:
                        img = Image.open(uploaded_file)
                        prompt = """
                        You are a top-tier Indian Reseller and Copywriter.
                        Analyze this image deeply.
                        
                        OUTPUT 1: 📱 INSTAGRAM/WHATSAPP STORY
                        - Write a hype caption. Use emojis.
                        - State the Price clearly in ₹ (Rupees).
                        - End with a Call to Action.
                        
                        OUTPUT 2: 💼 MARKETPLACE LISTING (OLX/Facebook)
                        - Title: (SEO Optimized)
                        - Condition: (X/10)
                        - Description: (Professional, mention flaws if any)
                        - Price Estimate: (₹ Range)
                        
                        OUTPUT 3: 💡 PRO FLIP TIP
                        - Give one specific tip to sell THIS item faster.
                        """
                        response = model.generate_content([prompt, img])
                        
                        # Success Box
                        st.success("✅ Analysis Complete!")
                        st.markdown(response.text)
                        st.balloons() # Fun animation!
                        
                    except Exception as e:
                        st.error(f"AI Brain Freeze: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 2: PHOTO COACH ---
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("### 🎨 Fix Your Photos")
        st.info("Bad photos cost you money. Upload a shot here to get a critique.")
        
        coach_file = st.file_uploader("Upload for review", key="coach", type=['jpg', 'jpeg', 'png'])
        
        if coach_file and st.button("Analyze Quality 🔍"):
            with st.spinner("Checking lighting & angles..."):
                img = Image.open(coach_file)
                st.image(img, use_column_width=True)
                
                res = model.generate_content(["Act as a harsh but helpful pro photographer. Give 3 specific commands to improve this photo (Lighting, Background, Angle).", img])
                
                st.warning("📸 **Director's Feedback:**")
                st.markdown(res.text)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. APP ENTRY POINT
# ---------------------------------------------------------
if not st.session_state.logged_in:
    login_screen()
else:
    main_app()
    
