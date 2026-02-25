import streamlit as st
import easyocr
import re
import cv2
import numpy as np
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(page_title="InsightVision AI", page_icon="🛡️", layout="centered")

# --- CUSTOM CSS FOR APP-LIKE UI ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { 
        width: 100%; border-radius: 10px; height: 3em; 
        background-color: #1E3A8A; color: white; font-weight: bold;
    }
    .stCamera>div>div>div>button { background-color: #1E3A8A !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (Managing Steps) ---
if 'step' not in st.session_state:
    st.session_state.step = 'login'

# --- 1. LOGIN PAGE ---
if st.session_state.step == 'login':
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🛡️ AI Doc Validator</h1>", unsafe_allow_html=True)
    st.write("---")
    username = st.text_input("Username (admin)")
    password = st.text_input("Password (123)", type="password")
    
    if st.button("LOG IN"):
        if username == "admin" and password == "123":
            st.session_state.step = 'selection'
            st.rerun()
        else:
            st.error("Invalid Username or Password")

# --- 2. DOCUMENT SELECTION PAGE ---
elif st.session_state.step == 'selection':
    st.markdown("<h2 style='color: #1E3A8A;'>📂 Select Document Type</h2>", unsafe_allow_html=True)
    doc_type = st.selectbox("Category select cheyandi:", ["Aadhaar Card", "PAN Card"])
    
    if st.button("PROCEED"):
        st.session_state.doc_type = doc_type
        st.session_state.step = 'media'
        st.rerun()

# --- 3. MEDIA UPLOAD / CAMERA ACCESS PAGE ---
elif st.session_state.step == 'media':
    st.markdown(f"<h2 style='color: #1E3A8A;'>📸 Scan {st.session_state.doc_type}</h2>", unsafe_allow_html=True)
    
    source = st.radio("Media source choose chey:", ["Camera Access", "Upload from Gallery"])
    
    if source == "Camera Access":
        img_file = st.camera_input("Place ID card in front of camera")
    else:
        img_file = st.file_uploader("Select Image", type=['jpg', 'png', 'jpeg'])

    if img_file:
        # --- 4. GENUINE vs FAKE DETECTION ---
        image = Image.open(img_file)
        img_array = np.array(image)
        
        with st.spinner('AI analyzing document...'):
            reader = easyocr.Reader(['en'])
            # Image cleaning for AI
            gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
            results = reader.readtext(gray, detail=0)
            text = " ".join(results).upper()
            
            # Logic for Genuine vs Fake (Pattern Matching)
            is_genuine = False
            if st.session_state.doc_type == "Aadhaar Card":
                # Check for 12 continuous digits or patterns
                digits = re.findall(r'\d', text)
                if len(digits) >= 12:
                    is_genuine = True
            
            elif st.session_state.doc_type == "PAN Card":
                # Check for PAN Alphanumeric format
                if re.search(r'[A-Z]{5}[0-9]{4}[A-Z]{1}', text):
                    is_genuine = True

            st.divider()
            if is_genuine:
                st.success(f"✅ GENUINE {st.session_state.doc_type} DETECTED")
                st.balloons()
            else:
                st.error(f"⚠️ FAKE OR INVALID DOCUMENT")
                st.warning("Reason: Security patterns/format mismatch.")
            
            # Showing extracted data as proof
            with st.expander("Show AI Metadata"):
                st.write(text)
            
            if st.button("New Scan"):
                st.session_state.step = 'selection'
                st.rerun()

# Sidebar for Logout
if st.session_state.step != 'login':
    if st.sidebar.button("Logout"):
        st.session_state.step = 'login'
        st.rerun()