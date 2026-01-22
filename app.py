import streamlit as st
import os
import base64
from utils.styles import load_css
from utils.data_loader import load_data_from_excel # Import the new function

# Import Views
from views import eis, revenue

# 1. CONFIGURATION
st.set_page_config(page_title="EIS Platform", layout="wide", page_icon="🏛️")
load_css()

# 2. SESSION STATE
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = ""

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
                <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 20px;">
                    <img src="data:image/jpeg;base64,{encoded}" style="width: 150px; max-width: 80%; border-radius: 50%;">
                </div>
                """, 
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Error loading logo: {e}")
    else:
        st.markdown("<h1 style='text-align:center; font-size: 80px;'>🏛️</h1>", unsafe_allow_html=True)
    
    # --- LOGIN FORM ---
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown('<div class="login-box"><h2 style="text-align: center;">🔐 เข้าสู่ระบบ</h2>', unsafe_allow_html=True)
        st.caption("⚠️ **ชื่อผู้ใช้และรหัสผ่านต้องระบุตัวพิมพ์เล็ก-ใหญ่ให้ถูกต้อง** (Case Sensitive)")
        
        user = st.text_input("ชื่อผู้ใช้ (Username)")
        pw = st.text_input("รหัสผ่าน (Password)", type="password")
        remember = st.checkbox("จำรหัสผ่านไว้ (Remember me)")
        
        if st.button("เข้าสู่ระบบ (Sign In)", use_container_width=True):
            if user == "admin" and pw == "admin123":
                st.session_state.logged_in, st.session_state.role, st.session_state.username = True, "Admin", "Administrator"
                st.rerun()
            elif user == "user" and pw == "user123":
                st.session_state.logged_in, st.session_state.role, st.session_state.username = True, "User", "General User"
                st.rerun()
            else:
                st.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
        st.markdown('</div>', unsafe_allow_html=True)

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

    if st.sidebar.button("🚪 ออกจากระบบ (Log off)"):
        st.session_state.logged_in = False
        st.rerun()

    st.sidebar.divider()
    
    # --- FILE UPLOADER (New!) ---
    st.sidebar.markdown("### 📂 Upload Data")
    uploaded_file = st.sidebar.file_uploader("Choose Excel File", type=["xlsx"])
    
    if uploaded_file:
        # Check if we already loaded this specific file to avoid reloading on every click
        if 'last_loaded_file' not in st.session_state or st.session_state.last_loaded_file != uploaded_file.name:
            success = load_data_from_excel(uploaded_file)
            if success:
                st.session_state.last_loaded_file = uploaded_file.name
                st.sidebar.success("✅ Data Loaded!")
                # Force a rerun to update graphs immediately
                st.rerun()
        else:
            st.sidebar.info("✅ Using loaded data")
    else:
        st.sidebar.warning("⚠️ Please upload data")

    st.sidebar.divider()
    selection = st.sidebar.radio("เลือกเมนู:", list(menu_options.keys()))
    
    if selection in menu_options:
        menu_options[selection]()
