import streamlit as st
import os
import base64
import datetime
import time
from utils.styles import load_css
from utils.data_loader import save_and_load_excel, load_from_disk
from utils import auth
from utils import email_service
import extra_streamlit_components as stx

# Import Views
from views import eis, admin, user_management, audit, legal, hospital, strategy, finance, treasury, welfare, dorm, procurement, api_management

# 1. CONFIGURATION
st.set_page_config(page_title="ระบบศูนย์ข้อมูลกลาง สกสค.", layout="wide", page_icon="🏛️")
load_css()
cookie_manager = stx.CookieManager()

# 2. SESSION STATE SETUP
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = ""
    st.session_state.allowed_views = [] 

# Login Flow States
if "login_stage" not in st.session_state: st.session_state.login_stage = "credentials" 
if "temp_user_data" not in st.session_state: st.session_state.temp_user_data = {}
if "otp_secret" not in st.session_state: st.session_state.otp_secret = ""

# Navigation State (Default View)
if "current_view" not in st.session_state:
    st.session_state.current_view = "บทสรุปผู้บริหาร"

# --- AUTO LOGIN ---
if not st.session_state.logged_in:
    try:
        cookie_user = cookie_manager.get(cookie="user_session")
        if cookie_user:
            users = auth.load_users()
            if cookie_user in users:
                user_data = users[cookie_user]
                st.session_state.logged_in = True
                st.session_state.role = user_data["role"]
                st.session_state.username = user_data["name"]
                st.session_state.allowed_views = user_data.get("allowed_views", [])
                time.sleep(0.1)
                st.rerun()
    except Exception as e:
        print(f"Cookie read error: {e}")

# 3. UPLOAD DATA VIEW (New function for main window)
def show_upload_view():
    st.markdown("## 📂 อัปโหลดข้อมูล (Upload Data)")
    st.info("กรุณาอัปโหลดไฟล์ Excel (.xlsx) เพื่ออัปเดตข้อมูลในระบบ")
    
    # Load logic (Keep existing data logic)
    if 'df_eis' not in st.session_state:
        if load_from_disk(): st.session_state['data_loaded'] = True

    # Main Window File Uploader
    uploaded_file = st.file_uploader("ลากและวางไฟล์ที่นี่ (Drag and drop file here)", type=["xlsx"])
    
    if uploaded_file:
        if 'last_loaded_file' not in st.session_state or st.session_state.last_loaded_file != uploaded_file.name:
            with st.spinner("กำลังประมวลผลข้อมูล..."):
                if save_and_load_excel(uploaded_file):
                    st.session_state.last_loaded_file = uploaded_file.name
                    st.session_state['data_loaded'] = True
                    st.success("✅ บันทึกข้อมูลเรียบร้อยแล้ว! (Data Saved Successfully)")
                    time.sleep(1.5)
                    st.rerun()

    if st.session_state.get('data_loaded', False):
        st.success(f"สถานะข้อมูล: ✅ พร้อมใช้งาน (Source: {st.session_state.get('last_loaded_file', 'Saved File')})")
    else:
        st.warning("สถานะข้อมูล: ⚠️ ยังไม่มีข้อมูลในระบบ")

# 4. LOGIN PAGE
def login_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    LOGO_FILENAME = "image_11b1c9.jpg"
    logo_path = "assets/" + LOGO_FILENAME
    if not os.path.exists(logo_path): logo_path = LOGO_FILENAME

    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            st.markdown(f"""<div style="display: flex; justify-content: center; align-items: center; margin-bottom: 10px;"><img src="data:image/jpeg;base64,{encoded}" style="width: 150px; max-width: 80%; border-radius: 50%;"></div>""", unsafe_allow_html=True)
        except Exception as e: st.error(f"Error loading logo: {e}")
    else: st.markdown("<h1 style='text-align:center; font-size: 80px;'>🏛️</h1>", unsafe_allow_html=True)
    
    st.markdown("""<h1 style='text-align: center; margin-bottom: 0px; font-weight: bold;'>ยินดีต้อนรับ</h1><h3 style='text-align: center; margin-top: 5px; margin-bottom: 30px; font-weight: normal;'>ระบบศูนย์ข้อมูลกลาง สกสค.</h3>""", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        if st.session_state.login_stage == "credentials":
            st.caption("⚠️ **กรุณาเข้าสู่ระบบด้วยรหัสผ่าน**")
            user = st.text_input("ชื่อผู้ใช้ (Username)")
            pw = st.text_input("รหัสผ่าน (Password)", type="password")
            remember = st.checkbox("จำรหัสผ่านไว้ 10 วัน (Remember me)")
            
            if st.button("ถัดไป (Next)", use_container_width=True):
                user_data = auth.check_credentials(user, pw)
                if user_data:
                    otp = email_service.generate_otp()
                    user_email = user_data.get('email', '')
                    if not user_email or "@" not in user_email:
                        st.error("❌ บัญชีนี้ยังไม่ได้ระบุอีเมล กรุณาติดต่อ Admin")
                    else:
                        email_service.send_otp_email(user_email, otp)
                        st.info(f"🔑 **TEST MODE OTP:** {otp}") 
                        st.session_state.temp_user_data = user_data
                        st.session_state.temp_user_data['remember'] = remember
                        st.session_state.otp_secret = otp
                        st.session_state.login_stage = "otp"
                        time.sleep(5) 
                        st.rerun()
                else: st.error("❌ ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

        elif st.session_state.login_stage == "otp":
            st.warning(f"🔑 **TEST CODE:** {st.session_state.otp_secret}")
            st.info(f"📧 กรุณากรอกรหัส 6 หลักที่ส่งไปยัง {st.session_state.temp_user_data.get('email')}")
            otp_input = st.text_input("รหัส OTP", max_chars=6)
            c_back, c_conf = st.columns(2)
            with c_back:
                if st.button("ย้อนกลับ", use_container_width=True):
                    st.session_state.login_stage = "credentials"
                    st.rerun()
            with c_conf:
                if st.button("ยืนยัน (Verify)", type="primary", use_container_width=True):
                    if otp_input == st.session_state.otp_secret:
                        user_data = st.session_state.temp_user_data
                        st.session_state.logged_in = True
                        st.session_state.role = user_data["role"]
                        st.session_state.username = user_data["name"]
                        st.session_state.allowed_views = user_data.get("allowed_views", [])
                        if user_data.get('remember'):
                            expires = datetime.datetime.now() + datetime.timedelta(days=10)
                            cookie_manager.set("user_session", user_data['username'], expires_at=expires)
                        st.session_state.login_stage = "credentials"
                        st.session_state.otp_secret = ""
                        st.rerun()
                    else: st.error("❌ รหัส OTP ไม่ถูกต้อง")

# 5. MAIN ROUTER & SIDEBAR
if not st.session_state.logged_in:
    login_page()
else:
    # --- SIDEBAR HEADER ---
    st.sidebar.title(f"👤 {st.session_state.username}")
    st.sidebar.caption(f"Role: {st.session_state.role}")
    st.sidebar.divider()

    # --- DEFINE MENUS ---
    # 1. Dashboard List
    dashboard_map = {
        "บทสรุปผู้บริหาร": eis.show_view,
        "สำนักการคลัง": treasury.show_view,
        "กองคลัง-พัสดุ": procurement.show_view,
        "ภาพรวมฐานะการเงิน": finance.show_view,
        "กลุ่มนโยบายและยุทธศาสตร์": strategy.show_view,
        "โรงพยาบาล": hospital.show_view,
        "สวัสดิการ": welfare.show_view,
        "หอพัก สกสค.": dorm.show_view,
        "สำนักอำนวยการ": admin.show_view,
        "สำนักตรวจสอบภายใน": audit.show_view,
        "สำนักนิติการ": legal.show_view,
    }

    # Filter Dashboards based on privilege
    available_dashboards = {}
    if st.session_state.role in ["Admin", "Superuser"]:
        available_dashboards = dashboard_map
    else:
        for name, func in dashboard_map.items():
            if name in st.session_state.allowed_views:
                available_dashboards[name] = func

    # 2. Admin Functions
    admin_map = {
        "⚙️ จัดการผู้ใช้งาน (Users)": user_management.show_view,
        "🔌 จัดการ API (API Keys)": api_management.show_view,
        "📂 อัปโหลดข้อมูล (Upload)": show_upload_view
    }

    # --- RENDER SIDEBAR ---
    
    # GROUP 1: DASHBOARDS
    st.sidebar.markdown("### 📊 เมนู Dashboard")
    
    # We use buttons for navigation to avoid 'Radio' complexity with two groups
    for name in available_dashboards.keys():
        if st.sidebar.button(name, use_container_width=True, type="primary" if st.session_state.current_view == name else "secondary"):
            st.session_state.current_view = name
            st.rerun()

    # GROUP 2: ADMINISTRATIVE (Only for Admin)
    if st.session_state.role == "Admin":
        st.sidebar.markdown("---")
        st.sidebar.markdown("### ⚙️ เมนูการจัดการ")
        
        for name in admin_map.keys():
            if st.sidebar.button(name, use_container_width=True, type="primary" if st.session_state.current_view == name else "secondary"):
                st.session_state.current_view = name
                st.rerun()

        # Log off is part of the Admin Group visually
        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 ออกจากระบบ (Log off)", use_container_width=True, type="secondary"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.allowed_views = []
            st.session_state.login_stage = "credentials" 
            try: cookie_manager.delete("user_session")
            except: pass
            time.sleep(0.1) 
            st.rerun()

    # For Non-Admins, Log off is separate
    elif st.sidebar.button("🚪 ออกจากระบบ (Log off)", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.allowed_views = []
        st.session_state.login_stage = "credentials"
        try: cookie_manager.delete("user_session")
        except: pass
        time.sleep(0.1) 
        st.rerun()

    # --- RENDER MAIN CONTENT ---
    
    # Ensure data is loaded (Non-blocking check)
    if 'df_eis' not in st.session_state: load_from_disk()

    # Routing Logic
    if st.session_state.current_view in available_dashboards:
        available_dashboards[st.session_state.current_view]()
    elif st.session_state.current_view in admin_map and st.session_state.role == "Admin":
        admin_map[st.session_state.current_view]()
    else:
        # Fallback if view not found
        st.error(f"View '{st.session_state.current_view}' not found or access denied.")
        # Reset to default
        if available_dashboards:
            first_view = list(available_dashboards.keys())[0]
            if st.button(f"Go to {first_view}"):
                st.session_state.current_view = first_view
                st.rerun()
