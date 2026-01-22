import streamlit as st
import os
import base64
from utils.styles import load_css

# Import Views (Ensure you have created these files in the 'views' folder)
from views import eis, revenue
# Note: Create legal.py and admin.py in 'views' folder to uncomment these
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
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # --- LOGO LOGIC (Robust Path Checking) ---
    # Check both common locations for the logo
    logo_path = "assets/image_11b1c9.jpg"
    if not os.path.exists(logo_path):
        logo_path = "image_11b1c9.jpg" # Fallback to root

    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            # Use Flexbox to force perfect centering
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 20px;">
                    <img src="data:image/jpeg;base64,{encoded}" style="width: 150px; max-width: 80%; border-radius: 50%;">
                </div>
                """, 
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Error loading logo: {e}")
    else:
        # Fallback Icon if image is totally missing
        st.markdown("<h1 style='text-align:center; font-size: 80px;'>🏛️</h1>", unsafe_allow_html=True)
    
    # --- LOGIN FORM (Centered) ---
    c1, c2, c3 = st.columns([1, 1.5, 1]) # Adjusted ratio for better centering on desktop
    with c2:
        st.markdown('<div class="login-box"><h2 style="text-align: center;">🔐 เข้าสู่ระบบ</h2>', unsafe_allow_html=True)
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        
        if st.button("Sign In", use_container_width=True):
            # Auth Logic
            if user == "admin" and pw == "admin123":
                st.session_state.logged_in, st.session_state.role = True, "Admin"
                st.rerun()
            elif user == "superuser" and pw == "superuser1234":
                st.session_state.logged_in, st.session_state.role = True, "Superuser"
                st.rerun()
            elif user == "user" and pw == "user123":
                st.session_state.logged_in, st.session_state.role = True, "User"
                st.rerun()
            else:
                st.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
        st.markdown('</div>', unsafe_allow_html=True)

# 4. Main Router
if not st.session_state.logged_in:
    login_page()
else:
    # Sidebar
    st.sidebar.title(f"👤 {st.session_state.username}")
    st.sidebar.write(f"Role: **{st.session_state.role}**")
    
    # Menu Configuration
    menu_options = {
        "EIS Dashboard": eis.show_view,
        "Revenue Dashboard": revenue.show_view,
    }
    
    # Add restricted dashboards based on role
    if st.session_state.role in ["Superuser", "Admin"]:
        # Ensure 'views/legal.py' exists before uncommenting
        # from views import legal 
        # menu_options["Legal Dashboard"] = legal.show_view
        pass 

    if st.session_state.role == "Admin":
        # Ensure 'views/admin.py' exists before uncommenting
        # from views import admin
        # menu_options["Admin Panel"] = admin.show_view
        pass

    if st.sidebar.button("Log off"):
        st.session_state.logged_in = False
        st.rerun()

    st.sidebar.divider()
    selection = st.sidebar.radio("เลือกเมนู:", list(menu_options.keys()))
    
    # Run the selected function
    if selection in menu_options:
        menu_options[selection]()
