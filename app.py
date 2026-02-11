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
# 2. ULTRA-MODERN CSS (The Polish)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* IMPORT MODERN FONT */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* GRADIENT BACKGROUND FOR HEADER */
    .stAppHeader {
        background-color: transparent;
    }
    
    /* CUSTOM CARD DESIGN */
    .css-1r6slb0 {
        background-color: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
    }
    
    /* SUCCESS METRICS (Green Text) */
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        color: #00b894;
        font-weight: 700;
    }
    
    /* BUTTON STYLING (Gradient & Shadow) */
    div.stButton > button {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        color: white !important;
        border: none;
        padding: 15px 30px;
        border-radius: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(56, 239, 125, 0.4);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(56, 239, 125, 0.6);
    }
    
    /* INPUT FIELDS */
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 10px;
        color: #333;
    }

    /* HIDE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. HELPER LOGIC
# ---------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_screen():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #333; margin-bottom:0;'>ResellerLens</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888; font-size: 14px;'>The AI Advantage for Modern Sellers</p>", unsafe_allow_html=True)
        st.divider()
        
        # Login Box
        password = st.text_input("Access Code", type="password", placeholder="Enter your invite code...", label_visibility="collapsed")
        
        if st.button("Enter Dashboard 🚀", use_container_width=True):
            if password == "MONEY2026":
                st.success("Access Granted")
                time.sleep(0.5)
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.toast("❌ Invalid Code. Please try again.")

# ---------------------------------------------------------
# 4. MAIN APP LOGIC
# ---------------------------------------------------------
def main_app():
    # --- SIDEBAR (Navigation) ---
    with st.sidebar:
        st.title("💎 ResellerLens")
        st.write("v11.0 Pro Edition")
        st.divider()
        mode = st.radio("Navigation", ["🔥 Profit Machine", "📸 Photo Studio", "⚙️ Settings"])
        st.divider()
        st.info("💡 **Tip:** Clear photos = 20% higher price.")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # Setup AI
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if not api_key:
            st.error("⚠️ API Key Missing in Secrets")
            return
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
    except:
        return

    # --- PAGE 1: PROFIT MACHINE ---
    if mode == "🔥 Profit Machine":
        st.markdown("### ⚡ Instant Listing Generator")
        st.markdown("Upload a photo to generate listings and calculate profit margins.")
        
        # 1. IMAGE UPLOAD
        with st.container():
            uploaded_file = st.file_uploader("Upload Product", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")
        
        if uploaded_file:
            # Layout: Image on Left, Inputs on Right (Desktop) / Stacked (Mobile)
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(uploaded_file, use_column_width=True, caption="Preview")
            
            with col2:
                cost_price = st.number_input("💸 Cost Price (What you paid)", min_value=0, step=50, value=0)
                
                if st.button("Analyze & Write Listing ✨", use_container_width=True):
                    with st.spinner("🔍 AI is researching market value..."):
                        try:
                            img = Image.open(uploaded_file)
                            
                            # PROMPT
                            prompt = f"""
                            Act as a professional reseller.
                            Cost Price: ₹{cost_price}
                            
                            Analyze this item image.
                            
                            Output EXACTLY in this format with separators:
                            
                            ESTIMATED_PRICE: [Just the number in rupees, e.g. 1500]
                            SOCIAL_POST: [Write a 2-line catchy caption with emojis]
                            OLX_TITLE: [SEO Friendly Title]
                            OLX_DESC: [Professional description, condition, and details]
                            PROFIT_TIP: [One expert tip to flip this fast]
                            """
                            
                            response = model.generate_content([prompt, img])
                            text = response.text
                            
                            # Simple Parsing (Robust)
                            est_price = "0"
                            try:
                                for line in text.split('\n'):
                                    if "ESTIMATED_PRICE:" in line:
                                        est_price = line.split(":")[1].strip().replace("₹", "").replace(",", "")
                            except:
                                est_price = "0"

                            # --- RESULTS DASHBOARD ---
                            st.divider()
                            st.markdown("### 💰 Financial Breakdown")
                            
                            # THE BIG METRICS ROW
                            m1, m2, m3 = st.columns(3)
                            m1.metric("Your Cost", f"₹{cost_price}")
                            m2.metric("Market Value", f"₹{est_price}")
                            
                            # Profit Calc
                            try:
                                profit = float(est_price) - cost_price
                                m3.metric("Net Profit", f"₹{profit}", delta=f"{profit} Profit")
                                if profit > 0:
                                    st.balloons()
                            except:
                                m3.metric("Profit", "Calc Error")
                            
                            st.divider()
                            
                            # TABS FOR CONTENT
                            t1, t2 = st.tabs(["📱 Social Media", "💼 OLX / Amazon"])
                            
                            with t1:
                                st.info("Copy this for Instagram/WhatsApp Status:")
                                try:
                                    content = text.split("SOCIAL_POST:")[1].split("OLX_TITLE:")[0].strip()
                                    st.code(content, language="text")
                                    st.markdown(f"**💡 Pro Tip:** {text.split('PROFIT_TIP:')[1].strip()}")
                                except:
                                    st.write(text) # Fallback if parsing fails
                                
                            with t2:
                                try:
                                    title = text.split("OLX_TITLE:")[1].split("OLX_DESC:")[0].strip()
                                    desc = text.split("OLX_DESC:")[1].split("PROFIT_TIP:")[0].strip()
                                    st.text_input("Title", title)
                                    st.text_area("Description", desc, height=150)
                                except:
                                    st.write("Could not parse perfectly. See below:")
                                    st.write(text)
                            
                        except Exception as e:
                            st.error("AI Error. Please try a clearer photo.")

    # --- PAGE 2: PHOTO STUDIO ---
    elif mode == "📸 Photo Studio":
        st.markdown("### 🎬 AI Photo Director")
        st.info("Bad photos cost you money. Upload a shot here to get a professional critique.")
        
        coach_file = st.file_uploader("Upload Image", key="coach")
        if coach_file:
            st.image(coach_file, width=200)
            if st.button("Critique My Shot 🔍"):
                with st.spinner("Analyzing lighting and angles..."):
                    img = Image.open(coach_file)
                    res = model.generate_content(["Act as a harsh but helpful product photographer. Give 3 short, specific tips to improve this photo.", img])
                    st.warning(res.text)

    # --- PAGE 3: SETTINGS ---
    elif mode == "⚙️ Settings":
        st.write("### Account Settings")
        st.write("Plan: **Pro Reseller**")
        st.write("Valid until: **Lifetime Access**")
        st.button("Contact Support")

# ---------------------------------------------------------
# 5. RUN APP
# ---------------------------------------------------------
if not st.session_state.logged_in:
    login_screen()
else:
    main_app()
                                        
