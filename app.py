import streamlit as st
import os
import base64
from utils.styles import load_css

# Import Views
from views import eis, revenue
# Note: Create legal.py and admin.py in views folder to uncomment these
# from views import legal, admin 

# 1. Config
st.set_page_config(page_title="EIS Platform", layout="wide", page_icon="🏛️")
load_css()

# 2. Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = ""

# 3. Login Page Logic
def login_page():
    st.markdown("<br>", unsafe_allow_html=True)
    # Load Logo for Login
    logo_path = "assets/image_11b1c9.jpg"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(f"""<div style="display: flex; justify-content: center; margin-bottom: 20px;"><img src="data:image/jpeg;base64,{encoded}" style="width: 150px;"></div>""", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
    with c2:
        st.markdown('<div class="login-box"><h2 style="text-align: center;">🔐 เข้าสู่ระบบ</h2></div>', unsafe_allow_html=True)
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Sign In", use_container_width=True):
            if user == "admin" and pw == "admin123":
                st.session_state.logged_in, st.session_state.role = True, "Admin"
                st.rerun()
            elif user == "user" and pw == "user123":
                st.session_state.logged_in, st.session_state.role = True, "User"
                st.rerun()
            else:
                st.error("Login Failed")

# 4. Main Router
if not st.session_state.logged_in:
    login_page()
else:
    # Sidebar
    st.sidebar.title(f"👤 {st.session_state.role}")
    
    # Menu Configuration
    menu_options = {
        "EIS Dashboard": eis.show_view,
        "Revenue Dashboard": revenue.show_view,
        # "Legal Dashboard": legal.show_view, 
        # "Admin Panel": admin.show_view
    }
    
    if st.sidebar.button("Log off"):
        st.session_state.logged_in = False
        st.rerun()

    st.sidebar.divider()
    selection = st.sidebar.radio("เลือกเมนู:", list(menu_options.keys()))
    
    # Run the selected function
    menu_options[selection]()
