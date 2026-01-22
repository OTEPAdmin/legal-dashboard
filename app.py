import streamlit as st
import os
import base64
import datetime
import time
from utils.styles import load_css
from utils.data_loader import load_data_from_excel

# Import Cookie Manager
import extra_streamlit_components as stx

# Import Views
from views import eis, revenue

# 1. CONFIGURATION
st.set_page_config(page_title="ระบบศูนย์ข้อมูลกลาง สกสค.", layout="wide", page_icon="🏛️")
load_css()

# --- COOKIE MANAGER SETUP ---
cookie_manager = stx.CookieManager()

# 2. SESSION STATE & AUTO-LOGIN CHECK
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = ""

# Try to auto-login from Cookie (if not already logged in)
if not st.session_state.logged_in:
    try:
        cookie_user = cookie_manager.get(cookie="user_session")
        if cookie_user:
            if cookie_user == "admin":
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.session_state.username = "Administrator"
            elif cookie_user == "user":
                st.session_state.logged_in = True
                st.session_state.role = "User"
                st.session_state.username = "General User"
            
            if st.session_state.logged_in:
                time.sleep(0.1)
                st.rerun()
                
    except Exception as e:
        print(f"Cookie read error: {e}")

# 3. LOGIN PAGE LOGIC
def login_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # --- LOGO LOGIC ---
    LOGO_FILENAME = "image_11b1c9.jpg"
    logo_path = "assets/" + LOGO_FILENAME
    if not os.path.exists(logo_path):
        logo_path = LOGO_FILENAME

    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 10px;">
                    <img src="data:image/jpeg;base64,{encoded}" style="width: 150px; max-width: 80%; border-radius: 50%;">
                </div>
                """, 
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Error loading logo: {e}")
    else:
        st.markdown("<h1 style='text-align:center; font-size: 80px;'>🏛️</h1>", unsafe_allow_html=True)
    
    # --- NEW HEADER TEXT (No Lock, No Box) ---
    st.markdown(
        """
        <h1 style='text-align: center; margin-bottom: 0px; font-weight: bold;'>ยินดีต้อนรับ</h1>
        <h3 style='text-align: center; margin-top: 5px; margin-bottom: 30px; font-weight: normal;'>ระบบศูนย์ข้อมูลกลาง สกสค.</h3>
        """,
        unsafe_allow_html=True
    )
    
    # --- LOGIN FORM ---
    # Using [1, 1.2, 1] ratio to keep the form centered but not too wide
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        # Note: 'login-box' div removed to remove the background card style
        st.caption("⚠️ **ชื่อผู้ใช้และรหัสผ่านต้องระบุตัวพิมพ์เล็ก-ใหญ่ให้ถูกต้อง** (Case Sensitive)")
        
        user = st.text_input("ชื่อผู้ใช้ (Username)")
        pw = st.text_input("รหัสผ่าน (Password)", type="password")
        remember = st.checkbox("จำรหัสผ่านไว้ 10 วัน (Remember me 10 days)")
        
        if st.button("เข้าสู่ระบบ (Sign In)", use_container_width=True):
            # Auth Logic
            valid_user = None
            role_name = ""
            display_name = ""
            
            if user == "admin" and pw == "admin123":
                valid_user = "admin"
                role_name = "Admin"
                display_name = "Administrator"
            elif user == "user" and pw == "user123":
                valid_user = "user"
                role_name = "User"
                display_name = "General User"
            
            if valid_user:
                st.session_state.logged_in = True
                st.session_state.role = role_name
                st.session_state.username = display_name
                
                # Set Cookie
                if remember:
                    expires = datetime.datetime.now() + datetime.timedelta(days=10)
                    cookie_manager.set("user_session", valid_user, expires_at=expires)
                
                st.rerun()
            else:
                st.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

# 4. MAIN ROUTER
if not st.session_state.logged_in:
    login_page()
else:
    # Sidebar
    st.sidebar.title(f"👤 {st.session_state.username}")
    st.sidebar.write(f"Role: **{st.session_state.role}**")
    
    menu_options = {
        "EIS Dashboard (บทสรุปผู้บริหาร)": eis.show_view,
        "Revenue Dashboard (รายได้)": revenue.show_view,
    }

    # Logout Button
    if st.sidebar.button("🚪 ออกจากระบบ (Log off)"):
        st.session_state.logged_in = False
        st.session_state.role = None
        cookie_manager.delete("user_session")
        st.rerun()

    st.sidebar.divider()
    
    # --- FILE UPLOADER ---
    st.sidebar.markdown("### 📂 Upload Data")
    uploaded_file = st.sidebar.file_uploader("Choose Excel File", type=["xlsx"])
    
    if uploaded_file:
        if 'last_loaded_file' not in st.session_state or st.session_state.last_loaded_file != uploaded_file.name:
            success = load_data_from_excel(uploaded_file)
            if success:
                st.session_state.last_loaded_file = uploaded_file.name
                st.sidebar.success("✅ Data Loaded!")
                st.rerun()
        else:
            st.sidebar.info("✅ Using loaded data")
    else:
        st.sidebar.warning("⚠️ Please upload data")

    st.sidebar.divider()
    selection = st.sidebar.radio("เลือกเมนู:", list(menu_options.keys()))
    
    if selection in menu_options:
        menu_options[selection]()
