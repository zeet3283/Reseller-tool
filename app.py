import streamlit as st
import google.generativeai as genai
import pandas as pd
import time
from PIL import Image

# ---------------------------------------------------------
# 1. APP CONFIGURATION (Must be first)
# ---------------------------------------------------------
st.set_page_config(
    page_title="ResellerLens AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# ---------------------------------------------------------
# 2. CUSTOM CSS (The "High Contrast" Fix)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Force Background to White and Text to Black */
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    
    /* Force Input Fields to have visible text */
    .stTextInput>div>div>input {
        color: #000000;
        background-color: #f0f2f6;
    }
    
    /* Force Headers to be Black */
    h1, h2, h3, h4, h5, h6, p, span {
        color: #000000 !important;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mobile-Friendly Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background-color: #000000;
        color: #ffffff !important; /* Button text must remain white */
        height: 50px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)
# ---------------------------------------------------------
# 3. SESSION STATE (Remembering User Data)
# ---------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'api_key' not in st.session_state:
    # In a real app, you would use st.secrets here
    st.session_state.api_key = "" 

# ---------------------------------------------------------
# 4. LOGIN SCREEN
# ---------------------------------------------------------
def login_screen():
    st.markdown("<h1 style='text-align: center;'>✨ ResellerLens</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Professional AI Listing Tool</p>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    
    with st.container():
        # Using a card-like layout
        password = st.text_input("Enter Access Code", type="password", placeholder="••••••••")
        
        # NOTE: In production, store this key in Streamlit Secrets, not here!
        user_key = st.text_input("Enter Your Google API Key", type="password", placeholder="AIzaSy...")
        
        if st.button("Unlock Tool 🔓"):
            if password == "MONEY2026" and len(user_key) > 10:
                st.session_state.logged_in = True
                st.session_state.api_key = user_key
                st.rerun()
            elif password != "MONEY2026":
                st.error("❌ Invalid Access Code. Please purchase a license.")
            else:
                st.error("⚠️ Please enter a valid API Key.")

# ---------------------------------------------------------
# 5. MAIN APPLICATION
# ---------------------------------------------------------
def main_app():
    # Setup AI
    genai.configure(api_key=st.session_state.api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    # Top Navigation
    tab1, tab2, tab3 = st.tabs(["🚀 Instant", "📦 Batch", "📸 Coach"])

    # --- TAB 1: INSTANT LISTING ---
    with tab1:
        st.write("### ⚡ Quick List")
        uploaded_file = st.file_uploader("Upload Item Photo", type=['jpg', 'png', 'jpeg'], key="t1")
        
        if uploaded_file and st.button("Generate Listing ✨", key="b1"):
            with st.spinner("Analyzing item details..."):
                try:
                    image = Image.open(uploaded_file)
                    st.image(image, caption='Your Item', use_column_width=True)
                    
                    prompt = """
                    You are an expert Indian reseller. 
                    OUTPUT 1: 📱 INSTAGRAM/WHATSAPP (Short caption, emojis, Price in ₹, 'DM to buy')
                    OUTPUT 2: 💼 OLX/QUICKR (Professional Title, Condition, Description, Price ₹)
                    OUTPUT 3: 💡 FLIP TIP (One specific tip to sell faster)
                    """
                    response = model.generate_content([prompt, image])
                    st.success("Analysis Complete!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

    # --- TAB 2: BATCH INVENTORY ---
    with tab2:
        st.write("### 🏭 Bulk Inventory")
        st.info("Upload multiple photos to generate an Excel sheet.")
        uploaded_files = st.file_uploader("Select Photos", accept_multiple_files=True, type=['jpg', 'png'], key="t2")
        
        if uploaded_files and st.button("Process All 📦", key="b2"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            inventory_data = []
            
            for i, file in enumerate(uploaded_files):
                status_text.text(f"Processing image {i+1} of {len(uploaded_files)}...")
                image = Image.open(file)
                
                try:
                    prompt = "Output ONLY: Title | Price (₹) | Description | Flip Tip"
                    response = model.generate_content([prompt, image])
                    text = response.text.strip()
                    parts = text.split('|')
                    if len(parts) >= 4:
                        inventory_data.append({
                            "Title": parts[0], "Price": parts[1], 
                            "Description": parts[2], "Tip": parts[3]
                        })
                except:
                    pass
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            if inventory_data:
                df = pd.DataFrame(inventory_data)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Download Excel CSV",
                    csv,
                    "inventory.csv",
                    "text/csv",
                    key='download-csv'
                )
                st.success("Batch processing done!")

    # --- TAB 3: PHOTO COACH ---
    with tab3:
        st.write("### 🎬 Photo Director")
        st.info("Get AI advice on how to take better product shots.")
        coach_file = st.file_uploader("Upload Shot to Analyze", type=['jpg', 'png'], key="t3")
        
        if coach_file and st.button("Analyze Quality 🔍", key="b3"):
            with st.spinner("Critiquing photo..."):
                image = Image.open(coach_file)
                st.image(image, use_column_width=True)
                prompt = "Act as a pro photographer. Give 3 specific commands to improve this photo's lighting, angle, or background."
                response = model.generate_content([prompt, image])
                st.warning(response.text)

# ---------------------------------------------------------
# 6. APP LOGIC
# ---------------------------------------------------------
if not st.session_state.logged_in:
    login_screen()
else:
    main_app()
  
